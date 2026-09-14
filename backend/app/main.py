from fastapi import FastAPI

app = FastAPI(
    title="KaushalSaathi AI",
    description="AI-powered livelihood assistant for PM-AJAY",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "KaushalSaathi AI API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }