"""Configuration management for the vendor evaluation agent."""
import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


class OpenAIConfig(BaseModel):
    """OpenAI API configuration."""
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = Field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"))
    temperature: float = 0.7
    max_tokens: int = 4000


class TelegramConfig(BaseModel):
    """Telegram bot configuration."""
    bot_token: str = Field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))
    enabled: bool = True


class ClawHubConfig(BaseModel):
    """ClawHub web-search configuration."""
    api_url: str = Field(default_factory=lambda: os.getenv("CLAWHUB_API_URL", "https://api.clawhub.com"))
    search_timeout: int = Field(default_factory=lambda: int(os.getenv("CLAWHUB_SEARCH_TIMEOUT", "30")))


class AgentConfig(BaseModel):
    """Agent behavior configuration."""
    max_candidates: int = Field(default_factory=lambda: int(os.getenv("MAX_CANDIDATES", "5")))
    research_depth: str = Field(default_factory=lambda: os.getenv("RESEARCH_DEPTH", "comprehensive"))
    enable_dynamic_weighting: bool = Field(default_factory=lambda: os.getenv("ENABLE_DYNAMIC_WEIGHTING", "true").lower() == "true")
    enable_hidden_risk_detection: bool = Field(default_factory=lambda: os.getenv("ENABLE_HIDDEN_RISK_DETECTION", "true").lower() == "true")


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_file: str = Field(default_factory=lambda: os.getenv("LOG_FILE", "agent.log"))


class Config(BaseModel):
    """Main configuration class."""
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    clawhub: ClawHubConfig = Field(default_factory=ClawHubConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


# Global configuration instance
config = Config()
