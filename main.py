import uvicorn
import config
from app import app

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port, log_level=config.log_level)
