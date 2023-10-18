from typing import Union

from fastapi import FastAPI
from modules.send_email import send_email

app = FastAPI()

@app.get("/sendemail")
def read_root():
    return {send_email()}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
