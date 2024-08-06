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

Evaluate if the above question is incomplete or lacks context when considered alone, without the chat history. Only if the question is genuinely incomplete or unclear on its own,(Important) use the chat history to complete or clarify it. If the question has any spelling errors just correct it or if is complete and clear by itself, print it unchanged. You are not supposed to answer the question.

State your response in this template only:
Question: "final complete question here"

Explanation: [Briefly explain why you kept the question as is or how you completed it]

(Your template must contain only these two things nothing other than this and in the same format as well)
Example responses:
Example 1 - 
Question: "-----------"

Explanation: ------------------.

Example 2 -
Question: "--------------------------"

Explanation: ---------------------------------.
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
1.Only If the user is greeting or acknowledging your previous response you do not need to refer to the context or chat history, you should reply politely  and end your responses with questions like would you like to know about this topic (from any topic provided in the context but never repeat the same questions in your responses, you can use the chat history to refer to previous questions you gave).
2. Use ONLY the information from the Chat History and Context to answer the question, do not use any external knowledge or make any assumptions.
3. Do not to answer any factual/mathematical/gk or any related topic to the context but not explicitly mentioned.
4. Do not ever mention from which context number or chat history you are stating the response, you must use them but not reveal the way of achieving the results.
5. Do not tell what is given in the context until is asked for .
6. If the question is irrelevant to the context and chat history, and cannot be answered using ONLY the provided information, respond with phrases like :
    A. "I don't have enough information in the given context to answer this topic(here the topic should be replace by the non contextual question of user)"
    or  
    B. "I cannot answer this question as it's unrelated to the information in the given context."
and if you use one of this then in next response where you cannot answer then use different option .
7. If asked about your capabilities or information source, only refer to the given context.
8. Use the Chat History to maintain consistency with previous answers, but do not add information beyond what's in the Context or Chat History.
9. Use clean formatting(tabs/new lines/indentation/bullet points)on your responses.
10. Never use your knowledge base to answer any question .

Current Question: {query}

Answer (remember to use ONLY the provided information and follow the instructions above):"""
    chat_completion = client.chat.completions.create(    
        messages=[
            {
                "role": "user",
                "content": f"Context :{prompt}",
            }
        ],
        model='llama-3.1-70b-versatile',
    )
    response = chat_completion.choices[0].message.content

    tokens = re.findall(r'\S+|\n|\t', response)

    for word in tokens:
        yield word + " "
        time.sleep(0.002)