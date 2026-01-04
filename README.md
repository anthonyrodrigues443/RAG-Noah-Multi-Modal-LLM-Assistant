# RAG-Noah - Multi-Modal LLM Assistant 🤖

**A comprehensive RAG (Retrieval Augmented Generation) system built with multiple LLMs via GROQ API for organizations to embed their data and help clients extract relevant information efficiently.**

## 🚀 Live Demo
**Test the webapp now:** https://rag-noah.streamlit.app/

*Note: Camera features are available in local setup only due to web deployment limitations.*

![RAG Architecture](imagefiles/rag_architecture.png)

## 📋 Project Overview

RAG-Noah is a multi-modal intelligent assistant with **two distinct modes**:

### 1. RAG Noah (Main Page)
A document-based Q&A assistant that processes PDFs and websites to answer questions from your uploaded content.

### 2. Noah (Sidebar Navigation → "Noah")
A general-purpose assistant with real-time computer vision capabilities including object detection and hand tracking.

Perfect for organizations looking to embed their data (policies, procedures, FAQs) and provide clients with instant access to relevant information.

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.8+ |
| **Framework** | Streamlit |
| **LLMs** | Gemma (query refinement) + LLaMA 70B (response generation) via GROQ API |
| **Vector Database** | FAISS (Facebook AI Similarity Search) |
| **Embeddings** | `nomic-ai/nomic-embed-text-v1` (HuggingFace) |
| **Object Detection** | YOLOv8n (Ultralytics) |
| **Hand Tracking** | cvzone + MediaPipe |
| **OCR** | EasyOCR |
| **Speech** | streamlit-mic-recorder, gTTS |

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.8+
- 10 GROQ API keys (for rate limit handling with key rotation)
- System packages: `libgl1`, `portaudio19-dev` (Linux/deployment)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/anthonyrodrigues443/RAG-Noah-Multi-Modal-LLM-Assistant.git
cd RAG-Noah-Multi-Modal-LLM-Assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure API keys**
```bash
# Navigate to .streamlit folder
cd .streamlit

# Rename the example file
# Windows:
ren secrets_eg.toml secrets.toml
# macOS/Linux:
mv secrets_eg.toml secrets.toml

# Edit secrets.toml and add your 10 GROQ API keys
# The system rotates through these keys to handle rate limits
```

6. **Run the application**
```bash
streamlit run RAG_Noah.py
```

## 🎯 Core Features

### RAG Noah (Document Intelligence)

**Multi-Source Data Integration**
- PDF document processing and text extraction
- Website content scraping and indexing

**Advanced Query Processing**
- Text input with natural language understanding
- Voice input with speech-to-text conversion
- Visual input with OCR text extraction from camera

**Intelligent Information Retrieval**
- Vector-based similarity search using FAISS
- Context-aware query refinement using chat history
- Top-4 relevant chunk retrieval for accurate responses

**Enhanced User Experience**
- Streaming response generation
- Text-to-speech output
- Conversation history maintenance

### Noah (Multi-Modal Assistant)

**Computer Vision Capabilities**
- Real-time object detection using YOLOv8n
- Hand tracking with finger counting (identifies which specific fingers are up)
- 5-second capture window for vision analysis

**Adaptive Processing**
- Intelligent query classification determines if camera is needed
- Conditional computer vision activation (only when visually-relevant questions asked)
- Multi-modal input processing (text, voice, camera)

## 🔧 Technical Architecture

### RAG Pipeline
1. **Document Processing**: Extract and concatenate text from PDFs and websites
2. **Text Chunking**: Split into 1024-token chunks with 256-token overlap
3. **Vector Embeddings**: Convert chunks using `nomic-embed-text-v1`
4. **Vector Storage**: Store embeddings in FAISS for efficient retrieval
5. **Query Refinement**: Fix grammar/incomplete queries using Gemma model
6. **Similarity Search**: Retrieve top-4 most relevant chunks
7. **Response Generation**: Generate contextual responses using LLaMA 70B

### Dual-Model Architecture

The system uses two LLM calls per query for optimal results:

| Stage | Model | Purpose |
|-------|-------|---------|
| **API Call 1** | Gemma | Query refinement - fixes spelling, grammar, expands incomplete questions using chat history |
| **API Call 2** | LLaMA 70B Versatile | Response generation with retrieved context chunks |

**For Noah (vision assistant):**
| Stage | Model | Purpose |
|-------|-------|---------|
| **API Call 1** | LLaMA 70B | Classifies if camera is needed (yes/no) based on question |
| **API Call 2** | LLaMA 70B | Generates response, including vision observations if camera was activated |

## 💡 Example Interactions

### RAG Mode
```
1. Upload your company's HR policy PDF
2. Ask: "What is the leave policy for new employees?"
3. System retrieves relevant chunks and generates contextual answer
```

### Noah Mode
```
1. Ask: "How many fingers am I holding up?"
2. System activates camera for 5 seconds
3. Detects: "3 fingers up on right hand (index, middle, ring)"
4. Responds with accurate finger count
```

## 🎨 Use Cases

### For Organizations
- **Customer Support**: Instant access to policy information, procedures, and FAQs
- **Employee Training**: Quick retrieval of training materials and guidelines
- **Knowledge Management**: Centralized access to organizational knowledge base

### For Educational Institutions
- **Student Queries**: Information about admission cutoffs, procedures
- **Academic Support**: Course materials and curriculum information
- **Administrative Assistance**: Policy and procedure clarification

## 📊 Performance Highlights

- **Accurate Retrieval**: Context-aware information extraction with query refinement
- **Fast Response**: Optimized FAISS vector search
- **Rate Limit Handling**: 10-key rotation system for uninterrupted service
- **Multi-Modal**: Support for text, voice, and visual inputs

## 🛣️ Future Enhancements

- **Fine-tuned LLM**: Custom model training for domain-specific improvements
- **Image Understanding**: Advanced image captioning and analysis
- **Reranking**: Cross-encoder reranking for improved retrieval (code ready, commented out)
- **Database Integration**: Extended connectivity options
- **Web Camera Support**: Enable camera features in deployed web app

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

## 📧 Contact

For questions or collaboration opportunities, connect with me on [LinkedIn](https://www.linkedin.com/in/anthonyrodrigues443).

---

*Built with ❤️ for efficient organizational knowledge management*
