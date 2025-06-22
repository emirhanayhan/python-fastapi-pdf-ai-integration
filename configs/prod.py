from os import getenv

prod_config = {
    "config": "prod",
    "host": getenv("HOST"),
    "port": int(getenv("PORT", "8000")),
    "mongo_connection_string": getenv("MONGO_CONNECTION_STRING"),
    "mongo_database_name": getenv("MONGO_DATABASE_NAME"),
    "postgres_connection_string": getenv("POSTGRES_CONNECTION_STRING"),
    "worker_count": int(getenv("WORKER_COUNT", "1")),
    "refresh_token_ttl": int(getenv("REFRESH_TOKEN_TTL", "432000")),
    "access_token_ttl": int(getenv("ACCESS_TOKEN_TTL", "86400")),
    "gemini_api_key": getenv("GEMINI_API_KEY"),
    "gemini_base_url": getenv("GEMINI_BASE_URL"),
    "gemini_model": getenv("GEMINI_MODEL"),
}
