# pip install youtube-transcript-api
import streamlit as st
import streamlit.components.v1 as components 
import time
from youtube_transcript_api import YouTubeTranscriptApi
#from utils import is_from_youtube, get_youtube_id
import re
from urllib import parse
import json
from pytube import extract


#------------------------------------------
def Lay_ttin_cua_url(url_vid_input):
    id_ofvid = extract.video_id(url_vid_input)
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(id_ofvid)
        if transcript_list:
            transcript = YouTubeTranscriptApi.get_transcript(id_ofvid)
            return transcript
    except:    
        return ''
    #transcript_list = YouTubeTranscriptApi.list_transcripts(id_ofvid)
    #for transcript in transcript_list:
        #st.write(
            # id cua video
        #    transcript.video_id,
            # ngon ngu cua text
        #    transcript.language,
            # ma code ngon ngu goc
        #    transcript.language_code,
            # duoc tao binh thuong hay sinh ra tu Yt
        #    transcript.is_generated,
            # da duoc dich ra en tu goc hay la khong
        #    transcript.is_translatable,
            # day la ban dich ra ngon ngu nao 
        #    transcript.translation_languages,
        #)

        # fetch the actual transcript data
        #print(transcript.fetch())

        # translating the transcript will return another
        # transcript object
        #return transcript.translate('vi').fetch()
        #print(transcript.translate('vi').fetch())

    # you can also directly filter for the language you are
    # looking for, using the transcript list
    #transcript = transcript_list.find_transcript(['en'])
    #return transcript 
    # or just filter for manually created transcripts
    #transcript = transcript_list.find_manually_created_transcript(['en'])
#--------------------------------------------------------
@st.cache_data
def Dem_txtbig_vao_html(fulltxt):
    ltext = fulltxt.split('.')
    chp='<br><br>'
    chp=chp+'<div class="f-grid">'+fulltxt+'</div>'   
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
                <title>Read Video</title>
                <style> {sty} </style>
                </head>
                <body>
                <iframe width="100%" height="460" src="{url_vid_input}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                <hr>
                <div id="google_translate_element" ></div>
                <script>{js1}</script>
                <script {js2}></script>
 
                <button id="English" onclick="speak_text_all(this.id)" translate="no">Speak with English</button>
                <button id="Vietnamese" onclick="speak_text_all(this.id)" translate="no">Speak with Vietnamese</button>
                <button id="stop" onclick="stop()" translate="no">Stop</button>
                <script>{js3}</script>
                <script>{js4}</script>
            
                {chp}
                <hr>
                <br>
                </body>
                </html>
                """,height=640,scrolling=True)

#==============================================================================
st.title('Nghe Văn bản của Video Youtube')
url_vid_input = st.text_input(':green[Nhập URL của youtube rồi Enter. Ví dụ : https://www.youtube.com/embed/lcZDWo6hiuI]',key='IP1')
#url_vid_input = st.text_input(':green[Nhập URL của youtube rồi Submit]', value = 'https://www.youtube.com/watch?v=KG0Q05Lnm7s',key='IP1')
if st.checkbox('Submit'):
    # neu video_input (url) hop le va cai nay cua youtube 
    if url_vid_input :
        
        vanban_phienam = Lay_ttin_cua_url(url_vid_input)
        if vanban_phienam != '':
            text_all = ''
            for element in vanban_phienam:
                text_element = element['text']
                text_all = text_all + text_element + ' '

            Dem_txtbig_vao_html(text_all)
            st.success('Converting Complete', icon="✅")
            st.balloons()
        else:
            st.write(':orange[Không có bản phiên âm nào!]')        
    else:
        st.write(':orange[Chưa nhập url hoặc url này không hợp lệ!]')

