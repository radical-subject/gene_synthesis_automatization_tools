from typing import Union

from modules.input_cleaner import combined_pipeline
from modules.send_email import send_email
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


class Item(BaseModel):
    name: str | None = None


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
