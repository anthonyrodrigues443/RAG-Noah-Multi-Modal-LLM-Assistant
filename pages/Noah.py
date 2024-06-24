import streamlit as st
st.markdown('<h1><font color="yellow"><center>Developer is currently working on it', unsafe_allow_html=True)

st.markdown('<h2><center>Connect with developer : ', unsafe_allow_html=True)

st.image('imagefiles/github_logo.png')

# import cv2
# import speech_recognition as sr
# import streamlit as st
# from gtts import gTTS
# import pygame
# import os
# import vision
# import warnings
# import sim
# from dotenv import load_dotenv
# load_dotenv()

# GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# warnings.filterwarnings('ignore')

# def rec_n_ret():    #STEP 1 : User speech to text with mic
#     r = sr.Recognizer()
#     try:
#         with sr.Microphone() as source2:
#             r.adjust_for_ambient_noise(source2, duration=0.2)
#             temp2 = r.listen(source2)
#             MyText = r.recognize_google(temp2)
#             MyText = MyText.lower()
#             return MyText
            
#     except sr.RequestError as e:
#         MyText = f"Could not request results; {e}"
#         st.write(MyText+' could you please repeat ?')
#         return None

#     except sr.UnknownValueError:
#         MyText = "unknown error occurred"
#         st.write(MyText+' could you please repeat ?')
#         return None

# @st.cache_resource(show_spinner=False)
# def get_cap():
#     return cv2.VideoCapture(0)

# def llm_working(query): #STEP 2 : User prompt response in text
#     client = Groq(api_key=GROQ_API_KEY)
#     chat_completion = client.chat.completions.create(    
#         messages=[
#             {
#                 "role": "user",
#                 "content": f"{query}",
#             }
#         ],
#         model='llama3-70b-8192',
#     )
#     response = chat_completion.choices[0].message.content
#     return response

# # Initialize pygame mixer
# pygame.mixer.init()

# # Function to convert text to speech and save as audio file with Indian accent
# def text_to_speech(text, num):
#     tts = gTTS(text=text, lang='en')
#     audio_file = f'audiofiles_Noah/resp{num}.mp3'
#     tts.save(audio_file)
#     return audio_file

# # Function to play audio
# def play_audio(file):
#     pygame.mixer.music.load(file)
#     pygame.mixer.music.play()

# # Function to stop audio
# def stop_audio():
#     pygame.mixer.music.stop()


# def clear_history():
#     clear_hist = st.sidebar.button('Clear history', use_container_width=True, type='primary')
#     if clear_hist :
#         st.session_state.messages_1.clear()
#         st.session_state.messages_2.clear()
#         st.sidebar.markdown('<h1><center>History cleared</center></h1>', 
#                             unsafe_allow_html=True)
        
# results = {}

# # Wrapper function to store the result of the target function
# def thread_wrapper(func, key):
#     results[key] = func()

# def handling_required_operations(query, prev_response, caps):
#     seq_op = dict()

#     for line in prev_response.splitlines():
#         if sim.has_letters_and_numbers(line):
#             seq_op[line[0]] = line

#     for value in seq_op.values():
#         if 'yes' in value.lower():
#             # object_detection_result, hand_tracking_result =  vision.run_concurrently(caps)
#             object_detection_result = vision.object_detection(caps)
#             hand_tracking_result = vision.hand_tracking(caps)
#             observations_summary = f'''Suppose you have ability to access the camera and when the Question(mentioned below) was asked you opened the camera and took the observations. Observations :\n{object_detection_result}\n{hand_tracking_result}. \nBased on all the observations mentioned above try to prepare the response only for the asked question(Important Instructions : 1.Dont unnecessarily state down all the observations 2.If the question is about the chat history observations answer accordingly you dont have to answer with current observations when the question is about previous observations ).\n Question : {query}'''
#             return observations_summary

#         elif 'no' in value.lower():
#             return "\nQuestion : "+query

# # with st.sidebar:
# #     model = st.radio(label="Select model", 
# #     options=['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it'])
# #     if model:
# #         clear_history()

# st.set_page_config(page_title='Smart glasses', page_icon=':👓:')
# st.header('Noah :eyeglasses: ')

# st.markdown(
#     """
#     <style>
#     [data-testid="stChatMessageContent"] *{
#         font-size: 1.25rem;
#         padding: 1px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# st.markdown(
#     """
#     <style>
#     .st-emotion-cache-ul70r3 li{
#         font-size: 1.25rem;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# #user text styling
# st.markdown(
#     """
# <style>
#     .st-emotion-cache-janbn0 {
#         text-align: left;
#         background-color: #333333;
#     }

# </style>
# """, unsafe_allow_html=True)

# # assistant text styling
# st.markdown(
#     """
# <style>
#     .st-emotion-cache-4oy321 {
#         text-align: left;
#         background-color: #203354;
#     }
# </style>
# """, unsafe_allow_html=True)

