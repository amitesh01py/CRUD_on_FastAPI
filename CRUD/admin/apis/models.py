from dataclasses import fields
from tortoise.models import Model
from tortoise import fields, Tortoise
from enum import auto
from fastapi import FastAPI
from tortoise.models import Model
from datetime import datetime



class Song(Model):
    id = fields.UUIDField(pk=True)
    song_name = fields.CharField(100)
    song = fields.TextField()
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class Admin(Model):
    id = fields.UUIDField(pk=True)
    full_name = fields.CharField(100, Uniqe=True)
    e_mail = fields.CharField(100)
    phone_number = fields.CharField(10, uniqe=True)
    password = fields.TextField()


# class AddUser(Model):
#     id= fields.UUIDField()
#     fname= fields.CharField(100)
#     mobile= fields.CharField(100)
#     email= fields.CharField(100)
#     password= fields.TextField()    
    

  