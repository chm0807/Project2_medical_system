from fastapi import FastAPI
from router import router as api_router

app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8040)
