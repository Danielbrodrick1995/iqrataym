# Iqra Taym - Islamic Knowledge Oracle

Iqra Taym is a source-anchored Islamic AI assistant that provides answers grounded in authentic Islamic sources (Qur'an, Sahih Hadith, classical scholarship, and recognised fiqh opinions).

## Features

- **Source-First Responses**: Every answer is backed by authentic Islamic sources
- **Citation System**: Inline citations with direct links to sources
- **Multi-Madhhab Support**: Presents different scholarly opinions where applicable
- **Bias Resistance**: Focuses on traditional Islamic knowledge over modern interpretations
- **Clean UI**: Modern, responsive interface inspired by leading search platforms

## Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key (for GPT models)
- Optional: Groq API key, Ollama for local models

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/iqra-taym.git
   cd iqra-taym
   ```

2. **Configure environment variables**
   ```bash
   cp .env-template .env
   ```
   
   Edit `.env` and add your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   GROQ_API_KEY=your_groq_api_key_here  # Optional
   ```

3. **Start the application**
   ```bash
   docker compose -f docker-compose.dev.yaml up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Search Engine: http://localhost:8080

## Development

### Local Development (without Docker)

1. **Backend Setup**
   ```bash
   cd src/backend
   poetry install
   poetry run alembic upgrade head
   poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Frontend Setup**
   ```bash
   cd src/frontend
   pnpm install
   pnpm dev
   ```

3. **Search Engine**
   You'll need to run SearxNG separately or use an external search provider.

### Environment Variables

Key environment variables you need to set:

- `OPENAI_API_KEY`: Required for GPT models
- `GROQ_API_KEY`: Optional, for Groq models
- `SEARCH_PROVIDER`: Set to `searxng` for local search
- `DATABASE_URL`: PostgreSQL connection string
- `NEXT_PUBLIC_API_URL`: Frontend API endpoint

## Architecture

- **Backend**: FastAPI with PostgreSQL database
- **Frontend**: Next.js with TypeScript
- **Search**: SearxNG for web search
- **AI Models**: OpenAI GPT, Groq, or local Ollama models

## Islamic Source Filtering

The application filters search results to only include recognized Islamic sources:
- quran.com
- sunnah.com
- islamqa.info
- seekersguidance.org
- daruliftaa.com
- aboutislam.net
- islamicstudies.info
- qurancentral.com

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

Apache License 2.0 - see LICENSE file for details.

## Acknowledgments

Based on the Farfalle project architecture with Islamic-specific modifications.