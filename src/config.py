from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    discord_token: str
    koboldcpp_api_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Load the settings
settings = Settings()
