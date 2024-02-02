from fastapi import APIRouter, Form, UploadFile, File, Request
from fastapi.responses import StreamingResponse
from app.Utils.Answer_Question import answer_question
from app.Models.Chatbot_Model import Question_Model
import time
import asyncio
import os
import shutil
# import requests

router = APIRouter()


@router.post("/user-question")
# def answer_user_question(question: Question_Model):
def answer_user_question(msg: str = Form(...)):
    try:
        return StreamingResponse(answer_question(msg), media_type='text/event-stream')
    except Exception as e:
        print(e)
        return e
