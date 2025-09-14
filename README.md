# youtube_extractor_ai
![maxresdefault](https://github.com/user-attachments/assets/970c7170-90cd-400f-bc22-a206b72e24b8)



to run this project write this ... in the Terminal of Pycharm 

uvicorn youtube_app:app --reload
-------------------------------------------------------------------------
عالیه ✅
من می‌تونم برات یک فایل **README.md** برای پروژه روی گیت‌هاب آماده کنم، با توضیحات کامل، شیک، حرفه‌ای و پر از **ایموجی** و حتی پیشنهاد استفاده از **Badges و تصاویر گرافیکی**.

---

### 📄 نمونه README برای پروژه‌ات:

```markdown
# 🎬 YouTube Transcript Cinematic App  

🚀 An interactive **FastAPI + JavaScript** web app that extracts YouTube transcripts, generates SRT files, and lets you **ask AI-powered questions** about the transcript using **Google Gemini API**.  

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Gemini](https://img.shields.io/badge/Google-Gemini-green?style=for-the-badge&logo=google)
![YouTube](https://img.shields.io/badge/YouTube-Transcript-red?style=for-the-badge&logo=youtube)

---

## ✨ Features

- 🔗 **Extract YouTube transcript** from any video  
- 📜 **Auto-generate SRT subtitles**  
- 📄 **Download transcript** as `.txt` or `.srt`  
- 🤖 **Ask questions in Persian** powered by **Gemini API**  
- 🎨 Beautiful **animated UI** with RTL support & Persian `B Titr` font  

---

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) ⚡  
- **Frontend**: Vanilla JavaScript + HTML + CSS 🎨  
- **AI**: [Google Gemini API](https://ai.google.dev/) 🤖  
- **Transcripts**: [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/) 🎬  

---

## 📂 Project Structure

```

.
├── main.py          # FastAPI server
├── static/          # Static files (fonts, css, etc.)
│   └── BTitr.ttf    # Persian font
└── README.md        # Documentation

````

---

## ⚡ Installation & Usage

### 1️⃣ Clone the repo
```bash
git clone https://github.com/yourusername/youtube-transcript-app.git
cd youtube-transcript-app
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt`:

```txt
fastapi
uvicorn
httpx
youtube-transcript-api
```

### 3️⃣ Add your **Gemini API Key**

In `main.py`, replace:

```python
GEMINI_API_KEY = "YOUR_GEMINI_API"
```

### 4️⃣ Run the server

```bash
uvicorn main:app --reload
```

### 5️⃣ Open in browser

👉 Go to: `http://127.0.0.1:8000`

---

## 🎥 Demo

![App Preview](https://raw.githubusercontent.com/yourusername/youtube-transcript-app/main/demo.gif)

*(Replace with your own screenshot or screen-recording of the app)*

---

## 🧑‍💻 Example

1. Paste a YouTube link 🎬
2. Click **Get Transcript** 📜
3. Preview first 50 lines 🧐
4. Ask: *"این ویدیو درباره چیست؟"* 🤔
5. AI will answer in Persian ✅

---

## 🌍 Internationalization

* ✅ **Persian RTL support**
* ✅ Uses `B Titr` font for better readability
* 🌐 Can be extended to support other languages

---

## 🤝 Contributing

Pull requests are welcome!
If you’d like to add features (e.g., translation, export to PDF, etc.), feel free to open an issue first.

---

## 📜 License

MIT License © 2025 — Created with ❤️ by \[Your Name]

---

## ⭐ Support

If you like this project, **give it a star ⭐** on GitHub!

```

