from typing import Union

from fastapi import FastAPI
from modules.input_cleaner import combined_pipeline
from modules.send_email import send_email
from modules.tg_notif import check_and_notify
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str


class Item_for_tg_notif(BaseModel):
    name: str
    chat_id: str


@app.post("/send_email_with_data/")
async def create_item(item: Item):
    """
    передаем EXPERIMENT_NAME переменную текстом. пример: `KJE0008`
    """
    send_email(item.name)
    return item


@app.post("/prepare_inputs/")
async def create_item(item: Item):
    """
    передаем EXPERIMENT_NAME переменную текстом. пример: `KJE0008`
    """
    combined_pipeline(item.name)
    return item


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/send_notif_tg/")
async def create_item_id(item: Item_for_tg_notif):
    """
    передаем chat_id переменную текстом. пример: `234234235`
    """
    check_and_notify(item.name, item.chat_id)
    return item
