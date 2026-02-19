 # 🤖 AI Assisted Code Review - Master Thesis Project  
**Development of an AI-Powered Interactive Programming Learning Assistant**


## 📚 Thesis Information
**Author:** Mahdi Roshanizarmehri  
**Matrikelnummer:** 69189307  
**Email:** mahdi.roshanizarmehri@ue-german.de  
**University:** University of Europe for Applied Sciences  
**Degree Program:** Master of Software Engineering
**Thesis Type:** Master Thesis  
**Supervisor:** Prof. Dr. Raja Hashim Ali, Prof. Dr. Iftikhar Ahmed  
**Submission Deadline:** 9th March 2026  
**Academic Year:** 2025/2026  

## 🎯 Executive Summary

### Thesis Title
**"Design and Development of an AI-Assisted Code Review Tool for Beginner Programmers"**

### Abstract
This master's thesis describes the design, implementation, and evaluation of an AI-based programming tutor that runs entirely on the user's own computer, without relying on external servers. This system runs large language models locally through the Ollama framework to provide individualized, interactive programming instruction without requiring internet access or cloud services. The application targets key challenges in programming education by improving access, protecting privacy, and allowing learners to progress at a pace that fits their needs. This study adds to educational technology research by showing that locally hosted AI tutors can be implemented in computer science courses and can support student learning outcomes.

### Keywords
- AI in Education
- Programming Tutor
- Local LLMs
- Ollama Integration
- Computer Science Education
- Privacy-Preserving AI
- Streamlit Applications
- Interactive Learning Systems
  
