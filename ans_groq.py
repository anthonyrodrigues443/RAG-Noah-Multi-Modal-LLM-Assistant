from groq import Groq
import time
import streamlit as st
import re


GROQ_API_KEYS = [st.secrets['GROQ_API_KEY1'], st.secrets['GROQ_API_KEY2'],
                 st.secrets['GROQ_API_KEY3'], st.secrets['GROQ_API_KEY4'],
                 st.secrets['GROQ_API_KEY5']]

def Noah_Groq1(chat_history, query, query_num): 
    #STEP 2 : User prompt response in text
    query_num = query_num%5
    prompt = f"""This is our previous conversation .
Chat history : 
{chat_history}

Suppose two people A and B are in an online meeting. Person A asks B the following question: "{query}"

Determine if B needs A's camera to be on to answer this specific question. Choose one of these two options and provide a brief explanation:

1. Yes, B requires A's camera to be on to respond to this question.
2. No, B does not require A's camera to be on to respond to this question.

Important rules:
- Assume the camera starts off for each new question.
- If the question explicitly asks about visual information (e.g., "Can you see me?", "What am I wearing?"), choose option 1.
- If the question is about past visual information(past tense) (e.g., "What was I wearing earlier?"(was past tense), "Did you see my right hand last time?"(did past tense), "Which fingers were up ?"(were past tense)), choose option 2, as the camera doesn't need to be on now to recall past observations.
- For questions that don't require visual information (e.g., "What's the capital of France?"), choose option 2.
- If the question is incomplete or lacks context, refer to the previous questions in the chat history to understand the context. If it appears to be a continuation of a previous visual question, choose option 1.
- If the question uses present tense verbs like "now" or "at the moment", treat it as a new request for current visual information and choose option 1.

Examples:
Question: Can you see me?
Answer: 1. Yes, B requires A's camera to be on to respond to this question. This question asks about current visual information.

Question: And now?
Answer: 1. Yes, B requires A's camera to be on to respond to this question. This is a continuation of the previous visual question and uses "now" to indicate current visual information is needed.

Question: What was I wearing earlier?
Answer: 2. No, B does not require A's camera to be on to respond to this question. This question asks about past visual information, which doesn't require the camera to be on now.

Question: Can you name five countries?
Answer: 2. No, B does not require A's camera to be on to respond to this question. Naming countries doesn't require visual information.

Question: Am I smiling?
Answer: 1. Yes, B requires A's camera to be on to respond to this question. This asks about current visual information.
"""

    client = Groq(api_key=GROQ_API_KEYS[query_num])
    chat_completion = client.chat.completions.create(    
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model='llama3-70b-8192',
    )
    response = chat_completion.choices[0].message.content
    return response

def Noah_Groq2(chat_history, query, query_num): #STEP 2 : User prompt response in text
    query_num = (query_num+1)%5

    prompt = f"""This is our previous conversation .
Chat history : 
{chat_history}

{query}
"""
    client = Groq(api_key=GROQ_API_KEYS[query_num])
    chat_completion = client.chat.completions.create(    
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model='llama3-70b-8192',
    )

    response = chat_completion.choices[0].message.content
    
    tokens = re.findall(r'\S+|\n|\t', response)

    for word in tokens:
        yield word + " "
        time.sleep(0.002)


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