# # avatar styling
# st.markdown(
#     """
# <style>
#     .st-emotion-cache-p4micv {
#     height: 80px;
#     width:  80px;
#     }

# </style>
# """, unsafe_allow_html=True)

# st.markdown(
#     """
# <style>
#     .st-emotion-cache-19rxjzo {
#     position: fixed;
#     top: 400px;
# }
# </style>
# """, unsafe_allow_html=True)


# user_avatar_path = "imagefiles/user_avatar.png"
# assistant_avatar_path = "imagefiles/assistant_avatar.png"

# if __name__ == '__main__':
#     clear_history()
#     captures = vision.setup_cam()

#     if "messages_1" not in st.session_state:
#         st.session_state.messages_1 = []
#     if "messages_2" not in st.session_state:
#         st.session_state.messages_2 = []


#     for message in st.session_state.messages_1:
#         if message['role'] == 'user' :
#             with st.chat_message(message['role'], avatar=user_avatar_path):
#                 st.markdown(message['content'])
#         if message['role'] == 'assistant' :
#             with st.chat_message(message['role'], avatar=assistant_avatar_path):
#                 st.markdown(message['content'])

#     with st.sidebar:
#         c1, c2 = st.columns(2)
#         with c2:
#             record = st.button('🎙️')
#         with c1:
#             cam = st.button('📸')
#     query = st.chat_input(placeholder='Message Noah')
#     import txt_detection
#     cap = get_cap()
#     import ans_groq

#     text = None

#     if record:
#         with st.spinner('Listening...'):
#             text = rec_n_ret()

#     if cam :#or st.session_state.start_func
#         st.sidebar.markdown('<h3><font color="yellow"><a href="https://github.com/Sharkytony">Developer</a> is currently working on it</font></h3>', unsafe_allow_html=True, help='Anthony Rodrigues')
#         # text = txt_detection.text_extraction(cap)
#         # st.session_state.start_func = False
#         # if text == 'No text detected' :
#         #     text = None
    
#     if text:
#         query = text

#     if query:
#         with st.chat_message('user', avatar=user_avatar_path):
#             st.write(query)

#         st.session_state.messages_1.append({"role":"user","content":query})
#         file_num = len(st.session_state.messages_1)
#         context_info =" This is our previous conversation\nChat history : "

#         context_chunk = st.session_state.messages_1
#         context_chunk_2 = st.session_state.messages_2

#         additional_context_info = f''' Suppose two people A and B are in an online meeting . Person A asks B Question : "{query}" so will B essentially require A's camera to be on to be able to answer the question (You can only answer from either of the two options and then state the reson  1.Yes B will require A's camera to be on to respond to this question 2.No B will not require A's camera to be on to respond to this question) .If you cannot make sense of the question or believe it is incomplete or lacks context you can refer to the previous questions from the chat history and remember if you believe it is continuation of previous question your response should always be option 1 that is Yes.(Keep in memory that after each question the camera is turned off so for each question dont think the camera is on so why will B need to turn the camera to be on when it is already on)
        
#         Example 1:
#         Question : Can you see me
#         Answer : Yes..(continued with option 1)
        
#         Question : And now
#         Answer : Yes..(continued with option 1) Because reffered to previous one
         
#         Question : And how about now
#         Answer : Yes..(continued with option 1) Because reffered to prev one and that reffers to prev one
         
#         Question : Can you name five countries
#         Answer : No..(continued with option 2) Because you dont need to look at A to name 5 countries

#         Question : again
#         Answer : No..(continued with option 2)Because reffered to previous one '''

# # (You can answer only one of the two options 1) yes the camera the camera needs to be on. 2) no the camera doesnt require to be on.).

#         query_for_ans_sel_model = context_info + str(context_chunk) + additional_context_info

#         with st.chat_message(name='assistant', avatar=assistant_avatar_path):
#             response = llm_working(query_for_ans_sel_model)
#             new_query = handling_required_operations(query, response, captures)
#             st.session_state.messages_2.append({"role":"user","content":new_query})
#             query_for_ans_model = context_info + str(context_chunk_2)+" Remember never mention anything about or from the chat history unless asked for it"+ new_query 
#             print('Query for LLM 2 : ', query_for_ans_model)
#             new_response = ans_groq.Groq_ans(query_for_ans_model)

#             st.write(new_response)
#             audio_file = text_to_speech(new_response, file_num)
#             play_audio(audio_file)

#         st.session_state.messages_1.append({"role":"assistant","content":new_response})
#         st.session_state.messages_2.append({"role":"assistant","content":new_response})

#         st.sidebar.write(st.session_state.messages_2)

#         if os.path.exists(f'audiofiles/resp{file_num-2}.mp3'):
#             os.remove(f'audiofiles/resp{file_num-2}.mp3')