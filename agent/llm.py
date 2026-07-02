#swithcing between models

from agent import metrics
from agent.config import settings

_NO_TEMPERATURE_PREFIXES = ("claude-opus-4-8", "claude-opus-4-7")

_limiter = None


def _rate_limiter():
    global _limiter
    if _limiter is None:
        from langchain_core.rate_limiters import InMemoryRateLimiter

        _limiter = InMemoryRateLimiter(
            requests_per_second=settings.llm_rps,
            check_every_n_seconds=0.5,
            max_bucket_size=1,
        )
    return _limiter


def get_llm(provider=None, model=None):
    provider = provider or settings.llm_provider
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        chosen = model or settings.anthropic_model
        kwargs = {
            "model": chosen,
            "max_tokens": 2000,
            "timeout": 60,
            "rate_limiter": _rate_limiter(),
            "callbacks": [metrics.counter],
        }
        if not chosen.startswith(_NO_TEMPERATURE_PREFIXES):
            kwargs["temperature"] = 0
        return ChatAnthropic(**kwargs)
    if provider in ("google", "gemini"):
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=model or settings.gemini_model,
            temperature=0,
            max_retries=6,
            rate_limiter=_rate_limiter(),
            callbacks=[metrics.counter],
        )
    if provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(
            model=model or settings.groq_model,
            temperature=0,
            rate_limiter=_rate_limiter(),
            callbacks=[metrics.counter],
        )
    raise ValueError(f"Nepoznat LLM provajder: {provider}")
