from fastapi import FastAPI, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from typing import Annotated

app = FastAPI()


@app.post('/items')
def create_item(image:UploadFile, 
                title:Annotated[str,Form()], #title정보는 Form데이터 형식으로 문자열(str)
                price:Annotated[int,Form()], 
                desc:Annotated[str,Form()], 
                place:Annotated[str,Form()]):
    print(image,title,price,desc,place)
    return '200' #ok 사인


app.mount("/", StaticFiles(directory="frontend", html= True), name="frontend")


