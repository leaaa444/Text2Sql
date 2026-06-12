#read variables from .env and define which patterns are we using
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


@dataclass
class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "anthropic")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "text2sql")
    db_admin_user: str = os.getenv("DB_ADMIN_USER", "t2s_admin")
    db_admin_password: str = os.getenv("DB_ADMIN_PASSWORD", "t2s_admin_pw")
    db_readonly_user: str = os.getenv("DB_READONLY_USER", "t2s_readonly")
    db_readonly_password: str = os.getenv("DB_READONLY_PASSWORD", "t2s_readonly_pw")
    result_limit: int = 100


settings = Settings()


@dataclass
class AblationConfig:
    use_retriever: bool = True
    use_selector: bool = True
    use_planner: bool = True
    use_integrator: bool = True
    use_security_guard: bool = True
    use_reflector: bool = True
    use_recorder: bool = True
    use_skill_build: bool = True
    max_retries: int = 3

    @classmethod
    def baseline(cls):
        return cls(
            use_retriever=False,
            use_selector=False,
            use_planner=False,
            use_integrator=False,
            use_security_guard=False,
            use_reflector=False,
            use_recorder=False,
            use_skill_build=False,
            max_retries=0,
        )
