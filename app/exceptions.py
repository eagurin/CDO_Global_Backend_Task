# app/exceptions.py

from fastapi import HTTPException, status


class ItemNotFoundException(HTTPException):
    def __init__(self):
        detail = "Элемент не найден"
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(status_code=status_code, detail=detail)
        self.status_code = status_code

    def as_dict(self):
        return {"status": self.status_code, "detail": self.detail}


class NoItemsFoundException(HTTPException):
    def __init__(self):
        detail = "Не найдено ни одного элемента"
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(status_code=status_code, detail=detail)
        self.status_code = status_code

    def as_dict(self):
        return {"status": self.status_code, "detail": self.detail}
