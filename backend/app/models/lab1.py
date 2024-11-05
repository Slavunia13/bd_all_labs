from pydantic import BaseModel

class KeyValue(BaseModel):
    key: str
    value: str

class UserSettings(BaseModel):
    font_name: str
    font_size: str
    font_color: str
    font_style: str

class TextRequest(BaseModel):
    text: str