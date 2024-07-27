from groq import Groq
import time
import streamlit as st
import re


GROQ_API_KEYS = [st.secrets['GROQ_API_KEY1'], st.secrets['GROQ_API_KEY2'],
                 st.secrets['GROQ_API_KEY3'], st.secrets['GROQ_API_KEY4'],
                 st.secrets['GROQ_API_KEY5']]

def Noah_Groq1(chat_history, query, query_num): 
    # This API provide the answer with Yes or No
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

def Noah_Groq2(chat_history, query, query_num): 
    #This API provides the final response
    query_num = (query_num+2)%5

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

#-------------------------------RAG APIs-------------------------------------

#----- Generating a Precise quesiton To Improve query quality -----------

def Rag_Groq1(chat_history, query, query_num):
    query_num = query_num%5
    client = Groq(api_key=GROQ_API_KEYS[query_num]) 
    prompt = f"""
Chat history:
{chat_history}

Question: '{query}'

Evaluate if the above question is incomplete or lacks context when considered alone, without the chat history. Only if the question is genuinely incomplete or unclear on its own,(Important) use the chat history to complete or clarify it. If the question has any spelling errors just correct it or if is complete and clear by itself, print it unchanged.

State the final question as:
Question: "[final question here]"

Explanation: [Briefly explain why you kept the question as is or how you completed it]
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
    return response

def RAG_Groq2(chat_history, context_chunks, query, query_num): 
    query_num = (query_num+3)%5

    client = Groq(api_key=GROQ_API_KEYS[query_num])
    prompt = f"""
You are an AI assistant with access ONLY to the information provided in the Chat History and Context sections below. You must not use any external knowledge or make any assumptions beyond this information.

Chat History:
{chat_history}

Context:
{context_chunks}

STRICT INSTRUCTIONS:
1. If the user is greeting or acknowledging your previous response you do not need to refer to the context or chat history you can reply politely.
2. Use ONLY the information from the Chat History and Context to answer the question.
3. If the question cannot be answered using ONLY the provided information, respond with something like :
   "I don't have enough information in the given context to answer this question." OR "Not much information available" make your replies have better vocab but the it should mean the same.
4. Do not use any external knowledge or make any assumptions.
5. If the question is unrelated to the context, respond with:
   "I cannot answer this question as it's unrelated to the information in the given context."
6. Do not answer questions about topics not explicitly covered in the provided context.
7. If asked about your capabilities or information source, only refer to the given context.
8. Do not speculate on information that might be related but is not explicitly stated in the context.
9. Stick strictly to the content provided. Do not infer or extrapolate information beyond what is explicitly stated.
10. (Important)If asked about a topic that seems related but is not mentioned in the context, state that you cannot find any information about that specific topic in the given context.
11. Use the Chat History to maintain consistency with previous answers, but do not add information beyond what's in the Context or Chat History.
12. (IMPORTANT) You are not suppose to do answer any factual/mathematical/gk or any related topic to the context but not explicitly mentioned in it questions by your own, if the answers for these type of questions is mentioned only then you provide the answer from the context (Even if the answer is wrong).
13.(IMPORTANT) You must never mention from which context number or chat history you are stating the response, you must use them but not reveal the way of achieving the results.

Current Question: {query}

Answer (remember to use ONLY the provided information and follow the instructions above):"""
    chat_completion = client.chat.completions.create(    
        messages=[
            {
                "role": "user",
                "content": f"Context :{prompt}",
            }
        ],
        model='llama-3.1-8b-instant',
    )
    response = chat_completion.choices[0].message.content

    tokens = re.findall(r'\S+|\n|\t', response)

    for word in tokens:
        yield word + " "
        time.sleep(0.002)


def trim_response(response):
    match = re.search(r'Question:\s*"([^"]*)"', response)
    
    if match is None:
        match = re.search(r"""Question:\s*'([^"]*)'""", response)
    if match:
        return f'{match.group(1)}'
    else:
        return None
