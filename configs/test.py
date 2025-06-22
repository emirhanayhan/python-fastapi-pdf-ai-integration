from os import getenv

# this configuration has default values set
test_config = {
    "config": "local",
    "host": getenv("HOST", "0.0.0.0"),
    "port": int(getenv("PORT", "8000")),
    "mongo_connection_string": getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017/"),
    # use test databases
    "mongo_database_name": getenv("MONGO_DATABASE_NAME", "pdf_management_test"),
    "postgres_connection_string": getenv("POSTGRES_CONNECTION_STRING", "postgresql+asyncpg://0.0.0.0:5432/iam_test"),
    "worker_count": int(getenv("WORKER_COUNT", "1")),
    # in seconds 5 days
    "refresh_token_ttl": int(getenv("REFRESH_TOKEN_TTL", "432000")),
    # in seconds 1 day
    "access_token_ttl": int(getenv("ACCESS_TOKEN_TTL", "86400")),
    "gemini_api_key": getenv("GEMINI_API_KEY"),
    "gemini_base_url": getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    "gemini_model": getenv("GEMINI_MODEL", "gemini-2.5-flash"),
}