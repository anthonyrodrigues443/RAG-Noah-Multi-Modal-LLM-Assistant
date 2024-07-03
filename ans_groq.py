from groq import Groq
import time
import streamlit as st
import re


GROQ_API_KEYS = [st.secrets['GROQ_API_KEY1'], st.secrets['GROQ_API_KEY2'],
                 st.secrets['GROQ_API_KEY3'], st.secrets['GROQ_API_KEY4'],
                 st.secrets['GROQ_API_KEY5']]

def Groq_ans(query): #STEP 2 : User prompt response in text
    client = Groq(api_key=GROQ_API_KEYS[0])
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


def RAG_Groq_ans(chat_history, context_chunks, query, query_num): #STEP 2 :User prompt response in text
    query_num = query_num%5

    client = Groq(api_key=GROQ_API_KEYS[query_num])
    prompt = f"""
You are an AI assistant with access ONLY to the information provided below. You MUST NOT use any external knowledge.

Chat History:
{chat_history}

Context:
{context_chunks}

STRICT CRUCIAL INSTRUCTIONS:
1. ONLY use the information from the Chat History and Additional Context to answer the question.
2. If the question CANNOT be answered using ONLY the provided information, your response MUST be:
   "I don't have enough information in the given context to answer this question."
3. DO NOT use any external knowledge or make any assumptions.
4. If the question is completely unrelated to the context, respond with:
   "The question is unrelated to the information I have. I can only answer questions about the topics in the given context."
5. NEVER answer questions about general knowledge, current events, or any topic not explicitly covered in the provided context.
6. If asked about your capabilities or the source of your information, only refer to the given context.

Current Question: {query}

Answer (remember, ONLY use the provided information):
"""
    chat_completion = client.chat.completions.create(    
        messages=[
            {
                "role": "user",
                "content": f"Context :{prompt}",
            }
        ],
        model='mixtral-8x7b-32768',
    )
    response = chat_completion.choices[0].message.content

    tokens = re.findall(r'\S+|\n|\t', response)

    for word in tokens:
        yield word + " "
        time.sleep(0.002)
        

