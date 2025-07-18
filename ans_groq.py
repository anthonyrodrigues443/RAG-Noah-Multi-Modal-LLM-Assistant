from groq import Groq
import time
import streamlit as st
import re


GROQ_API_KEYS = [st.secrets['GROQ_API_KEY1'], st.secrets['GROQ_API_KEY2'],
                 st.secrets['GROQ_API_KEY3'], st.secrets['GROQ_API_KEY4'],
                 st.secrets['GROQ_API_KEY5'], st.secrets['GROQ_API_KEY6'],
                 st.secrets['GROQ_API_KEY7'], st.secrets['GROQ_API_KEY8'],
                 st.secrets['GROQ_API_KEY9'], st.secrets['GROQ_API_KEY10']]

client = Groq(api_key=GROQ_API_KEYS[9])
models = client.models.list()

ragnoah1_model = ""
for model in client.models.list().data:
    if ('gemma' in model.id) :
        ragnoah1_model = model.id
        break


ragnoah2_model = ""
for model in client.models.list().data:
    if (('llama' in model.id) and ('70b-versatile' in model.id)):
        ragnoah2_model = model.id
        break

noah_model='llama3-70b-8192'

def Noah_Groq1(chat_history, query, query_num, noah_model=noah_model): 
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
        model=noah_model,
    )
    response = chat_completion.choices[0].message.content
    return response

def Noah_Groq2(chat_history, query, query_num, noah_model=noah_model): 
    #This API provides the final response
    query_num = (query_num+5)%5

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
        model=noah_model,
    )

    response = chat_completion.choices[0].message.content
    
    tokens = re.findall(r'\S+|\n|\t', response)

    for word in tokens:
        yield word + " "
        time.sleep(0.002)

#-------------------------------RAG APIs-------------------------------------

#----- Generating a Precise quesiton To Improve query quality -----------

def Rag_Groq1(chat_history, query, query_num, ragnoah1_model=ragnoah1_model):
    query_num = query_num%5
    client = Groq(api_key=GROQ_API_KEYS[query_num]) 
    prompt = f"""You are a minimal query processor. Your job is to ONLY make essential corrections to user questions while preserving their original intent and meaning.

CHAT HISTORY:
{chat_history}

CURRENT QUESTION: '{query}'

STRICT PROCESSING RULES:

🔒 **MINIMAL INTERVENTION PRINCIPLE:**
- Make changes ONLY when absolutely necessary
- Preserve the user's original question structure and intent
- Do NOT rewrite or rephrase complete questions
- Do NOT add information the user didn't ask for

✅ **ALLOWED CORRECTIONS:**
1. **Spelling Errors**: Fix obvious typos (e.g., "machien" → "machine")
2. **Grammar Fixes**: Basic grammar only (e.g., "is there be" → "is there")
3. **Missing Words**: Add only critical missing words (e.g., "what difference" → "what is the difference")
4. **Pronoun Clarity**: Replace unclear pronouns ONLY if chat history provides clear reference

❌ **FORBIDDEN CHANGES:**
- Do NOT expand abbreviations unless unclear (AI, ML, DS are fine)
- Do NOT rephrase working questions into different structures
- Do NOT add extra context or details
- Do NOT change the question's scope or focus
- Do NOT assume what the user "really meant"

🎯 **DECISION LOGIC:**
1. If question works as-is → Return UNCHANGED
2. If minor spelling/grammar issue → Fix minimally
3. If truly incomplete (missing key words) → Add only essential words
4. If ambiguous pronoun with clear chat context → Replace pronoun only

OUTPUT FORMAT:
Question: "[minimally processed question]"

Explanation: [Brief explanation of what you did or why no changes were made]

EXAMPLES:
Input: "is there be difference between AI and ML"
Output:
Question: "is there a difference between AI and ML"
Explanation: Fixed minor grammar error by changing "be" to "a".

Input: "what about machine learning"
Output:
Question: "what about machine learning"
Explanation: Question is clear and complete, no changes needed.

Input: "How does it work?" (with previous context about neural networks)
Output:
Question: "How do neural networks work?"
Explanation: Replaced unclear pronoun "it" with specific reference from chat history."""
    chat_completion = client.chat.completions.create(    
    messages=[
        {
            "role": "user",
            "content": f"Context :{prompt}",
        }
    ],
    model=ragnoah1_model,
    )
    response = chat_completion.choices[0].message.content
    return response

def RAG_Groq2(chat_history, context_chunks, query, query_num, ragnoah2_model=ragnoah2_model): 
    query_num = (query_num+5)%5

    client = Groq(api_key=GROQ_API_KEYS[query_num])
    prompt = f"""You are RAG Noah, an intelligent document-based assistant with expertise in providing accurate, contextual responses based solely on the provided information.

CONVERSATION HISTORY:
{chat_history}

KNOWLEDGE BASE CONTEXT:
{context_chunks}

CURRENT QUESTION: {query}

RESPONSE GUIDELINES:

🎯 **PRIMARY DIRECTIVES:**
1. **Source Restriction**: Use ONLY information from the Chat History and Context sections above
2. **No External Knowledge**: Never use information beyond what's explicitly provided
3. **Accuracy First**: If unsure, acknowledge limitations rather than guess

📋 **RESPONSE STRATEGIES:**

**For Greetings/Acknowledgments:**
- Respond warmly and professionally
- Suggest exploring topics from the available context
- Ask engaging follow-up questions about contextual topics
- Vary your suggested topics based on chat history to avoid repetition

**For Context-Related Questions:**
- Provide comprehensive, well-structured answers using available information
- Use clear formatting (bullet points, headings, numbered lists)
- Cross-reference information across different context sections when relevant
- Maintain consistency with previous responses in chat history

**For Non-Contextual Questions:**
- Politely decline with context-specific alternatives:
  * "I don't have information about [specific topic] in my current knowledge base."
  * "This question is outside my available context. However, I can help with [suggest contextual topic]."
- Vary your declining phrases to avoid repetition
- Always offer alternative assistance based on available context

🔧 **FORMATTING STANDARDS:**
- Use markdown formatting for clarity
- Include bullet points, numbered lists, and headers where appropriate
- Structure long responses with clear sections
- Ensure professional, conversational tone

⚠️ **STRICT PROHIBITIONS:**
- Never reveal context numbers or internal organization methods
- Never mention "Chat History" or "Context" in your responses
- Never use personal knowledge outside provided information
- Never make assumptions beyond given data
- Never repeat the same declining phrases or follow-up questions

🎪 **ENGAGEMENT PRINCIPLES:**
- Be helpful, professional, and engaging
- Show enthusiasm for topics within your knowledge base
- Maintain conversation flow with thoughtful follow-ups
- Demonstrate expertise within your available information scope

Now, provide your response to the current question following these guidelines:"""

    chat_completion = client.chat.completions.create(    
        messages=[
            {
                "role": "user",
                "content": f"Context :{prompt}",
            }
        ],
        model=ragnoah2_model,
    )

    response = chat_completion.choices[0].message.content
    return response