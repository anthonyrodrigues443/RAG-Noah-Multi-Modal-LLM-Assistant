# RAG-Noah - Multi-Modal LLM Assistant 🤖

**A comprehensive RAG (Retrieval Augmented Generation) system built with LLaMA 3.1 for organizations to embed their data and help clients extract relevant information efficiently.**

## 🚀 Live Demo
**Test the webapp now:** https://rag-noah.streamlit.app/

*Note: Camera features are available in local setup only due to web deployment limitations.*

## 📋 Project Overview

RAG-Noah is a multi-modal intelligent assistant that combines:
- **RAG LLM**: For accurate information retrieval from organizational data
- **General LLM**: With real-time computer vision capabilities for enhanced user interaction

Perfect for organizations looking to embed their data (policies, procedures, FAQs) and provide clients with instant access to relevant information like cutoffs, booking procedures, and institutional guidelines.

## 🛠️ Tech Stack

- **Language**: Python
- **Framework**: Streamlit
- **LLM**: LLaMA 3.1 (via GROQ API)
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace Transformers
- **Computer Vision**: OpenCV
- **Speech Processing**: SpeechRecognition, gTTS

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.8+
- GROQ API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Sharkytony/Smart_glasses_project.git
cd Smart_glasses_project
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
# Rename secrets_eg.toml to secrets.toml
# Add your GROQ API key
```

6. **Run the application**
```bash
streamlit run RAG_Noah.py
```

## 🎯 Core Features

### RAG-Noah (Document Intelligence)

**Multi-Source Data Integration**
- PDF document processing and text extraction
- Website content scraping and indexing
- Database integration for organizational data

**Advanced Query Processing**
- Text input with natural language understanding
- Voice input with speech-to-text conversion
- Visual input with text extraction from images

**Intelligent Information Retrieval**
- Vector-based similarity search
- Context-aware query completion using chat history
- Top-k relevant chunk retrieval for accurate responses

**Enhanced User Experience**
- Real-time response generation
- Text-to-speech output
- Conversation history maintenance

### Noah (Multi-Modal Assistant)

**Computer Vision Capabilities**
- Real-time object detection
- Hand tracking and gesture recognition
- Finger counting with detailed finger identification

**Adaptive Processing**
- Intelligent query classification (visual/non-visual)
- Conditional computer vision activation for optimal performance
- Multi-modal input processing

## 🔧 Technical Architecture

### RAG Pipeline
1. **Document Processing**: Extract and concatenate text from PDFs and websites
2. **Text Chunking**: Split content into manageable, semantically meaningful chunks
3. **Vector Embeddings**: Convert text chunks into high-dimensional vectors
4. **Vector Storage**: Store embeddings in ChromaDB for efficient retrieval
5. **Query Enhancement**: Complete incomplete queries using conversation context
6. **Similarity Search**: Find most relevant chunks using vector similarity
7. **Response Generation**: Generate contextual responses using LLaMA 3.1

### Dual-API Architecture
- **API 1**: Query classification and context completion
- **API 2**: Final response generation with enhanced context

This approach ensures:
- Precise information retrieval
- Improved query quality through context awareness
- Efficient resource utilization

## 🎨 Use Cases

### For Organizations
- **Customer Support**: Instant access to policy information, procedures, and FAQs
- **Employee Training**: Quick retrieval of training materials and guidelines
- **Knowledge Management**: Centralized access to organizational knowledge base

### For Educational Institutions
- **Student Queries**: Information about admission cutoffs, booking procedures
- **Academic Support**: Course materials and curriculum information
- **Administrative Assistance**: Policy and procedure clarification

## 🔐 Security & Reliability

- **Robust Prompting**: Prevents jailbreaking attempts
- **Data Privacy**: Secure handling of organizational data
- **Error Handling**: Comprehensive error management for stable operation

## 📊 Performance Highlights

- **Accurate Retrieval**: Context-aware information extraction
- **Fast Response**: Optimized vector search for quick results
- **Scalable**: Easy integration into existing web applications
- **Multi-Modal**: Support for text, voice, and visual inputs

## 🛣️ Future Enhancements

- **Fine-tuned LLM**: Custom model training for domain-specific improvements
- **Image Understanding**: Advanced image captioning and analysis
- **Enhanced Integration**: Extended database connectivity options
- **Real-time Collaboration**: Multi-user support with shared knowledge bases

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

## 📧 Contact

For questions or collaboration opportunities, connect with me on [LinkedIn](https://www.linkedin.com/in/anthonyrodrigues443).

---

*Built with ❤️ for efficient organizational knowledge management*
