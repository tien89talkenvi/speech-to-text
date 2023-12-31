import streamlit as st
from pytube import YouTube
import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import split_on_silence
from gtts import gTTS, gTTSError   
#from deep_translator import GoogleTranslator
from googletrans import Translator
import streamlit.components.v1 as components 
from io import StringIO,BytesIO
import os
import re

#background: linear-gradient(#e66465, #9198e5);
#https://images.unsplash.com/photo-1516557070061-c3d1653fa646?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80
#.stApp {{background-image: url("https://drive.google.com/file/d/1T0omEW91sYG5lssGqhLyCcqnz43C5CtW/view?usp=sharing"); 
#background-attachment: fixed;
#background-size: cover}}

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

@st.cache_data
def get_info(url):
    yt = YouTube(url)
    streams= yt.streams.filter(progressive= True, type= 'video')
    details= {}
    details["image"]= yt.thumbnail_url
    details["streams"]= streams
    details["title"]= yt.title
    details["length"]= yt.length
    itag, resolutions, vformat, frate = ([] for i in range(4))
    for i in streams:
        res= re.search(r'(\d+)p', str(i))
        typ= re.search(r'video/(\w+)', str(i))
        fps= re.search(r'(\d+)fps', str(i))
        tag= re.search(r'(\d+)',str(i))
        itag.append(str(i)[tag.start():tag.end()])
        resolutions.append(str(i)[res.start():res.end()])
        vformat.append(str(i)[typ.start():typ.end()])
        frate.append(str(i)[fps.start():fps.end()])
    details["resolutions"]= resolutions
    details["itag"]= itag
    details["fps"]= frate
    details["format"]= vformat
    return details

## cho 3.
#3.1
@st.cache_data
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
def Dich_l1_l2(fulltxt, codelang1,codelang2):
    translator = Translator()
    txt_translated = translator.translate(fulltxt, src=codelang1,dest=codelang2).text    # Dich ra En theo tai lieu web
    #txt_translated = GoogleTranslator(source=codelang1,target=codelang2).translate_file(teplsource)        
    return txt_translated

