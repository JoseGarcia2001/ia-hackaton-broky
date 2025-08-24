from pydantic import BaseModel


class QRResponse(BaseModel):
    success: bool
    message: str
    template_name: str

