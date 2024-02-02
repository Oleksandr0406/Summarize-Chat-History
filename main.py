from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import app.Routers.Chatbot as Chatbot
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(Chatbot.router, tags=["chatbot"])

# app.mount("/static", StaticFiles(directory="./data"), name="static")

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