@st.cache_data
def Dem_txtbig_vao_html(fulltxt):
    ltext = fulltxt.split('.')
    chp='<br><br>'
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
                {chp}
                <hr>
                <button id="English" onclick="speak_text_all(this.id)">Speak with English voice</button>
                <button id="Vietnamese" onclick="speak_text_all(this.id)">Speak with Vietnamese voice</button>
                <script>{js3}</script>
                <br><br>
                <button id="stop" onclick="stop()">Stop</button>
                <script>{js4}</script>
                <br><br>
                </body>
                </html>
                """,height=900,scrolling=True)
    #            

#3.2
@st.cache_data
def Xu_li_speech2text(path_filename,codelang1,codelang2,opption_browse):
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
    if opption_browse == ":blue[ngữ nguồn]":        
        #st.write(fulltxt.replace('.','.\n\n'))
        st.write(len(fulltxt))
        Dem_txtbig_vao_html(fulltxt)
        return
    if opption_browse == ":orange[ngữ đích]":
        txt_translated = Dich_l1_l2(fulltxt, codelang1,codelang2)
        st.write(txt_translated.replace('.','.\n\n'))
        mp3_fp = BytesIO()
        lang_dest=codelang2
        tts = gTTS(txt_translated, lang=lang_dest)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)  #phai co dong nay thi auto_phat_audio moi phat dc
        st.audio(mp3_fp, format="audio/wav",start_time=0)

    if opption_browse == ":blue[song ngữ]":
        txt_translated = Dich_l1_l2(fulltxt, codelang1,codelang2)        
        ltext = fulltxt.split('.')
        rtext = txt_translated.split('.')
        chp=''
        for i in range(len(ltext)):
            chi=str(i+1)
            htm=f"""
                <div class='f-grid'>
                    <div class='f-grid-col-left' id='l{chi}'  onclick='layidvaplay(this.id)'> {ltext[i]} </div>
                    <div class='f-grid-col-right' id='r{chi}' onclick='layidvaplay(this.id)'> {rtext[i]} </div>
                </div>
                """
            chp=chp+htm      
        sty='''
            body {
                margin:0;}
            .f-grid {
                display: flex;
                justify-content: space-between;
                margin-left:0.5rem;
                flex-flow: row wrap;}
            .f-grid-col-left {
                flex: 3 0;
                margin-left: 0.0rem;
                margin-right: 0.0rem;
                margin-bottom: 0.5rem;
                padding: 0.5rem;
                font-size: 14pt;}
            .f-grid-col-right {
                flex: 3 0;
                margin-left: 1.0rem;
                margin-right: 1.0rem;
                margin-bottom: 0.5rem;
                padding: 0.5rem;
                color:green;
                font-size: 14pt;}
            '''
        js1='''
            function layidvaplay(idname){
                const text = document.getElementById(idname).innerHTML ;
                const textEl = document.getElementById(idname);
                textEl.innerHTML = text;
                play(idname);

                function play(tenidl) {
                  if (window.speechSynthesis.speaking) {
                      // there's an unfinished utterance
                      window.speechSynthesis.resume();
                  } else {
                    // start new utterance
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.addEventListener('end', handleEnd);
                    utterance.addEventListener('boundary', handleBoundary);
                    if (tenidl.charAt(0) == 'l'){giongnoi='en-US';} else {giongnoi='vi-VN';}
                    utterance.lang = giongnoi;
                    window.speechSynthesis.speak(utterance);
                  }
                }

                function handleEnd() {
                  // reset text to remove mark
                  textEl.innerHTML = text;
                }
                
                function handleBoundary(event) {
                  if (event.name === 'sentence') {
                    // we only care about word boundaries
                    return;
                  }
                
                  const wordStart = event.charIndex;
                
                  let wordLength = event.charLength;
                  if (wordLength === undefined) {
                    // Safari doesn't provide charLength, so fall back to a regex to find the current word and its length (probably misses some edge cases, but good enough for this demo)
                    const match = text.substring(wordStart).match(/^[a-z\d']*/i);
                    wordLength = match[0].length;
                  }
                  
                  // wrap word in <mark> tag
                  const wordEnd = wordStart + wordLength;
                  const word = text.substring(wordStart, wordEnd);
                  const markedText = text.substring(0, wordStart) + '<mark>' + word + '</mark>' + text.substring(wordEnd);
                  textEl.innerHTML = markedText;
                }
            }
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
                        <br>
                        {chp}
                        <br>
                        <script>
                        {js1}
                        </script>
                        </body>
                        </html>
                        """,height=1200,scrolling=True)
        #            
        #components.html(html_str, unsafe_allow_html=True)
        #st.markdown(html_str, unsafe_allow_html=True)
        #agree = st.checkbox('Đọc text dịch ra đã Ctr-C')
        #if agree:
        #    text_translated = pyperclip.paste()


##################################################################################
st.title(":orange[Speech :open_mouth: in Video to Text] 📝")   #
url=''
TEPDLOAD=''
tieude=''
viec1_download=st.checkbox(":green[$\Large 1. Download \; Video$]",key="M1")
if viec1_download:
    url = st.text_input(":red[Paste URL here 👇 then Enter. Ex. https://www.youtube.com/watch?v=Z2iXr8On3LI]", placeholder='https://www.youtube.com/')
    if url:
        v_info= get_info(url)
        col1, col2= st.columns([1,1.5], gap="small")
        with st.container():
            with col1:
                st.image(v_info["image"])
            with col2:
                st.subheader(":orange[Video Details] ⚙️")
                res_inp = st.selectbox('__Select Resolution__', v_info["resolutions"],index=2)
                id = v_info["resolutions"].index(res_inp)            
                st.write(f"__Title:__ {v_info['title']}")
                st.write(f"__Length:__ {v_info['length']} sec")
                st.write(f"__Resolution:__ {v_info['resolutions'][id]}")
                st.write(f"__Frame Rate:__ {v_info['fps'][id]}")
                st.write(f"__Format:__ {v_info['format'][id]}")
                file_name = st.text_input('__Save as 🎯__', placeholder = v_info['title'])
                tieude = v_info['title']
                if file_name:        
                    if file_name != v_info['title']:
                        file_name+=".mp4"
                else:
                    file_name = v_info['title'] + ".mp4" 
                    
            button = st.button("Download ⚡️")
            if button:
                with st.spinner('Downloading...'):
                    try:
                        ds = v_info["streams"].get_by_itag(v_info['itag'][id])
                        ds.download(filename= file_name, output_path= "downloads/")
                        st.success('Download Complete', icon="✅")
                        TEPDLOAD="downloads/" + file_name       
                        st.balloons()
                    except:
                        st.error('Error: Save with a different name!', icon="🚨")      

st.write('---')

