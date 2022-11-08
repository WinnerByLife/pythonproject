import secrets
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from . import crud
from . import schemas

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=['Products'],
    prefix='/products'
)


@router.get("/api/products", response_model=list[schemas.ProductDetail])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_products(db)
    return users


@router.post("/api/product/create", response_model=schemas.ProductDetail)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)


@router.put("/api/product/update/{product_id}", response_model=schemas.ProductDetail)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db=db, product_id=product_id, product=product)


@router.post(("/api/product/upload_file/{product_id}"), response_model=schemas.ProductImageUpload)
async def upload_image(product_id: int, db: Session = Depends(get_db), file: UploadFile = File(...)):
    product = crud.get_product_by_id(db, product_id)
    FILEPATH = "./static/img/product/"
    filename = file.filename

    extension = filename.split(".")[1]

    if extension not in ["png", "jpg", "jpeg"]:
        return {"status": "error", "detail": "File extension not allowed."}

    token_name = secrets.token_hex(10)+"."+extension

    generated_name = FILEPATH + token_name
    file_content = await file.read()
    with open(generated_name, "wb") as file:
        file.write(file_content)

    product.images = generated_name



    print(product.images)
    db.add(product)
    db.commit()
    db.refresh(product)


@router.delete("/api/product/delete/{product_id}", response_model=schemas.ProductDetail)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db=db, product_id=product_id)
