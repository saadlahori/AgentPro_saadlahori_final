# agentpro_ui.py
import streamlit as st
import os
import re
from agentpro import ReactAgent, create_model
import time
from agentpro.tools import (
    QuickInternetTool, CalculateTool, UserInputTool, YFinanceTool,
    SlideGenerationTool, AresInternetTool, TraversaalProRAGTool
)
from agentpro.tools.custom_tool_weather_map import WeatherMapTool_OpenWeather
from agentpro.tools.custom_tool_texttospeech_Elevenlabs import TextToSpeechTool_ElevenLabsTTS
from agentpro.tools.custom_tool_unplash_Image import UnsplashImageSearchTool
from agentpro.tools.custom_tool_text_to_image import TextToImage_FluxProTool
from agentpro.tools.custom_tool_huggingface import MostModelTool

# -------------------- Tool Descriptions --------------------
tool_descriptions = {
    # BASE_TOOLS BY AGENTPRO
    "ARES Web Search": "Smart structured web search and extraction.",
    "Quick Web Search": "Real-time internet search for facts and summaries.",
    "CalculateTool": "Performs math and formula evaluation.",
    "UserInputTool": "Fetches custom user inputs within reasoning.",
    "YFinanceTool": "Gets live stock, ETF, and crypto data.",
    "SlideGeneration": "Creates auto-generated slide decks.",
    "TraversaalProRAG": "RAG on internal documentation like manuals.",

    # CUSTOM_TOOLS_BY_SAAD_SALEEM
    "OpenWeatherMap": "Provide weather info/ map.",
    "TextToSpeech_11Labs": "Generate realistic speech with voice ID.",
    "UnsplashImageSearch": "Search and retrieve beautiful images.",
    "TextToImage_FluxPro": "Generate Image from Text input",
    "MostModelTool": "Find famous HuggingFace models"
}
# -------------------- Layout --------------------
st.set_page_config(page_title="AgentPro AI", page_icon="🤖", layout="wide")
st.markdown("<div class='logo'>AgentPro AI Super Assistant - by Traversaal.ai & Radient Technologies</div>", unsafe_allow_html=True)

# -------------------- Sidebar Layout --------------------
st.sidebar.markdown("# 🛠️ Available Tools")

# -------------------- SIDEBAR Base Tools Section --------------------
st.sidebar.markdown('<div class="sidebar-section-header">📦 Base Tools</div>', unsafe_allow_html=True)
base_tools = [
    "ARES Web Search", "Quick Web Search", "CalculateTool",
    "UserInputTool", "YFinanceTool", "SlideGeneration", "TraversaalProRAG"
]
for tool in base_tools:
    with st.sidebar.expander(f"🔧 {tool}", expanded=False):
        st.markdown(tool_descriptions[tool])

# -------------------- SIDEBAR Custom Tools Section --------------------
st.sidebar.markdown('<div class="sidebar-section-header">🧪 Custom Tools</div>', unsafe_allow_html=True)
custom_tools = [
    "OpenWeatherMap", "TextToSpeech_11Labs", "UnsplashImageSearch", 
     "TextToImage_FluxPro", "MostModelTool"
]
for tool in custom_tools:
    with st.sidebar.expander(f"🔧 {tool}", expanded=False):
        st.markdown(tool_descriptions[tool])

# -------------------- Prompts Section --------------------
# tab1, = st.tabs(["🧾 Prompts"] )
# st.markdown("---")
# with tab1:
#     st.markdown("# Prompts For AI")
#     st.write("Here are some Prompts that can be used with AgentPro:")
#     st.markdown("""- 📌 Prompt 1: What is weather of Lahore, Islamabad, Moscow and CapeTown. 
#                                   Also show comparison tabe or chart
#                """)
#     st.markdown("- 📌 Prompt 2: She is the most powerful archon.")
#     st.markdown("- 📌 Prompt 3: Who is Raiden Shogun and is she the most powerful archon.")

# -------------------- Session Initialization --------------------
if "query" not in st.session_state:
    st.session_state.query = ""
if "response" not in st.session_state:
    st.session_state.response = None


