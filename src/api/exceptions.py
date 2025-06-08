from fastapi import HTTPException, status


class BadRequestError(HTTPException):
    def __init__(self, code: str | None = None) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=code)


class NotFoundError(HTTPException):
    def __init__(self, code: str | None = None) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=code)
