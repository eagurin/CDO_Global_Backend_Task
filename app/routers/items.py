# app/routers/items.py

import csv
from io import StringIO

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import ItemNotFoundException, NoItemsFoundException
from app.schemas import CreateSchema, ItemSchema, UpdateSchema
from app.service import ItemService

router = APIRouter()
item_service = ItemService()


@router.post(
    "/items/", response_model=ItemSchema, status_code=status.HTTP_201_CREATED
)
def create_item(item: CreateSchema, db: Session = Depends(get_db)):
    return item_service.create_item(db, item)


@router.get("/items/all")
def read_all_items_as_csv(db: Session = Depends(get_db)):
    items = item_service.get_all_items(db)
    if not items:
        raise NoItemsFoundException()

    csv_data = StringIO()
    csv_writer = csv.DictWriter(
        csv_data, fieldnames=["id", "name", "description"]
    )
    csv_writer.writeheader()
    for item in items:
        csv_writer.writerow(
            {"id": item.id, "name": item.name, "description": item.description}
        )

    csv_data.seek(0)
    return StreamingResponse(
        iter([csv_data.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=items.csv"},
    )


@router.get("/items/{item_id}", response_model=ItemSchema)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = item_service.get_item_by_id(db, item_id)
    if item is None:
        raise ItemNotFoundException()
    return item


@router.put("/items/{item_id}", response_model=ItemSchema)
def update_item(
    item_id: int, item: UpdateSchema, db: Session = Depends(get_db)
):
    updated_item = item_service.update_item(db, item_id, item)
    if updated_item is None:
        raise ItemNotFoundException()
    return updated_item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted = item_service.delete_item(db, item_id)
    if not deleted:
        raise ItemNotFoundException()
