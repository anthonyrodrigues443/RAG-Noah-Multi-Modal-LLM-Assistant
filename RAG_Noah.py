import time
# from audio_recorder_streamlit import audio_recorder
# import assemblyai as aai
from streamlit_mic_recorder import speech_to_text
import pyaudio
import cv2
import streamlit as st
import pyttsx3
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

st.set_page_config(page_title='Smart glasses', page_icon=':👓:')

@st.cache_data(show_spinner=False)
def pdf_reader(pdfs):
    text = ''''''
    no_of_pgs = list()
    for pdf in pdfs:
        reader = PdfReader(pdf)
        no_of_pgs.append(len(reader.pages))
        for page in range(no_of_pgs[-1]):
            pg = reader.pages[page]
            text += pg.extract_text()
    return text, sum(no_of_pgs)

@st.cache_data(show_spinner=False)
def get_text_chunks(text):
    max_tokens = 1024
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=max_tokens,
        chunk_overlap=max_tokens//4,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

@st.cache_resource(show_spinner=False)
def get_vectorstore(chunks):
    ini = time.time()
    embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
    print('embeddings : ', time.time()-ini)
    ini = time.time()
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    print('vectorstore : ', time.time()-ini)
    return vectorstore


def check_audio_device():
    p = pyaudio.PyAudio()
    try:
        p.get_default_input_device_info()
        return True
    except Exception as ex:
        print(ex)
        return False
    finally:
        p.terminate()


# def speech_to_text():    #STEP 1 : User speech to text with mic
#     text = speech_to_text()
#     return text
    # FILE_URL = 'audiofiles_RAGNoah/input_speech.mp3'

    # with open(FILE_URL, "wb") as f:
    #     f.write(audio_bytes_)

    # aai.settings.api_key = st.secrets["AAI_API_KEY"]

    # transcriber = aai.Transcriber()
    # transcript = transcriber.transcribe(FILE_URL)

    # if transcript.status == aai.TranscriptStatus.error:
    #     return None
    # else:
    #     return transcript.text


@st.cache_resource(show_spinner=False)
def get_cap():
    return cv2.VideoCapture(0)

def speak_text(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 120)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def clear_history():
    clear_hist = st.sidebar.button('Clear history', use_container_width=True, type='primary')
    if clear_hist :
        st.session_state.messages.clear()
        st.sidebar.markdown('<h1><center>History cleared</center></h1>', 
                            unsafe_allow_html=True)

st.header('RAG Noah :eyeglasses: ')

st.markdown(
    """
    <style>
    .st-emotion-cache-cnbvxy li{
        font-size: 1.25rem;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    [data-testid="stChatMessageContent"] * {
        font-size: 1.25rem;
        padding: 1px;
        margin: 0px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    [data-testid="chatAvatarIcon-user"] 
    <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
    </style>
    """, unsafe_allow_html=True
)

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

user_avatar_path = "imagefiles/user_avatar.png"
assistant_avatar_path = "imagefiles/assistant_avatar.png"

def main():
    with st.sidebar:
        st.markdown('<h1><center>Your docs </h1></center>', unsafe_allow_html=True)
        files = st.file_uploader(label="Upload docs",accept_multiple_files=True,
                label_visibility='hidden')
        if st.button('Process', use_container_width=True, type='primary'):
            if len(files) == 0:
                st.markdown('<h1><center>No file detected', unsafe_allow_html=True)
            else : 
                with st.spinner("Processing"):
                    raw_text, no_of_pgs = pdf_reader(files)
                    print('PDF Read')
                    text_chunks = get_text_chunks(raw_text)
                    print('Extracted text chunks')
                    stime = time.time()
                    vector_store = get_vectorstore(text_chunks)
                    etime = time.time()
                    print('Vectorstore Generated', 'Time taken : ',etime-stime)
                    st.header('Your file has been processed.')
                    return vector_store

if __name__ == '__main__':
    vec_store = main()
    if vec_store is not None:
        st.session_state.vec_store = vec_store
    clear_history()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if 'start_func' not in st.session_state:
        st.session_state.start_func = False

    def callback():
        st.session_state.start_func = True

    for message in st.session_state.messages:
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

        with c2 :
            text = speech_to_text("start", "stop")
            # audio_bytes = audio_recorder(
            #     text=" ",
            #     pause_threshold=2,  # Allow up to 2 seconds of silence
            #     recording_color="#e8b62c",
            #     neutral_color="#6aa36f",
            #     icon_name="microphone",
            #     icon_size="2x"
            #     )
    query = st.chat_input(placeholder='Message Noah')
    import txt_detection
    cap = get_cap()
    import ans_groq

    # if audio_bytes:
    #     with st.sidebar:
    #         with st.spinner('Transcribing Text'):
    #             text = speech_to_text(audio_bytes)
    #             if text == None:
    #                 st.sidebar.write('Some error encountered please try again...')

    if cam or st.session_state.start_func:
        # st.write('Working on this feature will be available soon.')
        text = txt_detection.text_extraction(cap)
        st.session_state.start_func = False
        if text == 'No text detected' :
            text = None

    if text:
        query = text

    vec_store = st.session_state.get('vec_store')
    try:
        formatted_query = ''
        if query:
            formatted_query = query.replace('\n', '\n\n')
            with st.chat_message('user', avatar=user_avatar_path):
                st.markdown(formatted_query)

            with st.spinner('Extracting information from documents'):
                chunks_ = vec_store.similarity_search(query=formatted_query)

            rel_chunks = ''
            for i in range(len(chunks_)):
                rel_chunks = rel_chunks + f'Context {i+1}: ' + chunks_[i].page_content

            st.session_state.messages.append({"role": "user", "content": query})
            file_num = len(st.session_state.messages)
            with st.chat_message(name='assistant', avatar=assistant_avatar_path):
                response = st.write_stream(ans_groq.RAG_Groq_ans(st.session_state.messages, rel_chunks, query))
                speak_text(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as ex:
        st.markdown('<h4><font color="yellow"><center>Submit the Context doc first.', unsafe_allow_html=True)

