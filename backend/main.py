from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routes.stock import router as stock_router
from routes.predict import router as predict_router
from routes.news import router as news_router

app = FastAPI(title="AI-Driven Indian Stock Market API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_router, prefix="/api", tags=["stock"])
app.include_router(predict_router, prefix="/api", tags=["predict"])
app.include_router(news_router, prefix="/api", tags=["news"])


@app.get("/")
def root():
    return {"status": "ok"}


