#----------------------------Importing Libraries-------------------------------

import time
initial = time.time()
import base64
from streamlit_mic_recorder import speech_to_text
import cv2
import streamlit as st
from PyPDF2 import PdfReader
import re
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import speech_recognition as sr
from gtts import gTTS
import io
import warnings
print('total Time taken for imports : ',time.time()- initial)

warnings.filterwarnings('ignore')



# ===========================RAG PIPELINE====================================

#----------------------------- Reading PDFs --------------------------------
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


#-------------------------Reading Webpages-----------------------------------

def clear_all_links():
    st.session_state.clear_links = True

def remove_single_link(index):
    if index < len(st.session_state.links_list):
        st.session_state.links_list.pop(index)

def start_processing():
    st.session_state.start_process = True

@st.cache_data(show_spinner=False)
def webpage_reader(links):
    if st.session_state.start_process:
        loader = WebBaseLoader(links)
        content = loader.load()
        content_str = ''.join(doc.page_content for doc in content)
        content_str = re.sub(r'(\n\s*)+\n+', '\n', content_str)
        st.session_state.start_process = False
        return content_str 

#----------------------- Extracting chunks --------------------------------
@st.cache_data(show_spinner=False)
def get_text_chunks(text):
    max_tokens = 1024
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n', ' '],
        chunk_size=max_tokens,
        chunk_overlap=max_tokens//4,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

#-----------------Generating Embeddings and Storing in VectorStore------------

@st.cache_resource(show_spinner=False)
def get_vectorstore(chunks):
    ini = time.time()
    embeddings = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1", model_kwargs={'trust_remote_code': True})
    print('embeddings : ', time.time()-ini)
    ini = time.time()
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    print('vectorstore : ', time.time()-ini)
    return vectorstore


#-------------------- Reading Camera for Text Extraction --------------------
@st.cache_resource(show_spinner=False)
def get_cap():
    return cv2.VideoCapture(0)

