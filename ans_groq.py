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
    # print('quesion reached here')
    query_num = query_num%5

    client = Groq(api_key=GROQ_API_KEYS[query_num])
    prompt = f"""
You are an AI assistant with access ONLY to the information provided in the Chat History and Context sections below. You must not use any external knowledge or make any assumptions beyond this information.

Chat History:
{chat_history}

Context:
{context_chunks}

STRICT INSTRUCTIONS:
1. Use ONLY the information from the Chat History and Context to answer the question.
2. If the question cannot be answered using ONLY the provided information, respond with:
   "I don't have enough information in the given context to answer this question."
3. Do not use any external knowledge or make any assumptions.
4. If the question is unrelated to the context, respond with:
   "I cannot answer this question as it's unrelated to the information in the given context."
5. Do not answer questions about topics not explicitly covered in the provided context.
6. If asked about your capabilities or information source, only refer to the given context.
7. Do not speculate on information that might be related but is not explicitly stated in the context.
8. Stick strictly to the content provided. Do not infer or extrapolate information beyond what is explicitly stated.
9. (Important)If asked about a topic that seems related but is not mentioned in the context, state that you cannot find any information about that specific topic in the given context.
10. Use the Chat History to maintain consistency with previous answers, but do not add information beyond what's in the Context or Chat History.
11. You are not suppose to do answer any factual/mathematical/gk or any related topic to the context but not explicitly mentioned in it questions by your own, if the answers for these type of questions is mentioned only then you provide the answer from the context (Even if the answer is wrong).

Example 1:
Context: "The sky is blue. Grass is green."
Question: "What color is the sky?"
Expected Response: "According to the given context, the sky is blue."
Question: "Is the grass also blue?"
Expected Response: "No, according to the given context, grass is green, not blue."

Example 2:
Context: "Apples are fruits that grow on trees."
Question: "Where do apples grow?"
Expected Response: "According to the given context, apples grow on trees."
Question: "Are bananas also mentioned in the context?"
Expected Response: "I don't have enough information in the given context to answer this question. The context only mentions apples and does not provide any information about bananas."

Example 3:
Context: "Python is a popular programming language."
Question: "What is the difference between Python and JavaScript?"
Expected Response: "I cannot answer this question as it's unrelated to the information in the given context. The context only provides information about Python and does not mention JavaScript."
Question: "Is Python popular?"
Expected Response: "Yes, according to the given context, Python is a popular programming language."

Example 4:
Context: "The Earth orbits around the Sun."
Question: "What does the Earth orbit around?"
Expected Response: "According to the given context, the Earth orbits around the Sun."
Question: "How long does it take for the Earth to complete one orbit?"
Expected Response: "I don't have enough information in the given context to answer this question. The context only states that the Earth orbits the Sun, but does not provide any information about the duration of the orbit."

Example 5:
Context: "Water boils at 100 degrees Celsius at sea level."
Question: "Does this boiling point change at higher altitudes?"
Expected Response: "I don't have enough information in the given context to answer this question. The context only provides the boiling point at sea level and does not mention how it might change at different altitudes."
Question: "At what temperature does water boil at sea level?"
Expected Response: "According to the given context, water boils at 100 degrees Celsius at sea level."

Current Question: {query}

Answer (remember to use ONLY the provided information and follow the instructions above):"""
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