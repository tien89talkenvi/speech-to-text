import streamlit as st
from pytube import YouTube
import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import split_on_silence
from googletrans import Translator 
from gtts import gTTS, gTTSError   
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

@st.cache(allow_output_mutation=True)
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

#3.2
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
    mp3_fp = BytesIO()
    lang_dest=codelang2
    tts = gTTS(text_translated, lang=lang_dest)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)  #phai co dong nay thi auto_phat_audio moi phat dc
    st.audio(mp3_fp, format="audio/wav",start_time=0)

##################################################################################
st.title(":orange[Speech :open_mouth: in Video to Text] 📝")   #
TEPDLOAD=''
viec1_download=st.checkbox(":green[$\Large 1. Download \; Video$]",key=1)
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

viec2_play_video = st.checkbox(":blue[$\Large 2.Play \; Video \; from \; Local$]",key=2)
if viec2_play_video:
    opption_play = st.radio(":green[Select one of:]", [":orange[Play video by click download again]",":blue[Upload from local then play]"],index=0,horizontal=True,key='R1' ) 
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

viec3_speech_to_text = st.checkbox(":orange[$\Large 3.Convert \; Speech \; to \; Text$]",key=3)

if viec3_speech_to_text:
    col1, col2=st.columns(2)
    with col1:
        language1 = st.selectbox(":blue[với ngôn ngữ nguồn là :]", 
                ("Vietnamese - Viet (vi)","English - Anh (en)","Latin - La tinh (la)","Spanish - Tây ban nha (es)","Taiwan - Đài loan (zh-TW)","Danish - Đan mạch (da)","German - Đức (de)","Dutch - Hà lan (nl)","French - Pháp (fr)","Japanese - Nhật bản (ja)","Korean - Hản quốc (ko)","Thai - Thái lan (th)","Khmer - Campuchia (km)"),index=1,key='L1' )
        codelang1 = ma_tieng(language1)
    with col2:
        language2 = st.selectbox(":blue[và ngôn ngữ đích là :]", 
                ("Vietnamese - Viet (vi)","English - Anh (en)","Latin - La tinh (la)","Spanish - Tây ban nha (es)","Taiwan - Đài loan (zh-TW)","Danish - Đan mạch (da)","German - Đức (de)","Dutch - Hà lan (nl)","French - Pháp (fr)","Japanese - Nhật bản (ja)","Korean - Hản quốc (ko)","Thai - Thái lan (th)","Khmer - Campuchia (km)"),index=0,key='L2' )
        codelang2 = ma_tieng(language2)


    opption_chon = st.radio(":green[Chọn nguồn video muốn lấy:]", [":orange[lấy tệp mp4 trong máy]",":blue[lấy tệp mp4 từ URL]"],index=1,horizontal=True,key='R1' ) 
    if opption_chon==":orange[lấy tệp mp4 trong máy]":
        uploaded_file = st.file_uploader('Chọn tệp mp4 trong máy muốn lấy',type=['mp4'],key='UF1')
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
        url_of_youtube = st.text_input(':red[Nhập URL của youtube rồi Enter. Ví dụ : https://www.youtube.com/watch?v=Z2iXr8On3LI]',key='IP1')
        if url_of_youtube != '':
            youtubeObject = YouTube(url_of_youtube)
            youtubeObject = youtubeObject.streams.get_highest_resolution()
            try:
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