## 📖 Table of Contents
1. [System Architecture](#1-system-architecture)
2. [Implementation](#2-implementation)
3. [Features](#3-features)
4. [Results & Discussion](#4-results--discussion)
5. [Conclusion](#5-conclusion)
6. [Appendices](#6-appendices)

## 1. System Architecture

## 📖 Table of Contents
1. [System Architecture](#1-system-architecture)
2. [Implementation](#2-implementation)
3. [Features](#3-features)
4. [Results & Discussion](#4-results--discussion)
5. [Conclusion](#5-conclusion)
6. [Appendices](#6-appendices)

## 1. System Architecture

### 1.1 High-Level Architecture
```
┌────────────────────────────────────────────────────────────┐
│                     User Interface Layer                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 Streamlit Web Application            │  │
│  │  • Chat Interface      • File Upload                 │  │
│  │  • Session Management  • Response Streaming          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                               │
┌────────────────────────────────────────────────────────────┐
│                    Application Logic Layer                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Python Backend (app.py)                    │  │
│  │  • Message Processing  • File Handling               │  │
│  │  • Context Management  • Session State               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                               │
┌────────────────────────────────────────────────────────────┐
│                     AI Integration Layer                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 Ollama Integration                   │  │
│  │  • Model Management   • API Communication            │  │
│  │  • Response Streaming • Error Handling               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                               │
┌────────────────────────────────────────────────────────────┐
│                      Local AI Layer                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 Local LLM (qwen2.5-coder)            │  │
│  │  • Model Inference    • Response Generation          │  │
│  │  • Context Processing • Token Management             │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### 1.2 Technical Stack
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Frontend | Streamlit | 1.29.0 | Web interface framework |
| Backend | Python | 3.8+ | Application logic |
| AI Runtime | Ollama | Latest | Local LLM deployment |
| LLM Model | qwen2.5-coder | 3B | Programming-focused AI |
| Dependencies | Various | See requirements.txt | Supporting libraries |

### 1.3 Data Flow
1. **User Input →** Streamlit Interface → Python Backend
2. **Backend Processing →** Context Assembly → Ollama API Call
3. **Ollama →** Local Model Inference → Streaming Response
4. **Response →** Backend Processing → Streamlit Interface → User

## 2. Implementation

### 2.1 Core Components

#### 2.1.1 Main Application (`app.py`)
```python
# Key features implemented:
# 1. Chat interface with message history
# 2. Real-time response streaming
# 3. File upload and processing
# 4. Session state management
# 5. Model configuration interface
```

#### 2.1.2 Ollama Integration
- **API Communication:** REST API calls to local Ollama server
- **Streaming Implementation:** Real-time character-by-character display
- **Error Handling:** Comprehensive exception management
- **Model Switching:** Dynamic model selection at runtime

#### 2.1.3 User Interface
- **Responsive Design:** Works on desktop and mobile
- **Accessibility Features:** Screen reader support, keyboard navigation
- **Internationalization:** UTF-8 support for multiple languages
- **Custom Styling:** CSS enhancements for better UX

### 2.2 Key Algorithms

#### 2.2.1 Context Management Algorithm
```
Algorithm: Context Assembly
Input: User message, conversation history, uploaded files
Output: Formatted context for LLM

1. Initialize empty context string
2. Append system prompt with teaching guidelines
3. For each message in recent history (last 6 messages):
   a. Format as "Role: Content"
   b. Append to context
4. If files uploaded:
   a. For each file: append "File: [filename]\n[content]"
5. Append current user message
6. Return context
```

#### 2.2.2 Response Streaming Algorithm
```
Algorithm: Stream Response
Input: Prompt, System Context
Output: Streaming text response

1. Initialize empty response buffer
2. Call Ollama API with streaming enabled
3. While receiving chunks:
   a. Parse JSON response
   b. Extract text content
   c. Append to buffer
   d. Update UI with buffer content
   e. Yield chunk for streaming
4. Handle completion or errors
5. Store complete response in history
```
### 2.3 Security and Privacy Features
- **Local Processing:** All data stays on user's machine
- **No External Calls:** Complete offline functionality
- **Session Isolation:** Chat history cleared on application close
- **File Handling:** Temporary file processing without persistence

## 3. Features

### 3.1 Core Educational Features
| Feature | Description | Implementation Status |
|---------|-------------|----------------------|
| Interactive Q&A | Real-time conversation with AI tutor | ✅ Implemented |
| Code Analysis | Upload and review programming code | ✅ Implemented |
| Step-by-Step Guidance | Breaking down complex concepts | ✅ Implemented |
| Multiple Language Support | Python, JavaScript, Java, C++, etc. | ✅ Implemented |
| Error Explanation | Debugging assistance with explanations | ✅ Implemented |

### 3.2 Technical Features
| Feature | Description | Educational Value |
|---------|-------------|-------------------|
| Local Processing | No internet required | Privacy protection |
| Model Selection | Choose different AI models | Adaptive teaching styles |
| File Upload | Submit code for review | Practical application |
| Conversation Export | Save learning sessions | Progress tracking |
| Custom Prompts | Adjust AI behavior | Personalized learning |

### 3.3 Advanced Features
1. **Context-Aware Responses:** Maintains conversation history
2. **Code Syntax Highlighting:** Improves code readability
3. **Multi-file Analysis:** Handle multiple uploaded files
4. **Parameter Tuning:** Adjust AI creativity and response length
5. **Cross-Platform Support:** Windows, macOS, Linux

## 4. Results & Discussion

### 4.1 Expected Outcomes

#### Technical Success:
- Functional local AI tutoring system
- Acceptable response times (<5 seconds average)
- Low system resource usage (<2GB RAM)

#### Educational Impact:
- Significant learning gains (p < 0.05)
- High user satisfaction (SUS > 80)
- Positive qualitative feedback

#### Usability Results:
- Intuitive interface (learnability < 10 minutes)
- High engagement (average session > 15 minutes)
- Low error rates (<5% user-reported issues)

### 4.2 Discussion Points
1. **Privacy vs. Performance Trade-off:** Analyzing the balance between local processing limitations and privacy benefits
2. **Model Selection Impact:** How different LLMs affect educational outcomes
3. **Scalability Considerations:** Potential for classroom deployment
4. **Integration Possibilities:** Combining with existing learning management systems

## 5. Conclusion

### 5.1 Conclusion
This thesis demonstrates the feasibility and effectiveness of locally-deployed AI tutors for programming education. The developed system successfully addresses privacy concerns while providing personalized, interactive learning experiences. The research contributes to both educational technology and practical AI deployment methodologies.

### 5.2 Contributions
1. **Theoretical Contribution:** Framework for local AI educational tools
2. **Practical Contribution:** Open-source implementation for community use
3. **Methodological Contribution:** Evaluation framework for AI tutoring systems
4. **Educational Contribution:** Evidence-based approach to programming instruction

### 5.3 Societal Impact
1. **Educational Equity:** Making programming education more accessible
2. **Privacy Protection:** Setting standards for educational AI tools
3. **Open Science:** Providing open-source tools for researchers
4. **Sustainable AI:** Promoting efficient, locally-run AI applications

## 6. Appendices


### Appendix A: Installation and Setup Guide

#### Prerequisites
- Python 3.8 or higher (Download from [python.org](https://python.org))
- Ollama (Download from [ollama.com](https://ollama.com))
- At least 4GB RAM recommended
- Windows/Mac/Linux operating system

#### Step 1: Download Ollama
1. Go to [ollama.com](https://ollama.com)
2. Download and install Ollama for your operating system
3. **Windows:** Run the installer (.exe file)
4. **Mac:** Drag Ollama to Applications folder
5. **Linux:** Follow terminal instructions on website

#### Step 2: Get the Code
Download the project files:

**Option A - Download ZIP:**
1. Click "Code" button
2. Select "Download ZIP"
3. Extract the ZIP file to a folder

**Option B - Clone (if you have Git):**
```bash
git clone https://github.com/[YOUR_USERNAME]/ai-programming-tutor.git
cd ai-programming-tutor
```

#### Step 3: Install Python Requirements
Open terminal/command prompt in the project folder:

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

#### Step 4: Download AI Model
In a NEW terminal window, run:
```bash
# Start Ollama service (keep this running)
ollama serve
```

In ANOTHER terminal window, run:
```bash
# Download the AI model (this may take 5-10 minutes)
ollama pull qwen2.5-coder:3b
```

#### Step 5: Run the Application
Back in your first terminal (with venv activated):
```bash
streamlit run app.py
```

The app will open in your browser at: **http://localhost:8501**

### Appendix B: Source Code Documentation

#### Modules Used
- **`json`** - Data serialization for conversation export
- **`streamlit`** - Web application framework
- **`subprocess`** - System command execution for Ollama

#### Functions
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `check_ollama_status() -> Dict` | Checks Ollama installation and service status | None | Status dictionary |
| `clear_chat()` | Clears conversation history | None | None |
| `export_conversation()` | Exports chat to JSON file | None | Filename |
| `generate_ollama_response_api()` | Uses HTTP API for AI responses | prompt, system_prompt | Streaming generator |
| `generate_ollama_response_cli()` | Uses CLI fallback for AI responses | prompt, system_prompt | Streaming generator |
| `process_file_upload()` | Processes uploaded files | uploaded_file | File content or None |
| `stream_ollama_response()` | Main response handler with fallback | prompt, system_prompt | Streaming generator |

#### Constants
```python
MODEL_NAME = "qwen2.5-coder:3b"  # Default AI model
DEFAULT_SYSTEM_PROMPT = """You are an AI programming tutor for beginners..."""
```

*(Generated with pydoc)*

### Appendix C: Ethical Considerations
1. **Data Privacy:** All processing is local, no data collection occurs
2. **Bias Mitigation:** Multiple model options to reduce single-model bias
3. **Accessibility:** Designed with WCAG guidelines in mind
4. **Transparency:** Open-source implementation for public scrutiny

## 🙏 Acknowledgments

I would like to express my sincere gratitude to:

1. **My Supervisor:** Prof. Dr. Raja Hashim Ali for invaluable guidance and support
2. **University Faculty:** For providing resources and expertise
3. **Open Source Community:** For the tools and frameworks that made this project possible
