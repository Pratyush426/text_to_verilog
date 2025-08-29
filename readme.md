# 🔧 Text-to-Verilog Code Generator (Google Gemini)

This project is a **Streamlit-based AI assistant** that converts **natural language specifications into synthesizable Verilog-2001 code** using **Google Gemini (Generative AI)**.  
It helps **hardware engineers, FPGA developers, and digital design students** quickly prototype and generate RTL designs with industry-standard coding practices.  

---

## 🚀 Features

- 📝 **Natural Language to Verilog** – Describe a hardware spec in plain English, get **synthesizable Verilog-2001** code.  
- ✅ **Safe RTL Practices** – Generated code follows:
  - No inferred latches  
  - Synchronous always blocks with nonblocking assignments  
  - Explicit reset behavior  
- 📂 **Downloadable Code** – Save generated Verilog into `design.v` automatically.  
- ⚡ **Fast & Interactive** – Runs in the browser with **Streamlit** UI.  
- 🔑 **Secure API Access** – API keys managed via `.env` file.  

---

## 🛠️ Tech Stack

- **Python 3.10+**  
- [Streamlit](https://streamlit.io/) – UI for interaction  
- [Google Generative AI](https://ai.google.dev/) – Gemini model for code generation  
- [dotenv](https://pypi.org/project/python-dotenv/) – Environment variable management  
- [Regex](https://docs.python.org/3/library/re.html) – Extract Verilog blocks from responses  

---

## 📂 Project Pipeline

1. **Specification Input** – User enters hardware spec (e.g., *“8-bit synchronous up-counter with async reset”*).  
2. **Prompt Engineering** – System prompt enforces safe RTL rules and Verilog-2001 standards.  
3. **Gemini LLM** – Google’s Gemini 2.5 Flash model generates Verilog code.  
4. **Code Extraction** – Regex filters ` ```verilog ... ``` ` fenced code blocks.  
5. **File Export** – Generated code is saved into `out/design.v` and available for download.  
6. **Streamlit UI** – Display code with syntax highlighting & download option.  

---

## ⚡ Quickstart

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/your-username/text-to-verilog-generator.git
cd text-to-verilog-generator
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up Environment Variables

Create a `.env` file in the root directory with your **Google Gemini API key**:

```bash
GEMINI_API_KEY=your_api_key_here
```

### 4️⃣ Run the App

```bash
streamlit run app.py
```

### 5️⃣ Generate Verilog

* Enter your specification in the text area.
* Click **"Generate Verilog"**.
* View the generated code, copy it, or download as `design.v`.
