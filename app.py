import os
import re
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()  # loads .env from same folder
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


st.set_page_config(page_title="Text → Verilog Generator", layout="centered")
st.title("🔧 Text-to-Verilog Code Generator (Google Gemini)")

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
                    st.subheader("Generated Verilog Code")
                    st.code(verilog_code, language="verilog")

                    file_path = save_code(blocks, "design.v")
                    with open(file_path, "rb") as f:
                        st.download_button(
                            "⬇️ Download Verilog File", 
                            f, 
                            file_name="design.v"
                        )
            except Exception as e:
                st.error(f"Error: {e}")