# -------------------- Model and Tools Defining --------------------
model = create_model(provider="openai", model_name="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
tools = [
    QuickInternetTool(),
    CalculateTool(),
    UserInputTool(),
    YFinanceTool(),
    SlideGenerationTool(),
    AresInternetTool(api_key=os.getenv("ARES_API_KEY")),
    TraversaalProRAGTool(api_key=os.getenv("TRAVERSAAL_PRO_API_KEY"), document_names="employee_safety_manual"),
    MostModelTool(),
    UnsplashImageSearchTool(),
    TextToSpeechTool_ElevenLabsTTS(),
    WeatherMapTool_OpenWeather(),
    TextToImage_FluxProTool()
]
agent = ReactAgent(model=model, tools=tools)

# -------------------- CSS Styling of Streamlit Page & Sections --------------------
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(to right, #f4f7fa, #e9eff5);
}

/* Sidebar Tool Panel */
section[data-testid="stSidebar"] > div:first-child {
    background-color: #d9f1ff;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.06);
}

/* Sidebar section headers */
.sidebar-section-header {
    font-size: 16px;
    font-weight: bold;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    color: #1f77b4;
    border-bottom: 2px solid #1f77b4;
    padding-bottom: 0.25rem;
}

/* Shrink expander title and content inside the sidebar */
section[data-testid="stSidebar"] .st-expander {
    font-size: 12px !important;
    padding: 10px !important;
}

section[data-testid="stSidebar"] .st-expander > summary {
    font-size: 12px !important;
    padding: 8px 12px !important;
}

/* Inside expander content */
section[data-testid="stSidebar"] .stMarkdown {
    font-size: 11px !important;
    padding: 4px 10px !important;
    color: #333;
}

/* Chat Box */
textarea.stTextArea {
    font-size: 16px;
    min-height: 150px !important;
    border-radius: 12px;
}

/* Step Cards */
.step-box {
    padding: 1rem;
    margin: 1rem 0;
    background-color: #124577;
    border-radius: 5px;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.08);
}

