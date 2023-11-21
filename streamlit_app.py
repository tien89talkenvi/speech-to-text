# -*- coding: utf-8 -*-
# 1- https://tien89.streamlit.app/     # up ngay 15-11-2023
#    https://github.com/tien89talkenvi/speech-to-text

# -*- coding: utf-8 -*-
# https://tien89.streamlit.app/     # up ngay 15-11-2023

import streamlit as st
from pytube import YouTube
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from googletrans import Translator 
from gtts import gTTS, gTTSError   
from googletrans import Translator 
import streamlit.components.v1 as components 
from io import StringIO,BytesIO
import os

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

def Xu_li_speech2text(path_filename,codelang1,codelang2):
    tepvideo=os.path.basename(path_filename)
    clip = mp.VideoFileClip(tepvideo)
    tepwav = tepvideo.replace('.mp4', '.wav') 
    clip.audio.write_audiofile(tepwav)
    tepout = tepwav.replace('.wav', '.txt') 
    fulltxt=''
    with sr.AudioFile(tepwav) as source:
        r = sr.Recognizer()
        fulltxt = get_large_audio_transcription(tepwav, r)
    
    translator = Translator()
    text_translated = translator.translate(fulltxt, src=codelang1,dest=codelang2).text    # Dich ra En theo tai lieu web
    st.write(text_translated)
        
        #ltext = fulltxt.split('.')
        #chp='<br><br>'
        #for text in ltext:
        #    chp=chp+'<div class="f-grid">'+text+'</div>'   
        #with open(tepout, encoding = 'utf-8', mode='w+') as fh:    
            #fh.write(fulltxt)
            #os.startfile(tepout)
            #st.write(fulltxt)
        #js1='''
        #    function googleTranslateElementInit(){new google.translate.TranslateElement({pageLanguage:'en'}, 'google_translate_element');}
        #    '''
        #js2='''
        #    src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"
        #    '''
        #sty='''
        #    .f-grid {
        #        display: flex;
        #        justify-content: space-between;
        #        margin-left:-0.5rem;
        #        flex-flow: row wrap;
        #        font-size: 20px; }
        #    '''
        #js3='''
        #    const downloadFile = () => {
        #        const link = document.createElement("a");
        #        const content = '';
        #        const file = new Blob([content], { type: 'text/plain' });
        #        link.href = URL.createObjectURL(file);
        #        link.download = "translated-text.txt";
        #        link.click();
        #        URL.revokeObjectURL(link.href);
        #    };
        #    '''
        #components.html(f"""
        #            <!DOCTYPE html>
        #            <html lang="en">
        #            <head>
        #            <meta charset="UTF-8">
        #            <meta http-equiv="X-UA-Compatible" content="IE=edge">
        #            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        #            <title>Tiensg89's App</title>
        #            <style> {sty} </style>
        #            </head>
        #            <body>
        #            <div id="google_translate_element" ></div>
        #            <script>{js1}</script>
        #            <script {js2}></script>
        #            {chp}
        #            <br><br>
        #            <button onclick = "downloadFile()"> Save to file by clicking here, it will browse nopad then you select translated text then copy and paste into nopad. </button>
        #            <script>{js3}</script>
        #            </body>
        #            </html>
        #            """,height=800,scrolling=True)
        #            
        #components.html(html_str, unsafe_allow_html=True)
        #st.markdown(html_str, unsafe_allow_html=True)
        #agree = st.checkbox('Đọc text dịch ra đã Ctr-C')
        #if agree:
        #    text_translated = pyperclip.paste()
    mp3_fp = BytesIO()
    lang_dest=codelang2
    tts = gTTS(text_translated, lang=lang_dest)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)  #phai co dong nay thi auto_phat_audio moi phat dc
    st.audio(mp3_fp, format="audio/wav",start_time=0)

def ma_tieng(tieng):
    global codelang1,codelang2
    sub1='('
    sub2=')'
    idx1 = tieng.index(sub1)
    idx2 = tieng.index(sub2)
    res = ''
    # getting elements in between
    for idx in range(idx1 + len(sub1), idx2):
        res = res + tieng[idx]
    codelang=res
    return codelang

