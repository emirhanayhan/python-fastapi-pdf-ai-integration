from os import getenv

prod_config = {
    "config": "local",
    "host": getenv("HOST"),
    "port": int(getenv("PORT")),
    "mongo_connection_string": getenv("MONGO_CONNECTION_STRING"),
    "mongo_database_name": getenv("MONGO_DATABASE_NAME"),
    "postgres_connection_string": getenv("POSTGRES_CONNECTION_STRING"),
    "worker_count": int(getenv("WORKER_COUNT")),
    "refresh_token_ttl": int(getenv("REFRESH_TOKEN_TTL")),
    "access_token_ttl": int(getenv("ACCESS_TOKEN_TTL")),
    "gemini_api_key": getenv("GEMINI_API_KEY"),
    "gemini_base_url": getenv("GEMINI_BASE_URL"),
    "gemini_model": getenv("GEMINI_MODEL"),
}
