import streamlit as st
import streamlit as st
from pytube import YouTube
import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import split_on_silence
#from gtts import gTTS, gTTSError   
#from deep_translator import GoogleTranslator
from googletrans import Translator
import streamlit.components.v1 as components 
#from io import StringIO,BytesIO
import os
#import re


directory= 'downloads/'
if not os.path.exists(directory):
    os.makedirs(directory)

st.set_page_config(page_title="Thong-Thao 20-11-23 ", page_icon="🚀", layout="centered", )     
st.markdown(f"""
            <style>
            .stApp {{background-image: linear-gradient(0deg,white,yellow);
            background-attachment: fixed;
            background-size: cover}}
        </style>
         """, unsafe_allow_html=True)


#3.2.1
@st.cache_data
def get_large_audio_transcription(path):
    sound = AudioSegment.from_wav(path)  
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    r = sr.Recognizer()
    
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
                #fh.write(txt + "\n") 
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text+'\n'

    return whole_text


@st.cache_data
def Dem_txtbig_vao_html(fulltxt):
    ltext = fulltxt.split('.')
    chp='<br><br>'
    for text in ltext:
        strcau=text+". "
        chp=chp+'<div class="f-grid">'+strcau+'</div>'   

    js1='''
        function googleTranslateElementInit(){new google.translate.TranslateElement({pageLanguage:'en'}, 'google_translate_element');}
        '''
    js2='''
        src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"
        '''
    js3='''
        function speak_text_all(idname){
        //  khoi dong text_all la bien gloabal  
        var text_all='';
        //dem vao list 
        const nodeList = document.querySelectorAll(".f-grid");
        // duyet list da lay
        for (let i = 0; i < nodeList.length; i++) {
            text_all = text_all + nodeList[i].innerText + '. ' ;
        }
        //alert(text_all);
        const utterance = new SpeechSynthesisUtterance(text_all);
        let giongnoi='en-US';
        if (idname.charAt(0) == 'English'){giongnoi='en-US';} else {giongnoi='vi-VN';}
        utterance.lang = giongnoi;
        window.speechSynthesis.speak(utterance);
        }    
        '''
    js4='''
        function stop() {
                window.speechSynthesis.cancel();
        }
        '''
    js5='''
        function copyToClipboard() {
            if (document.selection) { 
                var range = document.body.createTextRange();
                range.moveToElementText(document.getElementById('results'));
                range.select().createTextRange();
                document.execCommand("copy"); 
        
            } else if (window.getSelection) {
                var range = document.createRange();
                range.selectNode(document.getElementById('results'));
                window.getSelection().addRange(range);
                document.execCommand("copy");
            }
            //console.log('da copy');
        }
        '''
    sty='''
        .f-grid {
            display: flex;
            justify-content: space-between;
            margin-left: 0.0rem;
            flex-flow: row wrap;
            font-size: 20px; }
        '''
    components.html(f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Tiensg89's App</title>
                <style> {sty} </style>
                </head>
                <body>
                <div id="google_translate_element" ></div>
                <script>{js1}</script>
                <script {js2}></script>
                <hr>
                <div id="results">
                {chp}
                </div>
                <hr>
                <button id="English" onclick="speak_text_all(this.id)">Speak with English voice</button>
                <button id="Vietnamese" onclick="speak_text_all(this.id)">Speak with Vietnamese voice</button>
                <script>{js3}</script>
                <br><br>
                <button id="stop" onclick="stop()">Stop</button>
                <button onclick="copyToClipboard()">Copy</button>
                <button onclick="history.back()">Go back</button>

                <script>{js4}</script>
                <script>{js5}</script>
                <br><br>
                </body>
                </html>
                """,height=900,scrolling=True)

@st.cache_data
def Xu_li_speech2text(path_filename,codelang1):
    tepvideo=os.path.basename(path_filename)
    clip = mp.VideoFileClip(tepvideo)
    tepwav = tepvideo.replace('.mp4', '.wav') 
    clip.audio.write_audiofile(tepwav)
    tepout = tepwav.replace('.wav', '.txt') 
    tieude = youtubeObject.title + ' . '
    
    #with sr.AudioFile(tepwav) as source:
    #    r = sr.Recognizer()
    fulltxt = get_large_audio_transcription(tepwav)
    fulltxt=tieude+fulltxt
    # Save vao tep resultf.txt roi dich tep nay
    #fulltxt = youtubeObject.title + '.' + fulltxt
    lresult = fulltxt.split(".")
    teplsource='resultf.txt'
    with open(teplsource, 'w+') as fluu:
        for lr in lresult: 
            fluu.write(lr + '. \n')
    #st.write(fulltxt.replace('.','.\n\n'))
    st.write(len(fulltxt))
    Dem_txtbig_vao_html(fulltxt)
        


##################################################################################
st.title(":green[Speech :open_mouth: in Video to Text] 📝")   #
url=''


url_of_youtube = st.text_input('Nhập URL của youtube rồi Enter. Ví dụ : https://www.youtube.com/watch?v=Z2iXr8On3LI',key='IP1')
if url_of_youtube != '':
    youtubeObject = YouTube(url_of_youtube)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
        file_name = youtubeObject.default_filename
        #st.write(':blue[Download is completed successfully with file named : ] '+file_name)
    except:
        print("An error has occurred")

    Xu_li_speech2text(file_name,codelang1='en')
    st.success('Converting Complete', icon="✅")
    st.balloons()