# 3 -----------------------------
def Speech_invid_to_text(choice,codelang1,codelang2):
    st.subheader(choice)
    col1, col2=st.columns(2)
    with col1:
        language1 = st.selectbox(":blue[với ngôn ngữ nguồn là :]", 
                ("Vietnamese - Viet (vi)","English - Anh (en)","Spanish - Tây ban nha (es)","Taiwan - Đài loan (zh-TW)","Danish - Đan mạch (da)","German - Đức (de)","Dutch - Hà lan (nl)","French - Pháp (fr)","Japanese - Nhật bản (ja)","Korean - Hản quốc (ko)","Thai - Thái lan (th)","Khmer - Campuchia (km)"),index=1,key=1 )
        codelang1 = ma_tieng(language1)
    with col2:
        language2 = st.selectbox(":blue[và ngôn ngữ đích là :]", 
                ("Vietnamese - Viet (vi)","English - Anh (en)","Spanish - Tây ban nha (es)","Taiwan - Đài loan (zh-TW)","Danish - Đan mạch (da)","German - Đức (de)","Dutch - Hà lan (nl)","French - Pháp (fr)","Japanese - Nhật bản (ja)","Korean - Hản quốc (ko)","Thai - Thái lan (th)","Khmer - Campuchia (km)"),index=0,key=2 )
        codelang2 = ma_tieng(language2)

    opption_chon = st.radio(":green[Chọn nguồn video muốn lấy:]", [":red[lấy tệp mp4 trong máy]",":blue[lấy tệp mp4 từ URL]"],index=1,horizontal=True ) 
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
            Xu_li_speech2text(filename,codelang1,codelang2)
            #time.sleep(0.5)
            #st.success('Done!')

    else:
        url_of_youtube = st.text_input('Nhập URL của youtube rồi Enter. Ví dụ : https://www.youtube.com/watch?v=Z2iXr8On3LI')
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
            Xu_li_speech2text(file_name,codelang1,codelang2)
            #time.sleep(0.5)
            #st.success('Done!')

def Translated_text_to_speech(choice,codelang1,codelang2):
    st.subheader(choice)
    text_translated = pyperclip.paste()
    mp3_fp = BytesIO()
    lang_dest=codelang2
    tts = gTTS(text_translated, lang=lang_dest)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)  #phai co dong nay thi auto_phat_audio moi phat dc
    st.audio(mp3_fp, format="audio/wav",start_time=0)

def Dich_lang1txt_to_lang2txt(choice,codelang1,codelang2):
    st.subheader(choice)
    uploaded_file = st.file_uploader('Chọn tệp txt '+codelang1,type=['txt'])

    if uploaded_file is not None:
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        string_data = stringio.read()
        #st.write(string_data)

        tepin = uploaded_file.name
        tepout = tepin.replace('.txt', '_'+codelang2+'.txt') 
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
            kqdich = translator.translate(txtt, src=codelang1, dest=codelang2)
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



                
####################################################################    
st.title("Khám Phá Video Youtube")
menu = ["1. Download youtube khi biết url của nó",
        "2. Xem video youtube từ mp4 trong máy",
        "3. Chuyển âm nói trong youtube thành text",
        "4. Đọc nghe text đã dịch ra tiếng Việt"]
choice = st.sidebar.selectbox("MENU",menu,index=2)
codelang1='en'
codelang2='vi'

if '1.' in choice:
    Download_youtube(choice=":red[1. Download youtube khi biết url của nó]")
elif '2.' in choice:
    Browse_video(choice=":red[2. Xem video youtube từ mp4 trong máy]")
elif '3.' in choice:
    Speech_invid_to_text(choice=":red[3. Chuyển âm nói trong youtube thành text]",codelang1='en',codelang2='en')
elif '4.' in choice:
    Translated_text_to_speech(choice="4. Đọc nghe text đã dịch ra tiếng "+codelang2,codelang1='en',codelang2='vi')