viec2_play_video = st.checkbox(":blue[$\Large 2.Play \; Video$]",key="M2")
if viec2_play_video:
    opption_play = st.radio(":green[Select one of:]", [":orange[Play video by click download again]",":blue[Upload from local then play]"],index=0,horizontal=True,key='R11' ) 
    if opption_play==":orange[Play video by click download again]":
        if TEPDLOAD !='':
            video_file = open(TEPDLOAD, 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)

    if opption_play==":blue[Upload from local then play]":
        uploaded_file = st.file_uploader('Select Video file (.mp4) from Local',type=['mp4'],key='VD2')
        if uploaded_file is not None:
            st.video(uploaded_file)

st.write('---')

codelang1='en'
codelang2='vi'

viec3_speech_to_text = st.checkbox(":orange[$\Large 3.Convert \; Speech \; to \; Text$]",key='M3')

if viec3_speech_to_text:
    opption_browse = st.radio(":green[Chọn hiển thị:]", [":blue[ngữ nguồn]",":orange[ngữ đích]",":blue[song ngữ]"],index=0,horizontal=True,key='R00' ) 

    col1, col2=st.columns(2)
    with col1:
        language1 = st.selectbox(":blue[với ngôn ngữ nguồn là :]", 
                ("Vietnamese - Viet (vi)","English - Anh (en)","Latin - La tinh (la)","Spanish - Tây ban nha (es)","Taiwan - Đài loan (zh-TW)","Danish - Đan mạch (da)","German - Đức (de)","Dutch - Hà lan (nl)","French - Pháp (fr)","Japanese - Nhật bản (ja)","Korean - Hản quốc (ko)","Thai - Thái lan (th)","Khmer - Campuchia (km)"),index=1,key='L1' )
        codelang1 = ma_tieng(language1)
    with col2:
        language2 = st.selectbox(":blue[và ngôn ngữ đích là :]", 
                ("Vietnamese - Viet (vi)","English - Anh (en)","Latin - La tinh (la)","Spanish - Tây ban nha (es)","Taiwan - Đài loan (zh-TW)","Danish - Đan mạch (da)","German - Đức (de)","Dutch - Hà lan (nl)","French - Pháp (fr)","Japanese - Nhật bản (ja)","Korean - Hản quốc (ko)","Thai - Thái lan (th)","Khmer - Campuchia (km)"),index=0,key='L2' )
        codelang2 = ma_tieng(language2)


    opption_chon = st.radio(":green[Chọn nguồn video muốn lấy:]", [":blue[tệp downloaded tại mục 1]",":orange[tệp mp4 trong máy]",":blue[tệp mp4 từ URL]"],index=2,horizontal=True,key='R01' ) 
    st.write('---')

    if opption_chon==":blue[tệp downloaded tại mục 1]":
        if url !='':
            youtubeObject = YouTube(url)
            youtubeObject = youtubeObject.streams.get_highest_resolution()
            try:
                youtubeObject.download()
                file_name = youtubeObject.default_filename
                #st.write(':blue[Download is completed successfully with file named : ] '+file_name)
            except:
                print("An error has occurred")

            Xu_li_speech2text(file_name,codelang1,codelang2,opption_browse)
            st.success('Converting Complete', icon="✅")
            st.balloons()


    elif opption_chon==":orange[tệp mp4 trong máy]":
        uploaded_file = st.file_uploader('Chọn tệp mp4 trong máy muốn lấy',type=['mp4'],key='UF1')
        if uploaded_file is not None:
            filename = uploaded_file.name
            with open(os.path.join("",filename),"wb") as f: 
                f.write(uploaded_file.getbuffer())         
            Xu_li_speech2text(filename,codelang1,codelang2,opption_browse)
            st.success('Converting Complete', icon="✅")
            st.balloons()

    else:
        url_of_youtube = st.text_input(':red[Nhập URL của youtube rồi Enter. Ví dụ : https://www.youtube.com/watch?v=Z2iXr8On3LI]',key='IP1')
        if url_of_youtube != '':
            youtubeObject = YouTube(url_of_youtube)
            youtubeObject = youtubeObject.streams.get_highest_resolution()
            try:
                youtubeObject.download()
                file_name = youtubeObject.default_filename
                #st.write(':blue[Download is completed successfully with file named : ] '+file_name)
            except:
                print("An error has occurred")
            Xu_li_speech2text(file_name,codelang1,codelang2,opption_browse)
            st.success('Converting Complete', icon="✅")
            st.balloons()
