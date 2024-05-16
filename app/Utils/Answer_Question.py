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
    log_id = "goldrace"
    final = ""
    
    context = get_context(msg, log_id)
    
    print("context: ", context)
    
    msg += f"""
        In responding to user queries, please follow these refined guidelines:

        Integrate the provided context into your responses as if it is part of your natural knowledge base.
        Convey a sense of familiarity with the subject matter, refraining from phrases that suggest you are referencing an external context.
        Avoid overtly acknowledging the use of a reference text within your responses.
        Use the context to inform your responses to complex or detailed inquiries where the context is applicable and relevant.
        For straightforward queries that do not require context (such as simple greetings or basic questions), provide a direct and concise reply without referencing the context.
        Exercise discernment to determine when to draw from the context, ensuring that your responses are both relevant and informative without overloading simple exchanges with unnecessary detail.
        Below is the context which should be subtly woven into your answers when appropriate:
        ---------------
        {context}
    """
    
    saved_messages = find_messages_by_id(log_id)
    
    instructor = f"""
        You will act as a kind assistant.
    """
    
    messages = [{'role': message.role, 'content': message.content}
                for message in saved_messages[-3:]]
    
    messages.append({
        "role": "user",
        "content": [
            {"type": "text", "text": msg},
            # {
            # "type": "image_url",
            # "image_url": {
            #     "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            # },
            # },
        ],
    })
    messages.insert(0, {'role': 'system', 'content': instructor})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=3000,
            stream=True
        )
        # print(response)
        for chunk in response:
            if chunk.choices[0].delta.content != None:
                string = chunk.choices[0].delta.content
                yield string
                final += string
        print(final)
    except Exception as e:
        print(e)
        
    
    add_new_message(logId=log_id, msg=Message(content=msg, role="user"))
    add_new_message(logId=log_id, msg=Message(content=final, role="assistant"))