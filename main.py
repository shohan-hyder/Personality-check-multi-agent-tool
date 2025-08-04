from fastapi import FastAPI
from endpoints.endpoint import router as query_router
import uvicorn

app = FastAPI(title="Multi-Agents API")
app.include_router(query_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "AI Multi-Agent System is running", "docs": "/api/docs"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)