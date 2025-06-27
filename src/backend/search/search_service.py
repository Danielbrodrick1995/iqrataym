import json
import os
import re
import httpx
import asyncio

import redis
from dotenv import load_dotenv
from fastapi import HTTPException

from backend.schemas import SearchResponse
from backend.search.providers.base import SearchProvider
from backend.search.providers.bing import BingSearchProvider
from backend.search.providers.searxng import SearxngSearchProvider
from backend.search.providers.serper import SerperSearchProvider
from backend.search.providers.tavily import TavilySearchProvider

load_dotenv()


redis_url = os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(redis_url) if redis_url else None


def get_searxng_base_url():
    searxng_base_url = os.getenv("SEARXNG_BASE_URL")
    if not searxng_base_url:
        raise HTTPException(
            status_code=500,
            detail="SEARXNG_BASE_URL is not set in the environment variables.",
        )
    return searxng_base_url


def get_tavily_api_key():
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise HTTPException(
            status_code=500,
            detail="Tavily API key is not set in the environment variables. Please set the TAVILY_API_KEY environment variable or set SEARCH_PROVIDER to 'searxng' or 'serper'.",
        )
    return tavily_api_key


def get_serper_api_key():
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        raise HTTPException(
            status_code=500,
            detail="Serper API key is not set in the environment variables. Please set the SERPER_API_KEY environment variable or set SEARCH_PROVIDER to 'searxng' or 'tavily'.",
        )
    return serper_api_key


def get_bing_api_key():
    bing_api_key = os.getenv("BING_API_KEY")
    if not bing_api_key:
        raise HTTPException(
            status_code=500,
            detail="Bing API key is not set in the environment variables. Please set the BING_API_KEY environment variable or set SEARCH_PROVIDER to 'searxng', 'tavily', or 'serper'.",
        )
    return bing_api_key


def get_search_provider() -> SearchProvider:
    search_provider = os.getenv("SEARCH_PROVIDER", "searxng")

    match search_provider:
        case "searxng":
            searxng_base_url = get_searxng_base_url()
            return SearxngSearchProvider(searxng_base_url)
        case "tavily":
            tavily_api_key = get_tavily_api_key()
            return TavilySearchProvider(tavily_api_key)
        case "serper":
            serper_api_key = get_serper_api_key()
            return SerperSearchProvider(serper_api_key)
        case "bing":
            bing_api_key = get_bing_api_key()
            return BingSearchProvider(bing_api_key)
        case _:
            raise HTTPException(
                status_code=500,
                detail="Invalid search provider. Please set the SEARCH_PROVIDER environment variable to either 'searxng', 'tavily', 'serper', or 'bing'.",
            )


# --- Iqra Taym strict whitelist: only accept results from recognised Islamic sources
ALLOWED_DOMAINS: list[str] = [
    "quran.com",
    "sunnah.com",
    "islamqa.info",
    "seekersguidance.org",
    "daruliftaa.com",
    "aboutislam.net",
    "islamicstudies.info",
    "qurancentral.com",
]


async def perform_search(query: str) -> SearchResponse:
    search_provider = get_search_provider()

    try:
        cache_key = f"search:{query}"
        if redis_client and (cached_results := redis_client.get(cache_key)):
            cached_json = json.loads(json.loads(cached_results.decode("utf-8")))  # type: ignore
            return SearchResponse(**cached_json)

        results = await search_provider.search(query)

        # Filter link results by allowed domains
        filtered_results = [
            r for r in results.results if any(domain in r.url for domain in ALLOWED_DOMAINS)
        ]

        # If nothing remains, return empty response; upstream will trigger apology via prompt
        if not filtered_results:
            return SearchResponse(results=[], images=[])

        results.results = filtered_results

        # --- Enrich Qur'an links with actual verse text so LLM can quote
        async def enrich_quran(result):
            if "quran.com" not in result.url:
                return result

            # Attempt to extract surah and ayah
            m = re.search(r"quran\.com/(\d+)(?:/(\d+))?", result.url)
            if not m:
                return result
            surah = m.group(1)
            ayah = m.group(2)
            verse_key = f"{surah}:{ayah}" if ayah else f"{surah}:1"

            api_url = f"https://api.quran.com/api/v4/verses/by_key/{verse_key}?language=en&translations=131"  # 131 = Saheeh Intl
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(api_url, timeout=5)
                    if r.status_code == 200:
                        data = r.json()
                        verse_text = data.get("verse", {}).get("text_uthmani", "")
                        translation = data.get("verse", {}).get("translations", [{}])[0].get("text", "")
                        if verse_text:
                            combined = f"{verse_text} — {translation}"
                            from backend.schemas import SearchResult  # local import to avoid circular

                            result = SearchResult(
                                title=result.title,
                                url=result.url,
                                content=combined,
                            )
            except Exception:
                pass
            return result

        results.results = await asyncio.gather(*[enrich_quran(r) for r in results.results])

        if redis_client:
            redis_client.set(cache_key, json.dumps(results.model_dump_json()), ex=7200)

        return results
    except Exception:
        raise HTTPException(
            status_code=500, detail="There was an error while searching."
        )
