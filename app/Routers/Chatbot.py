from fastapi import APIRouter, Form, UploadFile, File, Request, HTTPException
from fastapi.responses import StreamingResponse
from app.Utils.Answer_Question import answer_question
from app.Models.Chatbot_Model import Question_Model
from app.Models.ChatLog_Model import delete_summary_db_id
from app.Utils.Pinecone import train_csv, train_ms_word, train_ms_word, train_pdf
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

@router.post("/create-new-thread")
def create_new_thread():
    log_id = "goldrace"
    delete_summary_db_id(log_id)

supported_file_extensions = [".csv", ".pdf", ".txt", ".doc", ".docx"]

@router.post("/add-training-file")
def add_training_file_api(file: UploadFile = File(...)):
    print("here")
    extension = os.path.splitext(file.filename)[1]
    if extension not in supported_file_extensions:
        raise HTTPException(
            status_code=500, detail="Invalid file type!")
    print("valid filetype")
    try:
        # save file to server
        directory = "./train-data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(f"{directory}/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        namespace = "goldrace"
        
        # add training file
        if extension == ".csv":
            train_csv(file.filename, namespace)
        elif extension == ".pdf":
            train_pdf(file.filename, namespace)
        elif extension == ".txt":
            train_txt(file.filename, namespace)
        elif extension == ".docx":
            train_ms_word(file.filename, namespace)
        print("end-training")
        # add_file(file.filename)
    except Exception as e:
        print("training error(Invalid File Type!)")
        print(e)
        raise HTTPException(
            status_code=500, detail=e)