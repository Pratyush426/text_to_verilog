import os
import re
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from google import genai
from google.genai import types

# ======= PAGE CONFIG =======
st.set_page_config(
    page_title="Text → Verilog Generator",
    page_icon="🔧",
    layout="wide"
)

# ======= LOAD API KEY =======
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ GEMINI_API_KEY not found. Please create a `.env` file with your key.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = (
    "You are a hardware code generator. Produce synthesizable Verilog-2001.\n"
    "- No inferred latches.\n"
    "- Use synchronous always blocks with nonblocking assignments.\n"
    "- Explicit reset behavior.\n"
    "Return ONLY code blocks fenced with ```verilog."
)

# ======= FUNCTIONS =======
def extract_verilog_blocks(text: str):
    return re.findall(r"```verilog\s+(.*?)```", text, flags=re.S)

def generate_verilog(spec: str):
    prompt = f"{SYSTEM_PROMPT}\n\nSpec: {spec}"
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )
    blocks = extract_verilog_blocks(response.text or "")
    return blocks

def save_code(blocks, filename="design.v"):
    Path("out").mkdir(exist_ok=True)
    file_path = Path("out") / filename
    file_path.write_text(blocks[0])
    return file_path

# ======= SIDEBAR =======
st.sidebar.title("📌 Instructions")
st.sidebar.write("""
1. Enter your Verilog module specification.
2. Click **Generate Verilog**.
3. View generated code and download the file.
""")

# ======= TABS =======
tab1, tab2 = st.tabs(["📝 Generator", "📜 History"])

# Initialize history in session
if "history" not in st.session_state:
    st.session_state.history = []

# ======= GENERATOR TAB =======
with tab1:
    st.title("🔧 Text-to-Verilog Code Generator")

    # Use columns for input and output
    col1, col2 = st.columns(2)

    with col1:
        spec = st.text_area(
            "Enter your module specification:",
            height=150,
            placeholder="e.g., 8-bit synchronous up-counter with async reset"
        )
        if st.button("Generate Verilog"):
            if not spec.strip():
                st.error("Please enter a specification first.")
            else:
                with st.spinner("Generating Verilog code..."):
                    try:
                        blocks = generate_verilog(spec)
                        if not blocks:
                            st.error("⚠️ No Verilog code found. Try refining your spec.")
                        else:
                            verilog_code = blocks[0]

                            # Save to session history
                            st.session_state.history.append({
                                "spec": spec,
                                "verilog": verilog_code
                            })

                            # Save file
                            file_path = save_code(blocks, "design.v")

                            with open(file_path, "rb") as f:
                                st.download_button(
                                    "⬇️ Download Verilog File",
                                    f,
                                    file_name="design.v"
                                )

                            st.success("✅ Verilog code generated successfully!")

                    except Exception as e:
                        st.error(f"Error: {e}")

    with col2:
        if st.session_state.history:
            st.subheader("Generated Verilog Code Preview")
            last_entry = st.session_state.history[-1]
            st.code(last_entry["verilog"], language="verilog")

# ======= HISTORY TAB =======
with tab2:
    st.title("📜 Your History")
    if not st.session_state.history:
        st.info("No history yet. Generate something first!")
    else:
        for i, entry in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"**{i}. Spec:** {entry['spec']}")
            st.code(entry['verilog'], language="verilog")
            st.divider()

# ======= CUSTOM CSS =======
st.markdown("""
<style>
.stButton>button {
    background-color: #007bff;
    color: white;
    border-radius: 10px;
}
.stTextArea textarea {
    font-family: monospace;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)