import uvicorn

from src.main import make_app

if __name__ == "__main__":
    uvicorn.run(
        make_app(),
        host="0.0.0.0",  # noqa: S104
        port=8000,
    )
