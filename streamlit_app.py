# -*- coding: utf-8 -*-
# https://tien89.streamlit.app/     # up ngay 15-11-2023

import streamlit as st
from pytube import YouTube
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from googletrans import Translator 
from io import StringIO
import os
import time
import streamlit.components.v1 as components 

# 1 -------------------------
def Download_youtube(choice):
    st.subheader(choice)
    url_of_youtube = st.text_input('Nhập URL của youtube. ( Ví dụ : https://www.youtube.com/watch?v=Z2iXr8On3LI ) rồi Enter:',)
    if url_of_youtube !='':
        youtubeObject = YouTube(url_of_youtube)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        n_bytes=youtubeObject.filesize
        st.write(n_bytes)
        folder_name = "videos"
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        try:
            youtubeObject.download(folder_name)
            file_name = youtubeObject.default_filename
            st.write(':blue[Download is completed successfully with file named : ] '+file_name)
        except:
            print("An error has occurred")
        st.write('---')

# 2 ---------------------
def Browse_video(choice):
    st.subheader(choice)
    uploaded_file = st.file_uploader('Chọn tệp mp4 muốn xem',type=['mp4'])
    if uploaded_file is not None:
        st.video(uploaded_file)
    st.write('---')

def Xu_li_speech2text(path_filename):
    tepvideo=os.path.basename(path_filename)
    clip = mp.VideoFileClip(tepvideo)
    tepwav = tepvideo.replace('.mp4', '.wav') 
    clip.audio.write_audiofile(tepwav)
    tepout = tepwav.replace('.wav', '.txt') 
    fulltxt=''
    with sr.AudioFile(tepwav) as source:
        r = sr.Recognizer()
        fulltxt = get_large_audio_transcription(tepwav, r)
        ltext = fulltxt.split('.')
        chp=''
        for text in ltext:
          chp=chp+'<div class="f-grid">'+text+'</div>'   
        #with open(tepout, encoding = 'utf-8', mode='w+') as fh:    
            #fh.write(fulltxt)
            #os.startfile(tepout)
            #st.write(fulltxt)
        js1='''
            function googleTranslateElementInit(){new google.translate.TranslateElement({pageLanguage:'en'}, 'google_translate_element');}
            '''
        js2='''
            src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"
            '''
        sty='''
            .f-grid {
                display: flex;
                justify-content: space-between;
                margin-left:-0.5rem;
                flex-flow: row wrap;}
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
                    {chp}
                    </body>
                    </html>
                    """,width=600, height=900, scrolling=True)
                    
        #components.html(html_str, unsafe_allow_html=True)

        #st.markdown(html_str, unsafe_allow_html=True)


# 3 -----------------------------
def Speech_invid_to_text(choice):
    st.subheader(choice)
    opption_chon = st.radio(":green[Chọn một nguồn:]", [":red[lấy tệp mp4 trong máy]",":blue[lấy tệp mp4 từ URL]"],index=1,horizontal=True ) 
    if opption_chon==":red[lấy tệp mp4 trong máy]":
        uploaded_file = st.file_uploader('Chọn tệp mp4 trong máy muốn lấy',type=['mp4'])
        if uploaded_file is not None:
            filename = uploaded_file.name
            #transcription(stt_tokenizer, stt_model, filename, uploaded_file)
            #st.subheader(filename)
            with open(os.path.join("",filename),"wb") as f: 
                f.write(uploaded_file.getbuffer())         
                #st.success("Saved File")
            #with st.spinner(':red[Wait for converting speech to text...]'):
            Xu_li_speech2text(filename)
            #time.sleep(0.5)
            #st.success('Done!')

    else:
        url_of_youtube = st.text_input('Nhập URL của youtube. ( Ví dụ : https://www.youtube.com/watch?v=Z2iXr8On3LI ) rồi Enter:',)
        if url_of_youtube != '':
            youtubeObject = YouTube(url_of_youtube)
            youtubeObject = youtubeObject.streams.get_highest_resolution()
            #n_bytes=youtubeObject.filesize
            #st.write(n_bytes)
            #folder_name = "videos"
            #if not os.path.isdir(folder_name):
            #    os.mkdir(folder_name)
            try:
                #youtubeObject.download(folder_name)
                youtubeObject.download()
                file_name = youtubeObject.default_filename
                st.write(':blue[Download is completed successfully with file named : ] '+file_name)
            except:
                print("An error has occurred")
            #st.write('---')
            #with st.spinner(':red[Wait for converting speech to text...]'):
            Xu_li_speech2text(file_name)
            #time.sleep(0.5)
            #st.success('Done!')

        
def Dich_entxt_to_vitxt(choice):
    st.subheader(choice)
    uploaded_file = st.file_uploader('Chọn tệp txt Anh văn',type=['txt'])

    if uploaded_file is not None:
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        string_data = stringio.read()
        #st.write(string_data)

        tepin = uploaded_file.name
        tepout = tepin.replace('.txt', '_vi.txt') 
        #infile = open(tepin, 'r')                   
        infile = string_data                 
        lines = 0
        words = 0
        char = 0
        i = 0
        tep = tepin.replace('.txt','')+str(i)+'.txt'
        filei = open(tep,'w+')
        for line in infile:
            wordslist = line.split()             
            lines = lines + 1       
            words = words + len(wordslist)        
            char = char + len(line)
            filei.write(line)
            if lines == 24 :
                filei.close()
                i = i + 1
                tep = tepin.replace('.txt','')+str(i)+'.txt'
                filei = open(tep,'w+')                               
                lines = 0
                words = 0
                char = 0

        filei.close()
        #tepd = fname.replace('.txt','')+'d.txt'
        ff = open(tepout, encoding = 'utf-8', mode='w+')
        translator = Translator()
        for ntep in range(0, i+1):
            tep = tepin.replace('.txt','')+str(ntep)+'.txt'
            f = open(tep, encoding = 'utf-8', mode='r')
            #f = open(tep, encoding = 'utf-8', mode='r')
            txtt = f.read().strip()
            #print(txtt)
            kqdich = translator.translate(txtt, src='en', dest='vi')
            textd = kqdich.text
                #print(textd)      
            ff.write(textd)

        #os.startfile(tepout)
        ff = open(tepout, encoding = 'utf-8', mode='r')
        data = ff.read()
        ff.close()
        os.startfile(tepout)
        #self.textEdit_2.clear()
        #self.listWidget_2.addItem(data)

def get_large_audio_transcription(path, r):
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


                
####################################################################    
st.title("Khám Phá Video Youtube")
menu = ["1. Download youtube khi biết url của nó",
        "2. Xem video youtube từ mp4 trong máy",
        "3. Chuyển âm nói trong youtube thành text",
        "4. Dịch text từ ngôn ngữ gốc sang ngôn ngữ Anh",
        "5. Dịch file.txt tiếng Anh sang tiếng Việt"]
choice = st.sidebar.selectbox("MENU",menu,index=2)
        
if '1.' in choice:
    Download_youtube(choice=":red[1. Download youtube khi biết url của nó]")
elif '2.' in choice:
    Browse_video(choice=":red[2. Xem video youtube từ mp4 trong máy]")
elif '3.' in choice:
    Speech_invid_to_text(choice=":red[3. Chuyển âm nói trong youtube thành text]")
elif '4.' in choice:
    pass
elif '5.' in choice:
    Dich_entxt_to_vitxt(choice=":blue[5. Dịch file.txt tiếng Anh sang tiếng Việt]")
else:    
    pass
