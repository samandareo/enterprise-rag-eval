from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://rag_user:rag_password@localhost:5432/enterprise_rag"
    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"

    # hyperparameters
    chunk_size_chars: int = 1200
    chunk_overlap_chars: int = 200
    rrf_k: int = 60
    retrieval_top_n: int = 20
    rerank_top_k: int = 5

    model_config: SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
