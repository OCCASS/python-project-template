import uvicorn
from fastapi import FastAPI

from src.models import PinnacleEvent
from src.pinnacle import Pinnacle

app = FastAPI()


@app.post('/fetch_cart/')
async def handle_fetch_cart(event: PinnacleEvent):
    pinnacle = Pinnacle()
    return await pinnacle.fetch_odds(event)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=3030)
