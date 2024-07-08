from dotenv import load_dotenv
import os
from openai import OpenAI
import tiktoken
import time
import json
import sys
from datetime import datetime, timedelta
from app.Models.ChatLog_Model import find_messages_by_id, add_new_message, Message, find_summary_by_id, save_summary_in_db
from app.Utils.Pinecone import get_context

load_dotenv()

client = OpenAI()

def answer_question(msg: str):
    # log_id = "goldrace"
    # final = ""
    
    # context = get_context(msg, log_id)
    
    # print("context: ", context)
    
    # saved_messages = find_messages_by_id(log_id)
    
    instructor = f"""
        You will act as a kind assistant.
        Please answer within 180 characters.
    """
    
    # messages = [{'role': message.role, 'content': message.content}
    #             for message in saved_messages[-3:]]
    
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {'role': "system", "content": instructor},
                {'role': "user", "content": msg}    
            ],
            max_tokens=3000,
            # stream=True
        )
        print("response: ", response)
        return response.choices[0].message.content
        # for chunk in response:
        #     print("chunk: ", chunk)
        #     if chunk.choices[0].delta.content != None:
        #         string = chunk.choices[0].delta.content
        #         yield string
                # final += string
        
    except Exception as e:
        print(e)
        
    
    # add_new_message(logId=log_id, msg=Message(content=msg, role="user"))
    # add_new_message(logId=log_id, msg=Message(content=final, role="assistant"))
    
    
def transcribe_audio(filename):
    audio_file= open(f"data/{filename}", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        language="az"
    )
    print(transcription.text)
    return transcription.text