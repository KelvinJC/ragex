import uvicorn

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run('app:app', host="127.0.0.1", port=8888, reload=True)