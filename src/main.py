import uvicorn
from settings import config
from app import app, first_app_init

if __name__ == "__main__":
    first_app_init()
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
