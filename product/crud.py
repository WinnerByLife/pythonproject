from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas
from .models import Product


def get_product_by_id(db: Session, product_id: int) -> Session.query:
    product = db.query(models.Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    return product


def get_product_id(db: Session, product_id: int) -> Session.query:
    product = db.query(models.Product).filter(Product.product_id == product_id).first()
    return product


def get_all_products_skips(db: Session, skip: int = 0, limit: int = 100) -> Session.query:
    return db.query(Product).offset(skip).limit(limit).all()


def get_all_products(db: Session, ) -> Session.query:
    return db.query(Product).all()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def update_product(db: Session, product: schemas.ProductUpdate, product_id):
    product_data = product.dict(exclude_unset=True)
    updating_product = get_product_by_id(db, product_id)
    for key, value in product_data.items():
        setattr(updating_product, key, value)
    db.add(updating_product)
    db.commit()
    db.refresh(updating_product)
    return updating_product


def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    db.delete(product)
    db.commit()
    raise HTTPException(status_code=200, detail="Product successfully deleted")



