from fastapi import FastAPI, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated

#SQL Lite 사용할 준비
import sqlite3
con = sqlite3.connect('db.db',check_same_thread=False) 
cur = con.cursor()



app = FastAPI()


@app.post('/items')
async def create_item(image:UploadFile, 
                title:Annotated[str,Form()], #title정보는 Form데이터 형식으로 문자열(str)
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):
    
    #이미지 읽을 시간 확보
    image_bytes = await image.read()
    
    cur.execute(f""" 
                INSERT INTO items (title,image,price,description,place,insertAt)
                VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}','{insertAt}')                 
                """) #f문자열, items라는 테이블에 들어갈 값 설정. image_bytes 16진법으로 저장: hex()
    
    con.commit()    
    
    return '200' #ok 사인

@app.get('/items')
async def get_items():
    con.row_factory = sqlite3.Row #컬럼명도 같이 가져옴
    cur = con.cursor()
    rows = cur.execute(f"""
                        SELECT * from items;
                        """).fetchall()
    return JSONResponse(
        jsonable_encoder(dict(row) for row in rows)
        )

# rows = [['id',1],['title','팝니다'],['description','상태 좋아요']...]
# dict(row) for row in rows
# 결과 : [{id:1, title:'팝니다', description:'상태 좋아요'},{id:2, title : '   ' ,description:'  '}....]
    
app.mount("/", StaticFiles(directory="frontend", html= True), name="frontend")


