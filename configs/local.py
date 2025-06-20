from os import getenv

# this configuration has default values set
local_config = {
    "config": "local",
    "host": getenv("HOST", "0.0.0.0"),
    "port": int(getenv("PORT", "8000")),
    "mongo_connection_string": getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017/"),
    "mongo_database_name": getenv("MONGO_DATABASE_NAME", "pdf_management"),
    "postgres_connection_string": getenv("POSTGRES_CONNECTION_STRING", "postgresql+asyncpg://0.0.0.0:5432/iam"),
    "worker_count": int(getenv("WORKER_COUNT", "1")),
    # in seconds 5 days
    "refresh_token_ttl": int(getenv("REFRESH_TOKEN_TTL", "432000")),
    # in seconds 1 day
    "access_token_ttl": int(getenv("ACCESS_TOKEN_TTL", "86400")),
}
