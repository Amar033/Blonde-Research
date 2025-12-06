from pydantic_settings import BaseSettings
from typing import Optional, List
class Settings(BaseSettings):
    # App
    APP_NAME: str = "LLaMA Chatbot"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # vLLM
    VLLM_API_URL: str = "http://localhost:8000/v1"
    VLLM_API_KEY: Optional[str] = None
    
    # Web Search
    TAVILY_API_KEY: Optional[str] = None
    ENABLE_WEB_SEARCH: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/chatbot.db"
    
    # CORS
    CORS_ALLOW_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]
    
    # Model
    DEFAULT_MODEL: str = "llama-3.3-70b-instruct"
    DEFAULT_MAX_TOKENS: int = 2048
    DEFAULT_TEMPERATURE: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()