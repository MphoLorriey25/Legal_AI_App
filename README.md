# LegalEase AI

LegalEase AI is a user-friendly web application that simplifies legal documents using artificial intelligence.  
Whether you're a student, entrepreneur, tenant, or small business owner, LegalEase AI helps you understand leases, contracts, and agreements without needing a law degree.

[Try the app live here!](https://legalaiapp-jrnucal5gcey3dswjkh6z8.streamlit.app/)

---

## Features

- Upload legal documents in TXT, PDF, or DOCX format.
- Ask specific questions or get a plain English summary.
- Translate explanations into multiple languages including English, Zulu, Xhosa, Afrikaans, French, Swahili, and Sesotho.
- Download the simplified explanation as a text file.
- Friendly and responsive UI with helpful guidance.
- Built with Streamlit and OpenRouter's GPT-3.5-turbo AI model.

---

## How to Use

1. Upload your legal document.
2. (Optional) Enter a specific question about the document.
3. Select the language you want the explanation in.
4. Click **Get Explanation**.
5. Read the simplified explanation.
6. Download the explanation if needed.
7. Check the FAQ section for tips.

---

## Installation & Running Locally

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/legalease-ai.git
   cd legalease-ai
````

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.streamlit/secrets.toml` file with your OpenRouter API key:

   ```toml
   OPENROUTER_API_KEY = "sk-or-your-api-key-here"
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

---

## Tech Stack

* [Streamlit](https://streamlit.io/) — Python web app framework for data apps
* [OpenRouter API](https://openrouter.ai/) — AI text generation powered by GPT-3.5-turbo
* [Deep Translator](https://github.com/nidhaloff/deep-translator) — For language translation
* PDF and DOCX text extraction utilities

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the app.

---

## License

This project is licensed under the MIT License.

---

## Contact

Built with ❤️ in Africa by Mpho Lorraine Ndou.

For questions or support, please contact: [lorrieym@gmail.com](mailto:lorrieym@gmail.com)

