import time
initial = time.time()
import streamlit as st
from streamlit_mic_recorder import speech_to_text
import cv2
import vision
from gtts import gTTS
import base64
import warnings
import io
print('total Time taken for imports : ',time.time()- initial)

warnings.filterwarnings('ignore')

#-------------------------Accessing Camera-----------------------------------
@st.cache_resource(show_spinner=False)
def get_cap():
    return cv2.VideoCapture(0)

@st.cache_resource(show_spinner=False)
def get_cap2():
    return cv2.VideoCapture(2)

#---------------- Checking response if CV is to be performed -------------------
def has_letters_and_numbers(s):
    has_letter = False
    has_digit = False

    for char in s:
        if char.isalpha():
            has_letter = True
        elif char.isdigit():
            has_digit = True
        
        # If both are found, short-circuit the loop
        if has_letter and has_digit :
            return True
    
    return False

#------------------ Autoplay Response to Speech ------------------------------
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

#-------------------------- Clear Chat history -------------------------------
def clear_history():
    clear_hist = st.sidebar.button('Clear history', use_container_width=True, type='primary')
    if clear_hist :
        st.session_state.messages_1.clear()
        st.session_state.messages_2.clear()
        st.sidebar.markdown('<h1><center>History cleared</center></h1>', 
                            unsafe_allow_html=True)
        

#---------------- Performing required operations as per response ---------------
def handling_required_operations(query, prev_response, caps):
    seq_op = dict()

    for line in prev_response.splitlines():
        if has_letters_and_numbers(line):
            seq_op[line[0]] = line

    for value in seq_op.values():
        if 'yes' in value.lower():
            object_detection_result, hand_tracking_result =  vision.run_concurrently(caps)
            # object_detection_result = vision.object_detection(caps)
            # hand_tracking_result = vision.hand_tracking(caps)
            observations_summary = f'''Suppose you have ability to access the camera and when the Question(mentioned below) was asked you opened the camera and took the observations. Observations :\n{object_detection_result}\n{hand_tracking_result}. \nBased on all the observations mentioned above try to prepare the response only for the asked question(Important Instructions : 1.Dont unnecessarily state down all the observations 2.If the question is about the chat history observations answer accordingly you dont have to answer with current observations when the question is about previous observations ).\n Question : {query}'''
            return observations_summary

        elif 'no' in value.lower():
            return "Question : " + query


#------------------------------- Styling UI ----------------------------------
st.set_page_config(page_title='Smart glasses', page_icon=':👓:')
st.header('Noah :eyeglasses: ')

# font size
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

#user text bg
st.markdown(
    """
<style>
    .st-emotion-cache-janbn0 {
        text-align: left;
        background-color: #333333;
    }

</style>
""", unsafe_allow_html=True)

# assistant text bg
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

user_avatar_path = "imagefiles/user_avatar.png"
assistant_avatar_path = "imagefiles/assistant_avatar.png"

#---------------------------------- Running -----------------------------------
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
    cap2 = get_cap2()
    import ans_groq
    print('cv loading time : ', time.time()- ini)

    if transcribed_txt:
        text = transcribed_txt

    if cam or st.session_state.start_func:
        text = txt_detection.text_extraction(cap2)
        st.session_state.start_func = False
        if text == 'No text detected' :
            text = None

    if text:
        query = text
        
    if query:
        if st.session_state.current_audio:
            st.session_state.current_audio.empty()
            st.session_state.current_audio = None

        query_number+=1
        with st.chat_message('user', avatar=user_avatar_path):
            st.write(query)

        st.session_state.messages_1.append({"role":"user","content":query})

        history_model1 = st.session_state.messages_1
        history_model2 = st.session_state.messages_2

        with st.chat_message(name='assistant', avatar=assistant_avatar_path):
            response = ans_groq.Noah_Groq1(history_model1, query, query_number)
            print('\nResponse of LLM 1 : ', response)
            new_query = handling_required_operations(query, response, cap)
            st.session_state.messages_2.append({"role":"user","content":new_query})

            new_response = st.write_stream(ans_groq.Noah_Groq2(history_model2, new_query, query_number))

            audio_file = text_to_speech(new_response)
            autoplay_tts(audio_file)

        st.session_state.messages_1.append({"role":"assistant","content":new_response})
        st.session_state.messages_2.append({"role":"assistant","content":new_response})

        print('\n\n Chat history : ',st.session_state.messages_2)
