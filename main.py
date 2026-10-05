from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


products = [
    {"id": 1, "name": "iPhone", "category": "phone", "price": 1000},
    {"id": 2, "name": "Samsung", "category": "phone", "price": 800},
    {"id": 3, "name": "Laptop", "category": "computer", "price": 1200},
    {"id": 4, "name": "iPad", "category": "tablet", "price": 600}
]


class ProductRequest(BaseModel):
    name: str = Field(min_length=2)
    category: str = Field(min_length=2)
    price: int = Field(gt=0)

class ProductPatch(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    category: str |None = Field(default=None, min_length=2, max_length=50)
    price: int |None= Field(default=None, ge=100)

class ProductResponse(BaseModel):
    id: int 
    name: str
    category: str
    price: int

@app.get("/")
def home():
    return {"message": "Welcome to online shopping"}


@app.get("/products/{id}", response_model = ProductResponse)
def get_product(id: int):
    for product in products:
        if product["id"] == id:
            return product

    raise HTTPException(
        status_code = 404,
        detail = "Product Not Found:"
    )


@app.get("/products")
def get_products(
    category: str | None = None,
    limit: int | None = None
):
    result = products

    if category:
        result = []

        for product in products:
            if product["category"] == category:
                result.append(product)

    if limit is not None:
        result = result[:limit]

    return result


@app.get("/productsprice")
def get_products_by_price(price: int):
    result = []

    for product in products:
        if product["price"] <= price:
            result.append(product)

    return result

@app.post("/products")
def create_product(product: ProductRequest):

    products.append(product.model_dump())
    return products

@app.put("/products/{id}")
def update_product(id: int, product: ProductRequest):

    for i in products:
        if i["id"] == id:
            i["name"] = product.name
            i["category"] = product.category
            i["price"] = product.price
            return i

    raise HTTPException(
            status_code=404,
            detail="Product Not Found"
     )
    


@app.delete("/products/{id}")
def delete_product(id: int):
    for product in products:
        if product["id"] == id:
            products.remove(product)
            return product

    raise HTTPException(
        status_code=404,
        detail="Product Not Found"
    )

@app.patch("/products/{id}")
def update_product_partial(id: int, product: ProductPatch):
    for item in products:
        if item["id"] == id:
            if product.name is not None:
                item["name"] = product.name
            if product.category is not None:
                item["category"] = product.category
            if product.price is not None:
                item["price"] = product.price

    
    raise HTTPException(
        status_code=404,
        detail="Product Not Found"
    )
    

