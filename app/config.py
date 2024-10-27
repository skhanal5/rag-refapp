from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    hugging_face_token: str
    embedding_model: str
    reranking_model: str
    text_generation_model: str
    opensearch_hostname: str
    opensearch_port: int
    opensearch_username: str
    opensearch_password: str
    opensearch_ssl_flag: bool

    model_config = SettingsConfigDict(env_file=".env")
