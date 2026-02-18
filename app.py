import streamlit as st
import subprocess
import json
from datetime import datetime
from typing import Dict, Optional, Generator

# Page configuration
st.set_page_config(
    page_title="AI Programming Tutor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1000px;
    }
    
    /* Chat messages */
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* User message */
    [data-testid="stChatMessage"]:has(svg[aria-label="user"]) {
        background-color: #f0f2f6;
        border-left: 4px solid #4f46e5;
    }
    
    /* Assistant message */
    [data-testid="stChatMessage"]:has(svg[aria-label="assistant"]) {
        background-color: #f8fafc;
        border-left: 4px solid #10b981;
    }
    
    /* Code blocks */
    pre {
        border-radius: 8px;
        padding: 1rem !important;
        background-color: #1e293b !important;
    }
    
    code {
        font-family: 'Fira Code', 'Consolas', monospace;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #f8fafc;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* File uploader */
    .uploadedFile {
        background-color: #e0f2fe;
        padding: 0.5rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border: 1px solid #bae6fd;
    }
    
    /* Status indicators */
    .status-success {
        color: #059669;
        font-weight: 500;
    }
    
    .status-warning {
        color: #d97706;
        font-weight: 500;
    }
    
    .status-error {
        color: #dc2626;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Constants
MODEL_NAME = "qwen2.5-coder:3b"
DEFAULT_SYSTEM_PROMPT = """You are an AI programming tutor for beginners. Follow these guidelines:

1. **Clarity**: Explain concepts in simple, easy-to-understand language
2. **Step-by-Step**: Break down complex topics into manageable steps
3. **Examples**: Always provide practical code examples when relevant
4. **Encouragement**: Be patient, friendly, and supportive
5. **Code Analysis**: When given code, explain what it does and suggest improvements

Format responses with clear explanations and code snippets in appropriate languages."""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT
if "model_name" not in st.session_state:
    st.session_state.model_name = MODEL_NAME
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 2048
if "response_in_progress" not in st.session_state:
    st.session_state.response_in_progress = False
if "file_history" not in st.session_state:
    st.session_state.file_history = []
if "connection_checked" not in st.session_state:
    st.session_state.connection_checked = False
if "ollama_status" not in st.session_state:
    st.session_state.ollama_status = {}

def check_ollama_status() -> Dict:
    """Check if Ollama is running and models are available"""
    status = {
        "installed": False, 
        "running": False, 
        "model_available": False,
        "available_models": []
    }
    
    try:
        # Check if ollama command exists
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        status["installed"] = result.returncode == 0
        if status["installed"]:
            status["version"] = result.stdout.strip()
        else:
            status["error"] = "Ollama not found. Please install from https://ollama.com"
            return status
        
        # Check if ollama is running
        list_result = subprocess.run(
            ["ollama", "list"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        status["running"] = list_result.returncode == 0
        
        if status["running"]:
            # Parse available models
            lines = list_result.stdout.strip().split('\n')
            models = []
            for line in lines[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if parts:
                        models.append(parts[0])
            
            status["available_models"] = models
            
            # Check if current model is available
            if st.session_state.model_name in models:
                status["model_available"] = True
            elif models:
                # If current model not available, switch to first available model
                st.session_state.model_name = models[0]
                status["model_available"] = True
                status["model_switched"] = f"Switched to {models[0]}"
            else:
                status["model_available"] = False
                status["warning"] = "No models found. Run: `ollama pull llama2`"
        
        else:
            status["error"] = "Ollama service not running. Start with: `ollama serve`"
    
    except subprocess.TimeoutExpired:
        status["error"] = "Ollama connection timeout. Make sure Ollama is running."
    except FileNotFoundError:
        status["error"] = "Ollama not installed. Download from https://ollama.com"
    except Exception as e:
        status["error"] = f"Unexpected error: {str(e)}"
    
    # Store in session state
    st.session_state.ollama_status = status
    st.session_state.connection_checked = True
    
    return status

def generate_ollama_response_api(prompt: str, system_prompt: str = None) -> Generator[str, None, None]:
    """Generate response from Ollama using HTTP API"""
    try:
        # Build the messages in Ollama format
        messages = []
        
        # Add system prompt if provided
        if system_prompt and system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt})
        
        # Add recent conversation history (last 3 exchanges)
        history_messages = st.session_state.messages[-6:] if len(st.session_state.messages) > 6 else st.session_state.messages
        for msg in history_messages:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Create the request payload
        request_data = {
            "model": st.session_state.model_name,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": st.session_state.temperature,
                "num_predict": st.session_state.max_tokens
            }
        }
        
        # Use curl to call Ollama's API endpoint
        curl_command = [
            "curl", "-s", "-N",  # -N for no buffering
            "-X", "POST", 
            "http://localhost:11434/api/chat",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(request_data)
        ]
        
        # Start the subprocess
        process = subprocess.Popen(
            curl_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Read and parse the streaming response
        buffer = ""
        while True:
            char = process.stdout.read(1)
            if not char:
                break
                
            buffer += char
            
            # Try to parse complete JSON lines
            if char == '\n' and buffer.strip():
                try:
                    line = buffer.strip()
                    if line:
                        response_chunk = json.loads(line)
                        if "message" in response_chunk and "content" in response_chunk["message"]:
                            yield response_chunk["message"]["content"]
                        elif "response" in response_chunk:
                            yield response_chunk["response"]
                except json.JSONDecodeError:
                    # Sometimes we get partial JSON, continue buffering
                    continue
                finally:
                    buffer = ""
        
        # Check for errors
        if process.poll() is not None and process.returncode != 0:
            error = process.stderr.read()
            if error:
                yield f"\n\n**Error in API call:** {error}"
    
    except Exception as e:
        yield f"**Error in API method:** {str(e)}"

def generate_ollama_response_cli(prompt: str, system_prompt: str = None) -> Generator[str, None, None]:
    """Generate response using direct ollama run command"""
    try:
        # Build the full prompt
        if system_prompt and system_prompt.strip():
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        else:
            full_prompt = f"User: {prompt}\n\nAssistant:"
        
        # Run ollama with timeout
        cmd = ["ollama", "run", st.session_state.model_name]
        
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Write prompt and close stdin
        process.stdin.write(full_prompt)
        process.stdin.flush()
        process.stdin.close()
        
        # Read output in real-time
        while True:
            output = process.stdout.read(1024)
            if output:
                yield output
            
            # Check if process has ended
            if process.poll() is not None:
                # Read any remaining output
                remaining = process.stdout.read()
                if remaining:
                    yield remaining
                break
        
        # Check for errors
        if process.returncode != 0:
            error = process.stderr.read()
            if error:
                yield f"\n\n**Error in CLI call:** {error}"
                
    except Exception as e:
        yield f"**Error in CLI method:** {str(e)}"

def stream_ollama_response(prompt: str, system_prompt: str = None) -> Generator[str, None, None]:
    """Unified streaming response handler - tries API first, then CLI"""
    # First check Ollama status
    status = check_ollama_status()
    
    if not status.get("running", False):
        yield "**Error:** Ollama is not running. Please start Ollama with `ollama serve` in your terminal."
        return
    
    if not status.get("model_available", False):
        yield "**Error:** No models available. Please pull a model with `ollama pull qwen2.5-coder:3b`"
        return
    
    # Try API method first
    try:
        st.session_state.response_in_progress = True
        for chunk in generate_ollama_response_api(prompt, system_prompt):
            yield chunk
    except Exception as api_error:
        # Fallback to CLI method
        try:
            for chunk in generate_ollama_response_cli(prompt, system_prompt):
                yield chunk
        except Exception as cli_error:
            yield f"**Both methods failed:**\n- API error: {str(api_error)}\n- CLI error: {str(cli_error)}"
    finally:
        st.session_state.response_in_progress = False

def process_file_upload(uploaded_file) -> Optional[str]:
    """Process uploaded file and return its content"""
    try:
        # Read file content
        content = uploaded_file.getvalue().decode('utf-8')
        
        # Store file info in session state
        file_info = {
            "name": uploaded_file.name,
            "size": len(content),
            "type": uploaded_file.type,
            "timestamp": datetime.now().isoformat(),
            "content_preview": content[:500] + "..." if len(content) > 500 else content
        }
        
        st.session_state.file_history.append(file_info)
        
        # Keep only last 10 files in history
        if len(st.session_state.file_history) > 10:
            st.session_state.file_history = st.session_state.file_history[-10:]
        
        return content
    
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

def export_conversation():
    """Export conversation to JSON file"""
    conversation_data = {
        "model": st.session_state.model_name,
        "timestamp": datetime.now().isoformat(),
        "system_prompt": st.session_state.system_prompt,
        "temperature": st.session_state.temperature,
        "max_tokens": st.session_state.max_tokens,
        "messages": st.session_state.messages,
        "uploaded_files": [
            {"name": f["name"], "size": f["size"], "type": f["type"]} 
            for f in st.session_state.file_history[-5:]
        ]
    }
    
    filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(conversation_data, f, indent=2, ensure_ascii=False)
    
    return filename

def clear_chat():
    """Clear chat history"""
    st.session_state.messages = []
    st.session_state.uploaded_files = []
    st.rerun()

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Connection status
    st.subheader("Connection Status")
    
    # Check connection on first load or manually
    if not st.session_state.connection_checked:
        check_ollama_status()
    
    status = st.session_state.ollama_status
    
    if status.get("installed", False):
        if status.get("running", False):
            st.markdown('<p class="status-success">✅ Ollama is running</p>', unsafe_allow_html=True)
            
            # Model selector
            if status.get("available_models"):
                selected_model = st.selectbox(
                    "Select Model",
                    status["available_models"],
                    index=status["available_models"].index(st.session_state.model_name) 
                    if st.session_state.model_name in status["available_models"] else 0
                )
                st.session_state.model_name = selected_model
                
                if status.get("model_switched"):
                    st.info(status["model_switched"])
            else:
                st.markdown('<p class="status-warning">⚠️ No models found</p>', unsafe_allow_html=True)
                st.code("ollama pull qwen2.5-coder:3b", language="bash")
        else:
            st.markdown('<p class="status-error">❌ Ollama not running</p>', unsafe_allow_html=True)
            st.code("ollama serve", language="bash")
    else:
        st.markdown('<p class="status-error">❌ Ollama not installed</p>', unsafe_allow_html=True)
        st.markdown("[Download Ollama](https://ollama.com)")
    
    # Refresh connection button
    if st.button("🔄 Refresh Connection", use_container_width=True):
        st.session_state.connection_checked = False
        st.rerun()
    
    # System prompt editor
    st.subheader("System Prompt")
    st.session_state.system_prompt = st.text_area(
        "Customize the system prompt",
        value=st.session_state.system_prompt,
        height=200,
        help="This defines how the assistant behaves"
    )
    
    if st.button("🔄 Reset to Default", use_container_width=True):
        st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT
        st.rerun()
    
    # Model parameters
    st.subheader("Model Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Higher = more creative, Lower = more focused"
        )
    
    with col2:
        st.session_state.max_tokens = st.slider(
            "Max Tokens",
            min_value=128,
            max_value=8192,
            value=st.session_state.max_tokens,
            step=128,
            help="Maximum response length"
        )
    
    # File upload section
    st.divider()
    st.subheader("📁 Upload Files")
    
    uploaded_files = st.file_uploader(
        "Upload code/text files",
        type=[
            "txt", "py", "js", "java", "cpp", "c", "cs", 
            "html", "css", "md", "json", "xml", "yaml", 
            "yml", "go", "rs", "rb", "php", "sql", "ts"
        ],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    # Process newly uploaded files
    new_uploads = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Check if this file was already uploaded
            if not any(f["name"] == uploaded_file.name for f in st.session_state.file_history[-10:]):
                content = process_file_upload(uploaded_file)
                if content:
                    new_uploads.append({
                        "name": uploaded_file.name,
                        "content": content
                    })
    
    # Add new uploads to session state
    if new_uploads:
        st.session_state.uploaded_files.extend(new_uploads)
        for upload in new_uploads:
            st.success(f"✅ {upload['name']}")
    
    # Display recent files
    if st.session_state.file_history:
        st.subheader("📋 Recent Files")
        for file_info in st.session_state.file_history[-3:]:  # Show last 3 files
            with st.expander(f"📄 {file_info['name']} ({file_info['size']} chars)"):
                # Try to guess language for syntax highlighting
                extension = file_info['name'].split('.')[-1].lower()
                languages = {
                    'py': 'python', 'js': 'javascript', 'java': 'java',
                    'cpp': 'cpp', 'c': 'c', 'html': 'html', 'css': 'css',
                    'md': 'markdown', 'json': 'json', 'xml': 'xml',
                    'yaml': 'yaml', 'yml': 'yaml', 'txt': 'text'
                }
                language = languages.get(extension, 'text')
                st.code(file_info["content_preview"], language=language)
    
    # Conversation management
    st.divider()
    st.subheader("Conversation")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
    
    with col2:
        if st.button("💾 Export Chat", use_container_width=True):
            try:
                filename = export_conversation()
                st.success(f"✅ Exported to {filename}")
                
                # Create download button
                with open(filename, "rb") as file:
                    st.download_button(
                        label="📥 Download",
                        data=file,
                        file_name=filename,
                        mime="application/json",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error exporting: {str(e)}")
    
    # Current model info
    st.divider()
    st.caption(f"**Current Model:** {st.session_state.model_name}")
    st.caption(f"**Messages in chat:** {len(st.session_state.messages)}")

# Main chat interface
st.title("🤖 AI Programming Tutor")
st.caption(f"Powered by Ollama • Model: {st.session_state.model_name}")

# Display connection warnings
status = st.session_state.ollama_status
if status.get("error"):
    st.error(f"Connection Issue: {status['error']}")
elif not status.get("running", False):
    st.warning("⚠️ Ollama is not running. Please start it with `ollama serve`")

# Display uploaded files context
if st.session_state.uploaded_files:
    with st.expander(f"📎 Attached Files ({len(st.session_state.uploaded_files)})", expanded=False):
        for i, file_data in enumerate(st.session_state.uploaded_files):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{file_data['name']}**")
            with col2:
                if st.button("🗑️", key=f"remove_{i}", help="Remove this file"):
                    st.session_state.uploaded_files.pop(i)
                    st.rerun()
            
            # Show preview
            preview = file_data['content'][:500] + ("..." if len(file_data['content']) > 500 else "")
            st.code(preview, language="text")
            st.divider()

# Display chat messages
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Add copy button for assistant messages
        if message["role"] == "assistant":
            st.caption(f"Message {i//2 + 1}")

# Chat input
if prompt := st.chat_input("Ask a programming question...", disabled=st.session_state.response_in_progress):
    # Check if Ollama is ready
    if not status.get("running", False):
        st.error("Ollama is not running. Please start it first.")
        st.stop()
    
    if not status.get("model_available", False):
        st.error("No models available. Please pull a model first.")
        st.stop()
    
    # Prepare user message with file context
    user_message_content = prompt
    
    # Include uploaded files in context if any
    if st.session_state.uploaded_files:
        file_context = "\n\n**Attached files:**\n"
        for file_data in st.session_state.uploaded_files:
            file_context += f"\n--- File: {file_data['name']} ---\n"
            file_context += file_data['content'] + "\n"
        user_message_content += file_context
    
    # Add user message to chat history (store original prompt for display)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        if st.session_state.uploaded_files:
            st.caption(f"📎 {len(st.session_state.uploaded_files)} file(s) attached")
    
    # Generate assistant response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Stream the response
            for chunk in stream_ollama_response(user_message_content, st.session_state.system_prompt):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            
            # Final message without cursor
            message_placeholder.markdown(full_response)
            
            # Add assistant response to history
            if full_response.strip():
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.warning("Received empty response from model")
            
        except Exception as e:
            error_msg = f"**Error generating response:** {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        finally:
            st.session_state.response_in_progress = False
    
    # Clear uploaded files after use (optional)
    # st.session_state.uploaded_files = []

# Cancel button if response is stuck
if st.session_state.response_in_progress:
    st.warning("Generating response...")
    if st.button("🛑 Cancel Response", type="secondary"):
        st.session_state.response_in_progress = False
        st.rerun()

# Quick action buttons
if not st.session_state.response_in_progress and len(st.session_state.messages) > 0:
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Continue Conversation", use_container_width=True):
            if st.session_state.messages:
                last_message = st.session_state.messages[-1]["content"]
                st.chat_input(f"Respond to: {last_message[:50]}...")
    
    with col2:
        if st.button("🔍 Analyze Code", use_container_width=True):
            if st.session_state.uploaded_files:
                st.chat_input("Analyze the uploaded code...")
            else:
                st.info("Upload a code file first")
    
    with col3:
        if st.button("🧹 Clear All", use_container_width=True):
            clear_chat()

# Footer
st.divider()
st.caption("""
**Tips:**
1. **Start simple**: "Explain variables in Python"
2. **Upload code**: Get specific feedback on your code
3. **Be specific**: "Why is this loop infinite?" works better than "Fix this code"
4. **Use parameters**: Adjust temperature for more/less creative responses
5. **Model selection**: Different models have different strengths

**Troubleshooting:**
- If responses hang, use the Cancel button and try again
- Ensure Ollama is running: `ollama serve`
- Pull the model if needed: `ollama pull qwen2.5-coder:3b`
""")

