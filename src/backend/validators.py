import os

from backend.constants import ChatModel
from backend.utils import is_local_model, strtobool


def validate_model(model: ChatModel):
    if model in {ChatModel.GPT_4o_mini, ChatModel.GPT_4o}:
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable not found. Please add your OpenAI API key to the .env file.")
        if model == ChatModel.GPT_4o:
            GPT4_ENABLED = strtobool(os.getenv("GPT4_ENABLED", True))
            if not GPT4_ENABLED:
                raise ValueError(
                    "GPT-4o has been disabled. Please try a different model or enable GPT-4 in your environment settings."
                )

    elif model == ChatModel.LLAMA_3_70B:
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable not found. Please add your Groq API key to the .env file.")
    elif is_local_model(model):
        LOCAL_MODELS_ENABLED = strtobool(os.getenv("ENABLE_LOCAL_MODELS", True))
        if not LOCAL_MODELS_ENABLED:
            raise ValueError("Local models are not enabled. Please enable local models in your environment settings.")
    else:
        raise ValueError("Invalid model selected")
    return True