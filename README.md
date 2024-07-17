# Smart Glasses Project 😎

⭐RAG Noah(RAG LLM)📚+ Noah(General LLM🌐 with capability of real time computer vision tasks🔭).  Ultimate Goal is to integrate the software in a AR glasses.

The RAG LLM can also be integrated into websites where the data of the website/institutions is provided as static information and users can access all the essential information at one place.

## You can test the webapp now !!
Link For <u>RAG Noah and Noah</u> : https://rag-noah.streamlit.app/<br>
Note - the camera features are not available online as there is no successful module to access live client cam and send the live feed frames to the python code.<br>
(If you do know how to do it you can dm me on My <a href="https://www.linkedin.com/in/anthonyrodrigues443">LinkedIn</a>)

## How to run locally
1. Open the terminal 
2. Navigate to the directory you want to run the code.
```
git clone https://github.com/Sharkytony/Smart_glasses_project.git
```
3. Once the repo is cloned Navigate the Smart_Glasses_Project directory
4. Create a virtual environment
```
python -m venv your_venv_name
```
5. Activate your virtual environment
```
your_venv_name/Scripts/activate
```
6. Install the requirements
```
pip install -r requirements.txt
```
7. Rename the secrets_eg.toml to secrets.toml and setup your API keys for GROQ.

8. Finally run 
```
streamlit run RAG_Noah.py
```


# RAG Noah (PDF/Website GPT)

## Working of RAG Noah

1) The given PDFs + Websites are read and the entire text within the document/URL is extracted and concatenated into a string.
2) The text is further splitted into smaller chunks of text .
3) These chunks are then embedded into vectors .
4) The embeddings are then stored in a vectorstore .
5) User Query 

---------> Text input<br>
Plain text is directly given to the RAG Noah.

---------> Voice input  
Voice input is transcribed into text and given to the RAG Noah.

---------> Visual input <br>
Visual input extracts text from visuals and asks the user to process or re click and extract text, the text extracted is then sent to the RAG Noah.

6. The user query is then embedded and similarity search is performed with the query and the vectorstore.
7. Top 5 closest chunks are retrieved and added to the query along with the chat history and as context.
8. The new query is submitted to the GROQ API and the response is retrieved.
9. The response is then displayed, turned to speech and autoplayed.

# Noah (LLM with Real time CV capabilities)

## Working of Noah

1. Three types of user query is accepted even here ( Speech + Text + Visual ).
2. The user query is given to the Groq API 1 which takes the input along with a scenario as a prompt template and restricted to give answer within the two options(Visual information needed/Visual information not needed) given in the prompt only .
3. The API 1 then gives the response accordingly selecting one of the two options.
4. If the option "Visual response needed" is in the response object detection and hand tracking is performed and the detections are listed .
5. These detections are then added to the query as context and provided to the API 2 .
6. Now the API 2 has the observations as context and can answer accordingly.

### Why 2 API's ?
1. Since performing CV operations at all times can be memory consuming.
2. Lead the app to lag and Crash eventually.
3. Getting responses quickly as there is no extra computation.

# Current Achievements of Noah

1. It can detect hands
2. Objects in your hands
3. Count the number of hands you show including the fingers with the finger names as well.

# Future Goals for Noah

1. Image captioning - to be able to caption the real time views .
2. Image generator - to be able to enhance pictures in real time .
3. To be able to play games (Rock-paper-scissors, etc)

