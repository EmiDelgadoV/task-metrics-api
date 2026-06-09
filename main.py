from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Docker funciona godines"}

@app.get("/health")
def health():
    return {"status": "ok"}