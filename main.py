import optparse
import uvicorn

from configs.local import local_config
from src import create_fastapi_app


CONFIG_LOOKUP = {
    "local": local_config,
    "prod": "",
    "stage": ""
}


def config_settings(config_name, run_migrations):
    config = CONFIG_LOOKUP[config_name]
    config.update({"run_migrations": True if run_migrations in ["true", "True"] else False})
    return config


parser = optparse.OptionParser()
parser.add_option("--config", default="local", help="Which config to load")
parser.add_option("--migrate", default=False, help="Migrate models to db on startup")
options, args = parser.parse_args()

settings = config_settings(options.config, options.migrate)


app = create_fastapi_app(settings)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings["host"], port=settings["port"], workers=settings["worker_count"])
