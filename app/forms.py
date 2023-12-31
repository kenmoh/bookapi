from fastapi import Form, Depends, UploadFile
from app.utils import add_image


class AddMovieForm:
    def __init__(
        self,
        length: float = Form(...),
        title: str = Form(...),
        descr: str = Form(...),
        casts: str = Form(...),
        genre: str = Form(None),
        thriller: str = Form(None),
        item_type: str = Form(None),
        image: UploadFile = Depends(add_image),
    ):
        self.title = title
        self.length = length
        self.descr = descr
        self.casts = casts
        self.genre = genre
        self.thriller = thriller
        self.image = image
        self.item_type = item_type
