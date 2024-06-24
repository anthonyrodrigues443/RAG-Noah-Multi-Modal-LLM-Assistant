from groq import Groq
from dotenv import load_dotenv
import time
import os
import re

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_KEY2 = os.getenv('GROQ_API_KEY2')

def Groq_ans(query): #STEP 2 : User prompt response in text
    client = Groq(api_key=GROQ_API_KEY2)
    chat_completion = client.chat.completions.create(    
        messages=[
            {
                "role": "user",
                "content": f"{query}",
            }
        ],
        model='llama3-70b-8192',
    )
    response = chat_completion.choices[0].message.content
    return response


def RAG_Groq_ans(chunks, query): #STEP 2 : User prompt response in text
    client = Groq(api_key=GROQ_API_KEY)
    chat_completion = client.chat.completions.create(    
        messages=[
            {
                "role": "user",
                "content": f"Context : {chunks}\n\n Based on the above context only provide the answer to the question below. If the question cannot be answered from the context your answer should always be saying not much information available about the specific topic in a polite manner. If you answer anything from outside what is provided in context i will pass away so please dont . \n\nQuestion : {query}",
            }
        ],
        model='mixtral-8x7b-32768',
    )
    response = chat_completion.choices[0].message.content
    print(f"Context : {chunks}\n\n Above is the Context given, you have to answer the question below only based on the context even the examples. If the question cannot be answered from the context your answer should always be saying not much information available about the specific topic in a polite manner. If you answer anything from outside what is provided in context i will pass away so please dont every bit of response should strictly be from the context provided . \n\nQuestion : {query}")

    for word in response.split(" "):
        yield word + " "
        time.sleep(0.002)
        

