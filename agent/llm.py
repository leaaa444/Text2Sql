#swithcing between models
 
from agent.config import settings

_NO_TEMPERATURE_PREFIXES = ("claude-opus-4-8", "claude-opus-4-7")


def get_llm(provider=None, model=None):
    provider = provider or settings.llm_provider
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        chosen = model or settings.anthropic_model
        kwargs = {"model": chosen, "max_tokens": 2000, "timeout": 60}
        if not chosen.startswith(_NO_TEMPERATURE_PREFIXES):
            kwargs["temperature"] = 0
        return ChatAnthropic(**kwargs)
    if provider in ("google", "gemini"):
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=model or settings.gemini_model, temperature=0)
    raise ValueError(f"Nepoznat LLM provajder: {provider}")
