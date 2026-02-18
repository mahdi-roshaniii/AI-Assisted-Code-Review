 # 🤖 AI Assisted Code Review - Master Thesis Project  
**Development of an AI-Powered Interactive Programming Learning Assistant**


## 📚 Thesis Information
**Author:** Mahdi Roshanizarmehri  
**Matrikelnummer:** 69189307  
**Email:** mahdi.roshanizarmehri@ue-german.de  
**University:** University of Europe for Applied Sciences  
**Degree Program:** Master of Software Engineering
**Thesis Type:** Master Thesis  
**Supervisor:** Prof. Dr. Raja Hashim Ali  
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
