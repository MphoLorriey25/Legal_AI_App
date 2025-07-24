import streamlit as st
import requests
import os
from deep_translator import GoogleTranslator
from utils.file_parser import extract_text_from_file

# -------------------- Page Config --------------------
st.set_page_config(page_title="LegalEase AI", page_icon="📄")

# -------------------- Branding --------------------
col1, col2 = st.columns([1, 6])
with col1:
    st.image("assets/logo.png", width=80)
with col2:
    st.markdown("<h1 style='margin-top: 20px;'>LegalEase AI</h1>", unsafe_allow_html=True)

# -------------------- Description --------------------
st.markdown("""
<div style='text-align: center; font-size: 17px;'>
LegalEase AI is your personal legal assistant powered by artificial intelligence.  
Whether you're a student, entrepreneur, tenant, or small business owner — understanding legal documents shouldn't require a law degree.

Just upload a lease, contract, or agreement and get a clear, simple explanation in your own language.  
Ask questions like "What are my rights?" or "What happens if I cancel?" — and get answers instantly.

Legal language is often designed to confuse. LegalEase AI exists to simplify, empower, and inform.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -------------------- Upload Section --------------------
file = st.file_uploader("📎 Upload a Legal Document", type=["txt", "pdf", "docx"])
question = st.text_area("❓ Ask a question (optional)", placeholder="e.g., What if I cancel early?")

# -------------------- Language Selection --------------------
languages = {
    "English 🇬🇧": "en",
    "Zulu 🇿🇦": "zu",
    "Xhosa 🇿🇦": "xh",
    "Afrikaans 🇿🇦": "af",
    "French 🇫🇷": "fr",
    "Swahili 🇰🇪": "sw",
    "Sesotho 🇿🇦": "st",
}

selected_language = st.selectbox("🌐 Translate Explanation To", list(languages.keys()))

# -------------------- Explanation Button --------------------
if st.button("🧠 Get Explanation"):
    if file:
        with st.spinner("⏳ Processing..."):
            try:
                extracted_text = extract_text_from_file(file)
                prompt = f"{extracted_text}\n\n{question or 'Summarize this in plain English.'}"

                api_key = os.getenv("OPENROUTER_API_KEY", st.secrets.get("OPENROUTER_API_KEY", ""))

                if not api_key:
                    st.error("⚠️ OpenRouter API key not found. Please set OPENROUTER_API_KEY.")
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

                        # Translate if needed
                        dest_code = languages[selected_language]
                        if dest_code != "en":
                            translated = GoogleTranslator(source='auto', target=dest_code).translate(reply)
                            st.success(f"✅ Explanation ({selected_language}):")
                            st.write(translated)
                        else:
                            st.success("✅ Explanation:")
                            st.write(reply)
                    else:
                        st.error("⚠️ Unexpected API response.")
                        st.code(data)

            except Exception as e:
                st.error("⚠️ Something went wrong.")
                st.code(str(e))
    else:
        st.warning("⚠️ Please upload a document.")

st.markdown("---")

# -------------------- Footer --------------------
st.markdown(
    "<div style='text-align: center; color: grey; font-size: small;'>"
    "💡 <em>“AI won't replace lawyers, but it will empower more people to understand the law.”</em><br>"
    "© 2025 LegalEase AI — Built with ❤️ in Africa to simplify legal understanding for all."
    "</div>", unsafe_allow_html=True
)
