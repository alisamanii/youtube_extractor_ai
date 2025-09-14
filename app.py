from youtube_transcript_api import YouTubeTranscriptApi

yt=YouTubeTranscriptApi()

inp="https://www.youtube.com/watch?v=NEG9lafbzvI"
x=inp.replace("https://www.youtube.com/watch?v=","")

tr=yt.fetch(x)

finaltext=""
for i in tr:
    print(i.text)
    finaltext+=i.text

with open("finaltext.txt","w",encoding='utf-8') as f:
    f.write(finaltext)

#uvicorn youtube_app:app --reload