#----------------------- Autoplay Text to Speech ----------------------------
def text_to_speech(text):
    tts = gTTS(text=text, lang='en', tld='us',slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    audio_bytes = fp.getvalue()
    return audio_bytes

def autoplay_tts(audio_bytes, autoplay=True):
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
        <audio id="tts_audio" controls autoplay="{autoplay}">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    return st.markdown(md, unsafe_allow_html=True)

# -------------------------- Clear History Messages --------------------------
def clear_history():
    clear_hist = st.sidebar.button('Clear history', use_container_width=True, type='primary')
    if clear_hist :
        st.session_state.frontend_messages.clear()
        st.session_state.backend_messages.clear()
        st.sidebar.markdown('<h1><center>History cleared</center></h1>', 
                            unsafe_allow_html=True)

#-----------------------------Styling UI ------------------------------------
st.set_page_config(page_title='Smart glasses', page_icon=':👓:')
st.header("RAG Noah :eyeglasses: ", anchor=False)
st.markdown(" <h3>(Chat with PDF's📚 and Websites🌐)", unsafe_allow_html=True)


# Chat messages font size
st.markdown(
    """
    <style>
    [data-testid="stChatMessageContent"] * {
        font-size: 1.1rem;
        padding: 1px;
        margin: 0px;        
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .st-emotion-cache-cnbvxy li{
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True
)

#button size
st.markdown('''
<style>
button.myButton{
    font-size:200px !important;
    }
</style>
    ''',
    unsafe_allow_html=True)

#pdf docs styling
st.markdown(
    """
<style>
    .st-emotion-cache-13k62yr {
        color: rgb(0, 250, 250);
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

st.markdown(
    """
<style>
    .st-emotion-cache-1sno8jx li {
        font-size:1.1rem;
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

# removing send button to eliminate duplication

st.markdown(
    """
<style>
    .st-emotion-cache-1f3w014 {
    width:  0px;
    }

</style>
""", unsafe_allow_html=True)

user_avatar_path = "imagefiles/user_avatar.png"
assistant_avatar_path = "imagefiles/assistant_avatar.png"

#------------------------ Running of RAG ------------------------------------
def main(files, link):
    if link:
        if not link.startswith('https://'):
            link = 'https://' + link
        if link not in st.session_state.links_list:
            st.session_state.links_list.append(link)
    if len(st.session_state.links_list) > 0:
        with st.sidebar:
            c1, c2 = st.columns([0.85, 0.15], vertical_alignment='center')
            for i, link in enumerate(st.session_state.links_list):
                with c1:
                    st.markdown(link)
                with c2:
                    if st.button('⛔', key=f"remove_{i}", help='Remove link'):
                        remove_single_link(i)
                        st.rerun()

            c1, c2 = st.columns([0.3, 0.7])
            with c2:
                clear_links = st.button('Clear all links', on_click=clear_all_links)

    with st.sidebar:
        if st.button('Process', use_container_width=True, type='primary', on_click=start_processing):
            if len(files) == 0 and len(st.session_state.links_list)==0:
                st.sidebar.markdown('<h1><center>No file detected', unsafe_allow_html=True)
            else : 
                with st.spinner("Processing"):
                    pdf_text = None
                    webpage_text = None
                    if len(files) > 0 :
                        pdf_text, no_of_pgs = pdf_reader(files)
                    if len(st.session_state.links_list) > 0:
                        webpage_text = webpage_reader(st.session_state.links_list)
                    if pdf_text and webpage_text :
                        full_text = pdf_text + webpage_text
                    elif pdf_text :
                        full_text = pdf_text
                    else :
                        full_text = webpage_text
                    text_chunks = get_text_chunks(full_text)
                    stime = time.time()
                    vector_store = get_vectorstore(text_chunks)
                    etime = time.time()
                    print(' Total Time taken : ',etime-stime)
                    st.header('Your file has been processed.',anchor=False)
                    return vector_store

#----------------------- Logic of the webapp -------------------------------
if __name__ == '__main__':
    if 'audio_placeholder' not in st.session_state:
        st.session_state.audio_placeholder = st.empty()
    if "backend_messages" not in st.session_state:
        st.session_state.backend_messages = []
    if "frontend_messages" not in st.session_state:
        st.session_state.frontend_messages = []
    if 'query_num' not in st.session_state:
        st.session_state.query_num = 1
    if 'start_func' not in st.session_state:
        st.session_state.start_func = False
    if 'links_list' not in st.session_state:
        st.session_state.links_list = []
    if 'clear_links' not in st.session_state:
        st.session_state.clear_links = False
    if 'start_process' not in st.session_state:
        st.session_state.start_process = False

    if st.session_state.clear_links:
        st.session_state.links_list.clear()
        st.session_state.clear_links = False

    with st.sidebar:
        st.markdown('<h1><center>Your docs </center></h1>', unsafe_allow_html=True)
        files = st.file_uploader(label="Upload docs",accept_multiple_files=True, label_visibility='collapsed')
        st.markdown('<h1><center>Provide website links </center></h1>', unsafe_allow_html=True)
        link = st.chat_input('Paste the link')
    
    try :
        vec_store = main(files, link)
    except Exception as exc:
        # print(exc)
        st.sidebar.markdown('<center><font color="white">Poor internet connection or Invalid URL', unsafe_allow_html=True)
        vec_store = None

    if vec_store is not None:
        st.session_state.vec_store = vec_store
    clear_history()

    def callback():
        st.session_state.start_func = True

    for message in st.session_state.frontend_messages:
        if message['role'] == 'user' :
            with st.chat_message(message['role'], 
                                 avatar=user_avatar_path):
                st.markdown(message['content'])
        else :
            with st.chat_message(message['role'],
                                avatar=assistant_avatar_path):
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

    
    if transcribed_txt :
        text = transcribed_txt

    if cam or st.session_state.start_func:
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
            st.session_state.query_num+=1

            with st.chat_message('user', avatar=user_avatar_path):
                st.markdown(formatted_query)
            st.markdown(
                """
                <script>
                var audio = document.getElementById('tts_audio');
                if (audio) {
                    audio.pause();
                    audio.currentTime = 0;
                }
                </script>
                """,
                unsafe_allow_html=True
                )
            # For raising error to avoid exhaustion of API 
            temporary = vec_store.similarity_search(query=query)
            ini = time.time()
            new_query = ans_groq.Rag_Groq1(st.session_state.backend_messages,
                                           query, st.session_state.query_num)
            print(new_query)
            new_query = new_query.split('Explanation:')[0][11:-1]
            if new_query is None:
                new_query = query
            print('\nModified Question : ',new_query)
            fin = time.time()
            print('LLM 1 Response Time : ', fin-ini)

            if new_query is None :
                new_query = query 

            with st.spinner('Extracting information from documents'):
                chunks_ = vec_store.similarity_search(query=new_query)

            rel_chunks = ''
            for i in range(len(chunks_)):
                rel_chunks = rel_chunks + f'\n\nContext {i+1} : ' + chunks_[i].page_content
            st.session_state.frontend_messages.append({"role": "user", "content": query})
            st.session_state.backend_messages.append({"role": "user", "content": new_query})

            with st.chat_message(name='assistant', avatar=assistant_avatar_path):
                ini = time.time()
                response = st.write_stream(ans_groq.RAG_Groq2(st.session_state.backend_messages, rel_chunks, new_query, 
                            st.session_state.query_num))
                fin = time.time()
                print('LLM 2 Response Time : ', fin-ini)
                st.session_state.frontend_messages.append({"role": "assistant", "content": response})
                st.session_state.backend_messages.append({"role": "assistant", "content": response})
                try : 
                    audio_bytes = text_to_speech(response)
                    autoplay_tts(audio_bytes)
                except Exception as exc:
                    # st.write(exc)
                    st.write('Poor internet connect couldnt transcribe text to speech')
    except Exception as ex:
        # st.write(ex)
        st.markdown('<h4><font color="yellow"><center>Oops! We need some PDFs/ Websites as Context.', unsafe_allow_html=True)