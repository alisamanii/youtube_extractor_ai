from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
import re
import httpx

app = FastAPI()
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
# کلید Gemini
GEMINI_API_KEY = "YOUR_GEMINI_API"


def extract_video_id(url: str) -> str:
    patterns = [r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"]
    for p in patterns:
        match = re.search(p, url)
        if match:
            return match.group(1)
    return url


@app.get("/", response_class=HTMLResponse)
async def index():
    return INDEX_HTML


@app.post("/api/transcript")
async def api_transcript(req: Request):
    data = await req.json()
    url = data.get("url", "")
    video_id = extract_video_id(url)

    try:
        yt = YouTubeTranscriptApi()
        transcript = yt.fetch(video_id)
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})

    # ساخت متن ساده و فایل SRT
    finaltext = " ".join([i.text for i in transcript])
    srt_lines = []
    for idx, t in enumerate(transcript, start=1):
        start = t.start
        dur = t.duration
        end = start + dur

        def fmt(secs):
            h = int(secs // 3600)
            m = int((secs % 3600) // 60)
            s = int(secs % 60)
            ms = int((secs - int(secs)) * 1000)
            return f"{h:02}:{m:02}:{s:02},{ms:03}"

        srt_lines.append(f"{idx}\n{fmt(start)} --> {fmt(end)}\n{t.text}\n")
    srt_text = "\n".join(srt_lines)

    return {
        "ok": True,
        "text": finaltext,
        "srt": srt_text,
        "preview": [
            {
                "start": round(t.start, 2),
                "duration": round(t.duration, 2),
                "text": t.text,
            }
            for t in transcript[:50]
        ],
    }


@app.post("/api/ask")
async def ask_question(req: Request):
    data = await req.json()
    question = data.get("question", "")
    transcript = data.get("transcript", "")

    if not question or not transcript:
        return JSONResponse({"ok": False, "error": "سوال یا متن وجود ندارد."})

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": f"متن زیر استخراج شده از یوتیوب است:\n\n{transcript}\n\nسوال کاربر به فارسی: {question}\n\nفقط بر اساس همین متن پاسخ بده و اگر در متن نبود بگو «در متن موجود نیست»."
                                }
                            ]
                        }
                    ]
                },
            )
            result = response.json()
            answer = (
                result.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            return {"ok": True, "answer": answer}
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})


# ------------------------
# UI HTML/JS
# ------------------------
INDEX_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>🎬 YouTube Transcript Cinematic App</title>
<style>

@font-face {
  font-family: 'BTitr';
  src: url('/static/BTitr.ttf') format('truetype');
}

#output,
#question,
#answerBox {
  direction: rtl;
  text-align: right;
  font-family: 'BTitr', sans-serif;
}

/* Reset */
*{margin:0;padding:0;box-sizing:border-box;}
html,body{height:100%;font-family:'Segoe UI',sans-serif;overflow-x:hidden;}

/* Background Animation */
body {
  background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
  background-size: 400% 400%;
  animation: gradientShift 20s ease infinite;
  color: #fff;
  text-align:center;
  padding:40px;
  perspective: 1500px;
}
@keyframes gradientShift {
  0%{background-position:0% 50%;}
  50%{background-position:100% 50%;}
  100%{background-position:0% 50%;}
}

/* Heading */
h1 {
  font-size:3em;
  margin-bottom:30px;
  letter-spacing:2px;
  color:#fff;
  text-shadow:0 0 15px #ff4b2b,0 0 30px #ff416c,0 0 50px #ff4b2b;
  animation: fadeInDown 1.5s ease;
}
@keyframes fadeInDown {
  from{opacity:0;transform:translateY(-50px);}
  to{opacity:1;transform:translateY(0);}
}

/* Input */
input {
  width:60%;
  padding:12px 18px;
  border-radius:15px;
  background:rgba(255,255,255,0.1);
  border:1px solid rgba(255,255,255,0.3);
  color:#fff;
  backdrop-filter:blur(8px);
  text-align:center;
  transition:transform .3s,box-shadow .3s;
}
input:focus {
  outline:none;
  transform:scale(1.05);
  box-shadow:0 0 15px rgba(255,255,255,0.3);
}
input::placeholder{color:#ddd;}

/* Buttons */
button {
  padding:12px 18px;
  margin:8px;
  border:none;
  border-radius:15px;
  font-size:16px;
  font-weight:bold;
  cursor:pointer;
  color:#fff;
  background:linear-gradient(45deg,#ff4b2b,#ff416c);
  box-shadow:0 5px 20px rgba(255,65,108,0.6);
  transition:transform .3s,box-shadow .3s;
}
button:hover {
  transform:translateY(-4px) scale(1.1) rotateX(10deg);
  box-shadow:0 10px 30px rgba(255,65,108,0.8);
}

/* Status */
#status {
  margin-top:15px;
  font-style:italic;
  color:#ff0;
  text-shadow:0 0 8px rgba(255,255,0,0.8);
  animation:pulse 2s infinite;
}
@keyframes pulse {
  0%,100%{opacity:1;}
  50%{opacity:0.6;}
}

/* Output Box */
#output {
  white-space:pre-wrap;
  text-align:left;
  margin:20px auto;
  max-width:850px;
  background:rgba(255,255,255,0.08);
  border:1px solid rgba(255,255,255,0.2);
  padding:25px;
  border-radius:20px;
  backdrop-filter:blur(12px);
  box-shadow:0 0 40px rgba(0,0,0,0.5), inset 0 0 20px rgba(255,255,255,0.1);
  transform:rotateX(3deg) rotateY(-3deg);
  transition:transform .6s ease;
  animation:fadeIn 1.5s ease;
}
#output:hover {
  transform:rotateX(0deg) rotateY(0deg) scale(1.03);
}

