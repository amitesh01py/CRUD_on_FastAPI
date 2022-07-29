from fastapi import APIRouter, Depends, UploadFile, File
from datetime import datetime
from typing import List
from pydantic import FilePath
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from . models import *
from admin.apis.pydantic_models import Addsong, UserAdmin, UserLogin, Token, UpdateAdmin, DeleteAdmin
from fastapi_login import LoginManager
from email_validator import validate_email, EmailNotValidError
from distutils import extension


router = APIRouter()
SECRET = 'your-secret-key'
manager = LoginManager(SECRET, token_url='/user_login/')
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)    

@manager.user_loader()
async def load_user(email: str): 
    if await Admin.exists(e_mail=email):
        user = await Admin.get(e_mail=email)
        return user




@router.post("/song/")
async def create_songs(song:UploadFile=File(...), data:Addsong=Depends()):
    # try:
        if await Song.exists(song_name=data.song_name):
            return {"status": False, "messeges": "This song already exists"}
        else:
            FILEPATH = "static/song"
            filename = song.filename
            extension = filename.split(".")[1]
            songname = filename.split(".")[0]
            if extension not in ["mp3", "mp4"]:
                return {"status": "error", "detail":"File extention not allowed"}

            dt = datetime.now()
            dt_timestamp = round(datetime.timestamp(dt))

            modified_song_name = songname + "_" + str(dt_timestamp)+"."+ extension
            generated_name = FILEPATH + modified_song_name
            file_content = await song.read()
            with open (generated_name, "wb") as file:
                file.write(file_content)
                file.close()

            song_url = song_url + generated_name

            song_obj = await Song.create(
                song = song_url,
                song_name = data.song_name,
            )

            if song_obj:
                return{"status":True, "messege": "song added"}
            else:
                return{"status":False, "messege":"something wrong"}

    # except Exception as ex:
        # return {str(ex)}

@router.post("/admin/")
async def create_user(data: UserAdmin):
    try:
        try:  # Email velidaction
            valid = validate_email(data.e_mail)
        except EmailNotValidError as e:
            return {"status": False, "message": "invalid email id"}
        if len(data.phone_number) != 10:
            # mobile number velidaction
            return {"status": False, "message": "invalid number"}
        if await Admin.exists(phone_number=data.phone_number):
            return {"status": False, "message": "This number already register"}
        elif await Admin.exists(e_mail=data.e_mail):
            return {"status": False, "message": "This email id is already registered"}
        add_user = await Admin.create(full_name=data.full_name, e_mail=data.e_mail, phone_number=data.phone_number,
                                     password=get_password_hash(data.password))
    # return{"status":True, "messege":"ok"}
        return JSONResponse({
            "status": True,
            "message": "registered successfully"})
    except Exception as e:
        return JSONResponse({
            "status": False,
            "message": str(e)})

@router.post('/user_login/', )
async def login(data: UserLogin):
    email = data.e_mail
    user = await load_user(email)
    if not user:
        return JSONResponse({'status': False, 'message': 'User not Registered'}, status_code=403)
    elif not verify_password(data.password, user.password):
        return JSONResponse({'status': False, 'message': 'Invalid password'}, status_code=403)
    access_token = manager.create_access_token(
        data={'sub': jsonable_encoder(user.e_mail), "full_name": jsonable_encoder(user.full_name),
         "phone_number": jsonable_encoder(user.phone_number)})

    '''test  current user'''
    new_dict = jsonable_encoder(user)
    new_dict.update({"access_token": access_token})
    res = Token(access_token=access_token, token_type='bearer')
    return res

@router.put('/update_user')
async def update_user(data:UpdateAdmin):
    if await Admin.exists(id = data.id):
        admin_obj = await Admin.filter(id=data.id).update(full_name=data.full_name,
        e_mail=data.e_mail, phone_number=data.phone_number)
        return {"status": True, "message": "update admin"}

@router.delete('/delete_admin')
async def delete_admin(data:DeleteAdmin):
    delete_admin = await Admin.filter(id=data.id).delete()
    return {"message":"dalate admin successfully"} 

@router.get("/alluser")
async def read_user():
        allusers = await Admin.all()
        return allusers