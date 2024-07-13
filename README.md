# Smart Glasses Project 😎

⭐RAG Noah(RAG LLM)📚+ Noah(General LLM🌐 with capability of real time computer vision tasks🔭).  Ultimate Goal is to integrate the software in a AR glasses.

The RAG LLM can also be integrated into websites where the data of the website/institutions is provided as static information and users can access all the essential information at one place.

# RAG Noah (PDF/Website GPT)

## Working of RAG Noah

1) The given PDFs are read and the entire text within the pdf is extracted with a string.
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
<ol>
<li> 1. Since performing CV operations at all times can be memory consuming.</li>
<li>2. Lead the app to lag and Crash eventually.</li>
</ol>