/* Preview */
#previewWrap h2 {
  font-size:1.8em;
  margin:20px 0;
  text-shadow:0 0 15px #0ff;
}
table {
  margin:0 auto;
  border-collapse:collapse;
  color:#fff;
  width:80%;
}
td {
  padding:8px 12px;
  border-bottom:1px solid rgba(255,255,255,0.2);
  text-align:left;
  animation:slideIn .8s ease;
}
@keyframes slideIn {
  from{opacity:0;transform:translateX(-50px);}
  to{opacity:1;transform:translateX(0);}
}

/* Controls Container */
.controls{margin:20px;}
.hidden{display:none;}

/* Pop In Animation */
input,button,#output {
  animation:popIn 1s ease;
}
@keyframes popIn {
  from{opacity:0;transform:scale(.9);}
  to{opacity:1;transform:scale(1);}
}

/* Mouse Parallax Effect */
body::after {
  content:'';
  position:fixed;
  top:-50%;
  left:-50%;
  width:200%;
  height:200%;
  background:radial-gradient(circle,#ffffff15 1px,transparent 1px);
  background-size:50px 50px;
  transform:translateZ(-500px) scale(2);
  pointer-events:none;
}
</style>
</head>
<body>
<h1>🎬 YouTube Transcript Extractor</h1>
<input type="text" id="yturl" size="50" placeholder="Paste YouTube URL here">
<div class="controls">
  <button id="go">Get Transcript</button>
  <button id="demo">Demo</button>
  <button id="copy">Copy</button>
  <button id="downloadTxt">Download TXT</button>
  <button id="downloadSrt">Download SRT</button>
  <button id="clear">Clear</button>
</div>
<div id="status">Idle...</div>
<div id="previewWrap" class="hidden">
  <h2>Preview</h2>
  <table id="previewTbl"></table>
</div>
<div id="output"></div>

<!-- بخش جدید Q&A -->
<div id="qaBox">
  <h2>❓ پرسش از متن</h2>
  <textarea id="question" rows="3" style="width:80%;padding:10px;border-radius:10px;"></textarea><br>
  <button id="ask">بپرس</button>
  <div id="answerBox" style="margin-top:15px;text-align:right;background:rgba(0,0,0,0.4);padding:15px;border-radius:10px;"></div>
</div>

<script>
/* Same JS Logic */
const $ = sel => document.querySelector(sel);
const outputEl = $('#output');
const previewTbl = $('#previewTbl');
const previewWrap = $('#previewWrap');
const statusEl = $('#status');
window.__lastText = '';
window.__lastSrt = '';

function setStatus(msg, good=false){
  statusEl.textContent = msg;
  statusEl.style.color = good ? '#0f0' : '#ff0';
}

async function fetchTranscript(){
  const url = $('#yturl').value.trim();
  if(!url){ setStatus('Please enter a URL'); return; }
  setStatus('Fetching...');
  try{
    const res = await fetch('/api/transcript',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({url})
    });
    const data = await res.json();
    if(!data.ok){ setStatus('Error: '+data.error); return; }
    window.__lastText = data.text;
    window.__lastSrt = data.srt;
    outputEl.textContent = data.text;
    setStatus('Done!',true);

    // Fill preview
    previewTbl.innerHTML='';
    if(data.preview && data.preview.length){
      previewWrap.classList.remove('hidden');
      for(const row of data.preview){
        const tr=document.createElement('tr');
        tr.innerHTML=`<td>${row.start}s</td><td>${row.text}</td>`;
        previewTbl.appendChild(tr);
      }
    }
  }catch(err){
    setStatus('Error: '+err.message);
  }
}

function copyText(){
  const text = window.__lastText || outputEl.textContent || '';
  if(!text){ setStatus('Nothing to copy.'); return; }
  navigator.clipboard.writeText(text).then(() => setStatus('Copied!',true));
}

function download(filename, content){
  const blob=new Blob([content],{type:'text/plain;charset=utf-8'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');
  a.href=url;a.download=filename;a.click();
  setTimeout(()=>URL.revokeObjectURL(url),2000);
}

async function askQuestion(){
  const question = $('#question').value.trim();
  if(!question){ setStatus('سوالی وارد کنید'); return; }
  if(!window.__lastText){ setStatus('اول متن استخراج کنید'); return; }

  setStatus('در حال پرسش...');
  try{
    const res = await fetch('/api/ask',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        question,
        transcript: window.__lastText
      })
    });
    const data = await res.json();
    if(!data.ok){ setStatus('Error: '+data.error); return; }
    $('#answerBox').textContent = data.answer;
    setStatus('پاسخ آماده شد ✅', true);
  }catch(err){
    setStatus('Error: '+err.message);
  }
}

$('#go').addEventListener('click', fetchTranscript);
$('#demo').addEventListener('click', () => {
  $('#yturl').value='https://www.youtube.com/watch?v=NEG9lafbzvI';
  fetchTranscript();
});
$('#copy').addEventListener('click', copyText);
$('#downloadTxt').addEventListener('click', () => {
  const text=window.__lastText||outputEl.textContent||'';
  if(!text){ setStatus('Nothing to download.'); return; }
  download('transcript.txt', text);
});
$('#downloadSrt').addEventListener('click', () => {
  const srt=window.__lastSrt||'';
  if(!srt){ setStatus('No SRT available.'); return; }
  download('subtitles.srt', srt);
});
$('#clear').addEventListener('click', () => {
  outputEl.textContent='';
  previewTbl.innerHTML='';
  previewWrap.classList.add('hidden');
  setStatus('Cleared.');
});
$('#ask').addEventListener('click', askQuestion);
</script>
</body>
</html>
"""
