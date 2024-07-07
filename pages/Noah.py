# import streamlit as st
# st.markdown(
#     '<h1><font color="yellow"><center>Developer is currently working on Noah', unsafe_allow_html=True)

# st.markdown(
#     '<hr><h3>Vision of Noah 🎯 <br><br>  📌To have Real Time Computer Vision capabilities along with GPT. <br>📌To be integrated in AR glasses ',
#       unsafe_allow_html=True)


# st.sidebar.markdown('<h1><center>Connect with developer', unsafe_allow_html=True)

# style_image_dp = """
#     max-width: 150px;
#     height: auto;
#     max-height: 150px;
#     display: block;
#     margin-left: auto;
#     margin-right: auto;
#     border-radius: 50%;
# """


# st.sidebar.markdown(
#     f'<img src="{"https://media.licdn.com/dms/image/D4E03AQGREUZ3djPpog/profile-displayphoto-shrink_400_400/0/1685977776362?e=1724889600&v=beta&t=16HVxWzwc5clVOIpWqIqgq6FuTPViYf-g2hZPAmZuyc"}" style="{style_image_dp}">',
#     unsafe_allow_html=True)

# git = st.sidebar.link_button('Github', 'https://github.com/Sharkytony', type='primary', use_container_width=True)


# st.sidebar.link_button('LinkedIn', 'https://linkedin.com/in/anthonyrodrigues443', type='primary', use_container_width=True)

import time
initial = time.time()
import cv2
import streamlit as st
from gtts import gTTS
import vision
import base64
import warnings
import sim
from streamlit_mic_recorder import speech_to_text
import io
print('total Time taken for imports : ',time.time()- initial)

warnings.filterwarnings('ignore')

@st.cache_resource(show_spinner=False)
def get_cap():
    return cv2.VideoCapture(0)

def text_to_speech(text):
    tts = gTTS(text=text, lang='en', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

def autoplay_tts(audio_bytes, autoplay=True):
    if st.session_state.current_audio:
        st.session_state.current_audio.empty()
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
        <audio autoplay={autoplay} class="stAudio">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3" format="audio/mpeg">
        </audio>
        """
    st.session_state.current_audio = st.markdown(md, unsafe_allow_html=True)
    return st.session_state.current_audio

def clear_history():
    clear_hist = st.sidebar.button('Clear history', use_container_width=True, type='primary')
    if clear_hist :
        st.session_state.messages_1.clear()
        st.session_state.messages_2.clear()
        st.sidebar.markdown('<h1><center>History cleared</center></h1>', 
                            unsafe_allow_html=True)
        
results = {}

# Wrapper function to store the result of the target function
def thread_wrapper(func, key):
    results[key] = func()

def handling_required_operations(query, prev_response, caps):
    seq_op = dict()

    for line in prev_response.splitlines():
        if sim.has_letters_and_numbers(line):
            seq_op[line[0]] = line

    for value in seq_op.values():
        if 'yes' in value.lower():
            # object_detection_result, hand_tracking_result =  vision.run_concurrently(caps)
            object_detection_result = vision.object_detection(caps)
            hand_tracking_result = vision.hand_tracking(caps)
            observations_summary = f'''Suppose you have ability to access the camera and when the Question(mentioned below) was asked you opened the camera and took the observations. Observations :\n{object_detection_result}\n{hand_tracking_result}. \nBased on all the observations mentioned above try to prepare the response only for the asked question(Important Instructions : 1.Dont unnecessarily state down all the observations 2.If the question is about the chat history observations answer accordingly you dont have to answer with current observations when the question is about previous observations ).\n Question : {query}'''
            return observations_summary

        elif 'no' in value.lower():
            return "Question : " + query

# with st.sidebar:
#     model = st.radio(label="Select model", 
#     options=['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it'])
#     if model:
#         clear_history()

st.set_page_config(page_title='Smart glasses', page_icon=':👓:')
st.header('Noah :eyeglasses: ')

st.markdown(
    """
    <style>
    [data-testid="stChatMessageContent"] *{
        font-size: 1.25rem;
        padding: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .st-emotion-cache-ul70r3 li{
        font-size: 1.25rem;
    }
    </style>
    """, unsafe_allow_html=True)

#user text styling
st.markdown(
    """
<style>
    .st-emotion-cache-janbn0 {
        text-align: left;
        background-color: #333333;
    }

</style>
""", unsafe_allow_html=True)

# assistant text styling
st.markdown(
    """
<style>
    .st-emotion-cache-4oy321 {
        text-align: left;
        background-color: #203354;
    }
</style>
""", unsafe_allow_html=True)

# avatar styling
st.markdown(
    """
<style>
    .st-emotion-cache-p4micv {
    height: 80px;
    width:  80px;
    }

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
<style>
    .st-emotion-cache-19rxjzo {
    position: fixed;
    top: 400px;
}
</style>
""", unsafe_allow_html=True)


user_avatar_path = "imagefiles/user_avatar.png"
assistant_avatar_path = "imagefiles/assistant_avatar.png"

if __name__ == '__main__':
    clear_history()
    query_number = 0
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    if "messages_1" not in st.session_state:
        st.session_state.messages_1 = []
    if "messages_2" not in st.session_state:
        st.session_state.messages_2 = []
    if 'start_func' not in st.session_state:
        st.session_state.start_func = False

    def callback():
        st.session_state.start_func = True

    for message in st.session_state.messages_1:
        if message['role'] == 'user' :
            with st.chat_message(message['role'], avatar=user_avatar_path):
                st.markdown(message['content'])
        if message['role'] == 'assistant' :
            with st.chat_message(message['role'], avatar=assistant_avatar_path):
                st.markdown(message['content'])
    text = None

    with st.sidebar:
        c1, c2 = st.columns(2)
        with c1 :
            cam = st.button('📸', help='Visual input', on_click=callback)
        with c2:
            transcribed_txt = speech_to_text("🎙️", "🟥",just_once=True)

    query = st.chat_input(placeholder='Message Noah')
    print('time for loading entire web page : ', time.time() - initial)

    ini = time.time()
    import txt_detection
    cap = get_cap()
    import ans_groq
    print('cv loading time : ', time.time()- ini)

    if transcribed_txt:
        text = transcribed_txt

    if cam or st.session_state.start_func:
        text = txt_detection.text_extraction(cap)
        st.session_state.start_func = False
        if text == 'No text detected' :
            text = None

    if text:
        query = text
        
    if query:
        query_number+=1
        with st.chat_message('user', avatar=user_avatar_path):
            st.write(query)

        st.session_state.messages_1.append({"role":"user","content":query})

        history_model1 = st.session_state.messages_1
        history_model2 = st.session_state.messages_2

        with st.chat_message(name='assistant', avatar=assistant_avatar_path):
            response = ans_groq.Noah_Groq1(history_model1, query, query_number)
            print(response)
            new_query = handling_required_operations(query, response, cap)
            st.session_state.messages_2.append({"role":"user","content":new_query})

            new_response = ans_groq.Noah_Groq2(history_model2, new_query, query_number)

            st.write(new_response)
            audio_file = text_to_speech(new_response)
            autoplay_tts(audio_file)

        st.session_state.messages_1.append({"role":"assistant","content":new_response})
        st.session_state.messages_2.append({"role":"assistant","content":new_response})

        st.sidebar.write(st.session_state.messages_2)
