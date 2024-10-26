from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class Settings(BaseModel):
    hugging_face_token: str
    embedding_model: str
    reranking_model: str
    text_generation_model: str

    model_config = SettingsConfigDict(env_file=".env")
