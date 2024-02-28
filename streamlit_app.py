# pip install youtube-transcript-api
import streamlit as st
import streamlit.components.v1 as components 
import time
from youtube_transcript_api import YouTubeTranscriptApi
import re
from urllib import parse
import json


#------------------------------------
@st.cache_data
def is_from_youtube(url:str) -> bool:
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return re.match(youtube_regex, url)

#--------------------------------------
@st.cache_data
def get_youtube_id(url:str) -> str:
    query = parse.urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return ""

#------------------------------------------
@st.cache_data
def Lay_ttin_cua_url(url_vid_input):
    id_ofvid = get_youtube_id(url_vid_input)
    transcript_list = YouTubeTranscriptApi.list_transcripts(id_ofvid)
    for transcript in transcript_list:
        return transcript.translate('vi').fetch()
#--------------------------------------------------------
@st.cache_data
def Dem_txtbig_vao_html(fulltxt):
    ltext = fulltxt.split('.')
    chp='<br><br>'
    chp=chp+'<div class="f-grid">'+fulltxt+'</div>'   
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
                <iframe width="100%" height="460" src="{url_vid_input}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                <hr>
                <button id="English" onclick="speak_text_all(this.id)">Speak with English</button>
                <button id="Vietnamese" onclick="speak_text_all(this.id)">Speak with Vietnamese</button>
                <button id="stop" onclick="stop()">Stop</button>
                <script>{js3}</script>
                <script>{js4}</script>
            
                {chp}
                <hr>
                <br>
                </body>
                </html>
                """,height=600,scrolling=True)

#==============================================================================
st.title('Nghe Văn bản của Video Youtube')
#video_input = st.text_input(':green[Nhập URL của youtube rồi Enter. Ví dụ : https://www.youtube.com/watch?v=KG0Q05Lnm7s]',key='IP1')
url_vid_input = st.text_input(':green[Nhập URL của youtube rồi Submit]', value = 'https://www.youtube.com/embed/lcZDWo6hiuI',key='IP1')
if st.checkbox('Submit'):
    # neu video_input (url) hop le va cai nay cua youtube 
    if url_vid_input and is_from_youtube:
        vanban_phienam = Lay_ttin_cua_url(url_vid_input)

        #thu
        filename = 'zzzthu'
        _id = get_youtube_id(url_vid_input)
        transcript = YouTubeTranscriptApi.get_transcript(_id)
        with open(f'{filename}.json', 'w', encoding='utf-8') as json_file:
            json.dump(transcript, json_file)
        #    
         
        text_all = ''
        for element in vanban_phienam:
            text_element = element['text']
            text_all = text_all + text_element + ' '

        Dem_txtbig_vao_html(text_all)
        st.success('Converting Complete', icon="✅")
        st.balloons()
    else:
        st.write(':orange[Chưa nhập url hoặc url này không phải của Youtube!]')

