import uvicorn
import config
from app import app, first_app_init

if __name__ == "__main__":
    first_app_init()
    uvicorn.run(app, host=config.api_host, port=config.port, log_level=config.log_level)
