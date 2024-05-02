# app/service.py

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Item
from app.schemas import CreateSchema, UpdateSchema

class ItemService:
    @staticmethod
    def get_item_by_id(db: Session, item_id: int) -> Optional[Item]:
        return db.query(Item).filter(Item.id == item_id).first()

    @staticmethod
    def get_all_items(db: Session) -> List[Item]:
        return db.query(Item).all()

    @staticmethod
    def create_item(db: Session, item: CreateSchema) -> Item:
        db_item = Item(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def update_item(db: Session, item_id: int, item_data: UpdateSchema) -> Optional[Item]:
        db_item = ItemService.get_item_by_id(db, item_id)
        if not db_item:
            return None
        for key, value in item_data.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def delete_item(db: Session, item_id: int) -> bool:
        db_item = ItemService.get_item_by_id(db, item_id)
        if not db_item:
            return False
        db.delete(db_item)
        db.commit()
        return True
