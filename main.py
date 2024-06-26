from fastapi import FastAPI, UploadFile, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated

#SQL Lite 사용할 준비
import sqlite3
con = sqlite3.connect('db.db',check_same_thread=False) 
cur = con.cursor()

#테이블이 없을때만 테이블 생성  IF NOT EXISTS
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items(
	            id INTEGER PRIMARY KEY,
	            title TEXT NOT NULL,
	            image BLOB,
	            price INTEGER NOT NULL,
	            description TEXT,
	            place TEXT NOT NULL,
	            insertAt INTEGER NOT NULL
            );
            """)


app = FastAPI()

SERCRET = 'super-coding'
manager = LoginManager(SERCRET,'/login')

@manager.user_loader()
def query_user(id):
    con.row_factory = sqlite3.Row #컬럼명도 같이 가져옴
    cur=con.cursor()
    user = cur.execute(f"""
                       SELECT * from users WHERE id='{id}'
                       """).fetchone()
    return user
    
@app.post('/login')
def login(id:Annotated[str,Form()], 
           password:Annotated[str,Form()]):
    user = query_user(id)
    if not user:
        raise InvalidCredentialsException #에러메시지 던지기
    elif password != user['password']:
        raise InvalidCredentialsException #에러메시지 던지기
    
    access_token = manager.create_access_token(data={
        'id':user['id'],
        'name':user['name'],
        'email':user['email']
        
    })
    
    return {'access_token':access_token} #'리턴값' 상관 없이 '상태코드' 자동으로 200



@app.post('/signup')
def signup(id:Annotated[str,Form()], 
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    
    #DB에 저장
    #이미 회원가입이 되어있는 사람은 중복 가입 안되도록 처리 해야됨. (추가해보기)
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES ('{id}','{name}','{email}','{password}')
                """)
    con.commit()
    return '200'



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



@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    #16진법
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                              """).fetchone()[0] #열 1개만 가져오기 [0]번째 인덱스
    
    return Response(content=bytes.fromhex(image_bytes), media_type="image/*")


           
    
app.mount("/", StaticFiles(directory="frontend", html= True), name="frontend")


