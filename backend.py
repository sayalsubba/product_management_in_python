from fastapi import FastAPI, HTTPException
app= FastAPI()
import psycopg
from pydantic import BaseModel
from contextlib import closing
from psycopg.rows import dict_row


# DATABASE CONFIGURATION

DB_HOST ="localhost"
DB_NAME = "postgres"
DB_USER="sayalsubba"
DB_PASSWORD = "12345678"
DB_PORT =5432

##Data connection
def data_connect():
    return psycopg.connect(
            host =DB_HOST,
            dbname = DB_NAME,
            user= DB_USER,
            password =DB_PASSWORD,
            port = DB_PORT
        )
    

class Product(BaseModel):
    name:str
    color:str

    ## HOME__PAGE
@app.get("/")
def home():
    return{
        "message":"Welcome to my website!!"
    }

##Get products
@app.get("/products")
def get_products():
    with data_connect() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM products")
            result = cursor.fetchall()
            
    return result

@app.post("/products")
def create_products(product:Product):
    with data_connect() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("INSERT INTO products(name,color) VALUES(%s,%s) RETURNING *",
                          (product.name,product.color) )
            result = cursor.fetchone()
    return result

@app.get("/products/{product_id}")
def search_product(product_id:int):
    with data_connect() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s",
                         (product_id,))
            product = cursor.fetchone()
                      
            if product is None:
                    raise HTTPException(status_code=404, detail="Product Not Found!!!")
            return product

@app.patch("/products/{product_id}")
def update_product(product_id:int, product:Product):
   with data_connect() as conn:
      with conn.cursor(row_factory=dict_row) as cursor:
          cursor.execute("UPDATE products SET name = %s, color =%s WHERE id = %s RETURNING *",
                         (product.name,product.color,product_id,))
          product = cursor.fetchone()
          
          if product is None:
              raise HTTPException(status_code=404, detail="Product Not Found!!!")
      return product
          


