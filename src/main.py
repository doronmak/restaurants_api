import uvicorn
from src.settings import config
from src.app import app, first_app_init

if __name__ == "__main__":
    first_app_init()
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT, log_level=config.LOG_LEVEL)