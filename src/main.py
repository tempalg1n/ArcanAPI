import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.src:src", host="localhost", log_level="info")
