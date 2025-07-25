import streamlit as st
import requests
from deep_translator import GoogleTranslator
from utils.file_parser import extract_text_from_file

# Page config
st.set_page_config(page_title="LegalEase AI", page_icon="📄")

# Branding Header
col1, col2 = st.columns([1, 6])
with col1:
    st.image("assets/logo.png", width=80)
with col2:
    st.markdown("<h1 style='margin-top: 20px;'>LegalEase AI</h1>", unsafe_allow_html=True)

# Description with padding
st.markdown("""
<div style='text-align: center; font-size: 17px; margin-bottom: 30px;'>
LegalEase AI is your personal legal assistant powered by artificial intelligence.  
Whether you're a student, entrepreneur, tenant, or small business owner — understanding legal documents shouldn't require a law degree.

Just upload a lease, contract, or agreement and get a clear, simple explanation in your own language.  
Ask questions like "What are my rights?" or "What happens if I cancel?" — and get answers instantly.

Legal language is often designed to confuse. LegalEase AI exists to simplify, empower, and inform.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Upload and Language Selection side-by-side
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("<h3>📎 Upload Your Legal Document</h3>", unsafe_allow_html=True)
    file = st.file_uploader("", type=["txt", "pdf", "docx"])
with col2:
    st.markdown("<h3>🌐 Translate Explanation To</h3>", unsafe_allow_html=True)
    languages = {
        "English 🇬🇧": "en",
        "Zulu 🇿🇦": "zu",
        "Xhosa 🇿🇦": "xh",
        "Afrikaans 🇿🇦": "af",
        "French 🇫🇷": "fr",
        "Swahili 🇰🇪": "sw",
        "Sesotho 🇿🇦": "st",
    }
    selected_language = st.selectbox("", list(languages.keys()))

st.markdown("<br>", unsafe_allow_html=True)  # spacing

# Question input with helper text
question = st.text_area(
    "❓ Ask a question (optional)",
    placeholder="e.g., What if I cancel early?",
    max_chars=300,
    help="Ask anything about the document or leave blank for a summary."
)

st.markdown("<br>", unsafe_allow_html=True)  # spacing

# Explanation button styled below
if st.button("🧠 Get Explanation"):
    if file:
        with st.spinner("⏳ Processing your document and generating explanation..."):
            try:
                extracted_text = extract_text_from_file(file)
                prompt = f"{extracted_text}\n\n{question or 'Summarize this in plain English.'}"

                api_key = st.secrets.get("OPENROUTER_API_KEY", "")

                if not api_key:
                    st.error("⚠️ OpenRouter API key not found. Please set OPENROUTER_API_KEY in secrets.")
                else:
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": "openai/gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": prompt}]
                    }
                    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                    data = res.json()

                    if 'choices' in data and data['choices']:
                        reply = data['choices'][0]['message']['content']
                        dest_code = languages[selected_language]

                        # Translation
                        if dest_code != "en":
                            translated = GoogleTranslator(source='auto', target=dest_code).translate(reply)
                            st.success(f"✅ Explanation ({selected_language}):")
                            st.write(translated)
                        else:
                            st.success("✅ Explanation:")
                            st.write(reply)

                        # Save explanation for download (Step 10)
                        st.download_button(
                            label="💾 Download Explanation as TXT",
                            data=reply,
                            file_name="legalease_explanation.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("⚠️ Unexpected API response.")
                        st.code(data)

            except Exception as e:
                st.error("⚠️ Something went wrong.")
                st.code(str(e))
    else:
        st.warning("⚠️ Please upload a document.")

st.markdown("---")

# FAQ / Help Section (Step 9)
with st.expander("❓ How to use LegalEase AI?"):
    st.write("""
    1. Upload a legal document (PDF, DOCX, or TXT).  
    2. Optionally ask a specific question about the document.  
    3. Select the language you want the explanation in.  
    4. Click 'Get Explanation' and wait for results.  
    5. Download the explanation for your records.  
    """)

# Footer
st.markdown(
    "<div style='text-align: center; color: grey; font-size: small;'>"
    "💡 <em>“AI won't replace lawyers, but it will empower more people to understand the law.”</em><br>"
    "© 2025 LegalEase AI — Built with ❤️ in Africa to simplify legal understanding for all."
    "</div>", unsafe_allow_html=True
)

# Inject custom CSS (Step 5)
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    /* Add spacing below the footer */
    footer {margin-top: 40px;}
    </style>
    """, unsafe_allow_html=True
)