.thought-box { background: #e7f0fd; border-left: 5px solid #1f77b4; }
.action-box { background: #fff4e6; border-left: 5px solid #ff9800; }
.observation-box { background: #e8f5e9; border-left: 5px solid #4caf50; }
.final-box { background: #f0fff4; border-left: 5px solid #2ecc71; font-weight: bold; font-size: 18px; }

/* Branding */
.stApp header {
    background: #1f77b4;
    color: white;
}

.logo {
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #1f77b4;
}
</style>
""", unsafe_allow_html=True)


# # -------------------- Query Input --------------------
# st.markdown("### Ask a Question")
# st.session_state.query = st.text_area("", value=st.session_state.query, label_visibility="collapsed")
# submit = st.button("🚀 Submit Query")

# #-----------------------Prompt Collapsable 2
# st.markdown("---")

# with st.expander("🧾 Prompts For AI"):
#     st.markdown("### Basic Prompts")
#     st.markdown("""- 📌 Prompt 1: What is weather of Lahore, Islamabad, Moscow and CapeTown.
#                                 Also show summary, comparison table chart and speech of final answer.
#                                 Also give powerpoint presentation on it.
#                 """
#                 )
#     st.markdown("- 📌 Prompt 2: Convert this text to image 'Cats and Dogs dancing in jungle'")
#     st.markdown("- 📌 Prompt 3: Fetch me and display famous pictures of 'historic sites'")
#     st.markdown("- 📌 Prompt 4: What is height of Effile Tower. And what is 1/4th of it.")

# -------------------- Query Input --------------------
st.markdown("### Ask a Question")
st.session_state.query = st.text_area("", value=st.session_state.query, label_visibility="collapsed")
submit = st.button("🚀 Submit Query")

# -------------------- Prompts --------------------
st.markdown("---")
with st.expander("🧾 Prompts For AI", expanded=False):  # Keep it always open
    st.markdown("### Basic Prompts")

    # Prompt 1
    prompt_1 = """What is the weather of Lahore, Islamabad, Moscow, and Cape Town?
    Also show a summary, comparison table chart, and speech of the final answer.
    Also give a PowerPoint presentation on it.
    Also give text to speech of final response."""
    st.markdown(f"**Prompt 1:** {prompt_1}")
    if st.button("📌 Use Prompt 1"):
        st.session_state.query = prompt_1

    # Prompt 2
    prompt_2 = "Convert this text to image: 'Cats and Dogs dancing in jungle'"
    st.markdown(f"**Prompt 2:** {prompt_2}")
    if st.button("📌 Use Prompt 2"):
        st.session_state.query = prompt_2

    # Prompt 3
    prompt_3 = "Fetch and display famous pictures of 'Historic Sites'"
    st.markdown(f"**Prompt 3:** {prompt_3}")
    if st.button("📌 Use Prompt 3"):
        st.session_state.query = prompt_3

    # Prompt 4
    prompt_4 = "What is the height of the Eiffel Tower? And what is 1/4th of it?"
    st.markdown(f"**Prompt 4:** {prompt_4}")
    if st.button("📌 Use Prompt 4"):
        st.session_state.query = prompt_4



# --- Function to detect and show files ---
def show_detected_files(response_text: str):
    #pattern = r'([\w\-. ]+\.(pptx|pdf|docx|xlsx|csv|txt|zip|json|png|jpg|jpeg|webp|mp4|mp3))'
    pattern = r'([\w\-/\\:. ]+\.(pptx|pdf|docx|xlsx|csv|txt|zip|json|png|jpg|jpeg|webp|mp4|mp3))'
    found_files = re.findall(pattern, response_text)

    shown = set()
    for match in found_files:
        filename = match[0]
        if filename not in shown and os.path.exists(filename):
            shown.add(filename)

            with open(filename, "rb") as f:
                file_data = f.read()

            st.markdown(f"""
            <div class="file-box">
                📄 <strong>{filename}</strong><br>
                Detected in response — you can download or open it.
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 2])
            with col1:
                st.download_button("⬇️ Download", file_data, file_name=filename)
            with col2:
                if st.button("🔍 Open", key=f"open_{filename}"):
                    st.session_state[f"open_file_{filename}"] = True

            # Display preview if open was clicked
            if st.session_state.get(f"open_file_{filename}", False):
                ext = filename.split(".")[-1].lower()
                st.markdown(f"##### Preview of `{filename}`:")

                if ext in ["png", "jpg", "jpeg", "webp"]:
                    st.image(file_data, use_column_width=True)
                elif ext == "pdf":
                    st.download_button("📄 Open PDF in New Tab", file_data, file_name=filename, mime="application/pdf")
                elif ext in ["txt", "json", "csv"]:
                    st.text(file_data.decode("utf-8")[:3000])  # limit preview
                elif ext in ["mp3", "wav"]:
                    st.audio(file_data, format=f"audio/{ext}")
                elif ext in ["mp4"]:
                    st.video(file_data)
                else:
                    st.info("File format preview not supported — please download to view.")

# -------------------- Agent Execution --------------------
if submit:
    with st.spinner("Thinking..."):
        st.session_state.response = agent.run(st.session_state.query)

# -------------------- Response Rendering --------------------
if st.session_state.response:
    response = st.session_state.response
    data = response.dict() if hasattr(response, "dict") else {}
    
    #---------------------------------- TABS
    tab1, tab2, tab3= st.tabs(["🧠 Formatted Response", "🧾 Raw Data", "🛠️ Debug Info"] )
    st.markdown("---")
    with tab1:
        st.markdown("## 🧠 Agent Thought Process")
        for step in data.get("thought_process", []):
            if step.get("thought"):
                st.markdown(f"<div class='step-box thought-box'><strong>Thought:</strong> {step['thought']}</div>", unsafe_allow_html=True)
            if step.get("action"):
                action = step["action"]
                st.markdown(f"<div class='step-box action-box'><strong>Action:</strong> {action['action_type']}<br><strong>Input:</strong> {action['input']}</div>", unsafe_allow_html=True)
            if step.get("observation"):
                obs = step.get("observation", {})
                obs_result = obs.get("result") if isinstance(obs, dict) else str(obs)
                st.markdown(f"<div class='step-box observation-box'><strong>Observation:</strong><br>{obs_result}</div>", unsafe_allow_html=True)

        if data.get("final_answer"):
            st.markdown("### ✅ Final Answer")
            st.markdown(f"<div class='step-box final-box'>{data['final_answer']}</div>", unsafe_allow_html=True)

    #---------------------------------- File Display
            # Combine all text from the response to search for filenames
            response_text_parts = []
            for step in data.get("thought_process", []):
                obs = step.get("observation", "")
                if isinstance(obs, dict):
                    response_text_parts.append(obs.get("result", ""))
                elif obs:
                    response_text_parts.append(str(obs))

            if data.get("final_answer"):
                response_text_parts.append(data["final_answer"])

            response_text = "\n".join(response_text_parts)
            show_detected_files(response_text)



        # Convert response to dict if possible
        data = response.dict() if hasattr(response, "dict") else {}


        with tab2:
            st.markdown("### 📦 Raw Response")
            st.write("🔍 Raw:", response)
            st.write("📦 Parsed Dict:", data)

        with tab3:
            st.markdown("### 🛠️ Debugging / Dev Tools")

            st.subheader("🧠 Agent Execution Summary")
            if "thought_process" in data:
                st.markdown(f"- Steps run: `{len(data['thought_process'])}`")
            if "final_answer" in data:
                st.markdown(f"- ✅ Final answer generated")

            # Tool usage trace
            tool_calls = [step for step in data.get("thought_process", []) if step.get("action")]
            if tool_calls:
                with st.expander("🧰 Tool Calls Trace"):
                    for i, step in enumerate(tool_calls, 1):
                        action = step["action"]
                        observation = step.get("observation", {}).get("result") if isinstance(step.get("observation"), dict) else step.get("observation")
                        st.markdown(f"""
                        **Step {i}:**  
                        🔧 **Tool:** `{action.get("action_type")}`  
                        📥 **Input:** `{action.get("input")}`  
                        📤 **Output:** `{observation}`
                        """)

            # Timing info
            if "metadata" in data and "duration" in data["metadata"]:
                st.subheader("⏱️ Timing Info")
                st.markdown(f"- Total duration: `{data['metadata']['duration']}s`")

            # Token usage
            if "usage" in data:
                st.subheader("🔢 Token Usage")
                st.markdown(f"- Prompt tokens: `{data['usage'].get('prompt_tokens', 'N/A')}`")
                st.markdown(f"- Completion tokens: `{data['usage'].get('completion_tokens', 'N/A')}`")
                st.markdown(f"- Total tokens: `{data['usage'].get('total_tokens', 'N/A')}`")

            # Full JSON
            with st.expander("📦 Full JSON Payload"):
                st.json(data)

            # Logs and generated code
            if "logs" in data:
                with st.expander("📜 Logs"):
                    st.code(data["logs"], language="text")
            if "code_snippet" in data:
                with st.expander("🧩 Generated Code"):
                    st.code(data["code_snippet"], language="python")

#--------------------------------LOG & EMAIL---------------------------

import yagmail
from datetime import datetime
import os

# --- Save query and response logs ---
if "interaction_log" not in st.session_state:
    st.session_state.interaction_log = []

if submit and st.session_state.response:
    log_lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_lines.append(f"---\nTimestamp: {timestamp}")
    log_lines.append(f"Query: {st.session_state.query}")

    for i, step in enumerate(data.get("thought_process", []), 1):
        log_lines.append(f"\nStep {i}:")
        if step.get("thought"):
            log_lines.append(f"Thought: {step['thought']}")
        if step.get("action"):
            action = step["action"]
            log_lines.append(f"Action: {action.get('action_type')} | Input: {action.get('input')}")
        if step.get("observation"):
            obs = step.get("observation", {})
            obs_result = obs.get("result") if isinstance(obs, dict) else str(obs)
            log_lines.append(f"Observation: {obs_result}")

    log_lines.append(f"\nFinal Answer: {data.get('final_answer', 'N/A')}")
    log_lines.append("---")
    st.session_state.interaction_log.append("\n".join(log_lines))

# --- Email Sending Form ---
st.markdown("---")
st.markdown("## 📧 Email Your Session Log")

with st.form("email_form"):
    recipient_email = st.text_input("Recipient Gmail Address")
    sender_email = st.text_input("Your Gmail Address")
    sender_password = st.text_input("Gmail App Password", type="password")
    send_email = st.form_submit_button("📤 Send Email")

    if send_email:
        if not st.session_state.interaction_log:
            st.warning("No log entries found. Submit at least one query first.")
        elif not (recipient_email and sender_email and sender_password):
            st.error("Please fill in all fields.")
        else:
            try:
                # Save log to file in current folder (with UTF-8 to support emojis)
                filename = f"agent_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                log_dir = os.path.join(os.getcwd(), "log")
                os.makedirs(log_dir, exist_ok=True)
                filepath = os.path.join(log_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("\n\n".join(st.session_state.interaction_log))

                # Send via Yagmail
                yag = yagmail.SMTP(user=sender_email, password=sender_password)
                yag.send(
                    to=recipient_email,
                    subject="🤖 Your AI Agent Interaction Log",
                    contents="Attached is the log from your Streamlit AI session.",
                    attachments=filepath
                )
                st.success(f"✅ Email successfully sent to {recipient_email}")
            except Exception as e:
                st.error(f"❌ Failed to send email: {str(e)}")
