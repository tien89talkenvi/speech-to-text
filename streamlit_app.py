# pip install streamlit
# pip install youtube-transcript-api
# pip install pytube
# pip install googletrans==4.0.0rc1
# pip install  yt-dlp
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
import streamlit.components.v1 as components 
from pytube import YouTube, extract
import time
from streamlit_input_box import input_box



st.set_page_config(page_title="Speak Youtube Subtitles", layout="wide")
st.markdown(" <style> div[class^='block-container'] { padding-top: 0rem; } </style> ", unsafe_allow_html=True)

#----Set background----------------------------------------------------------------------------------------
#st.set_page_config(page_title="Video với dịch & đọc phụ đề En-Vi", page_icon="🚀", layout="centered",)     
#st.markdown(f"""
#            <style>
#            .stApp {{background-image: linear-gradient(0deg,lightgrey,lightgrey);
#            background-attachment: fixed;
#            background-size: cover}}
#        </style>
#         """, unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------
#------------------------------------------
def Lay_ttin_cua_url(url_vid_input):
    #<iframe width="100%" height="460" src="{url_vid_input}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    id_ofvid = extract.video_id(url_vid_input)
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(id_ofvid)
        if transcript_list:
            transcript = YouTubeTranscriptApi.get_transcript(id_ofvid)
            return transcript
    except:    
        return ''
#-------------------------------------------------------------
@st.cache_data
def Lap_html_video(transcript_en, videoID):
    chp = ''
    for pt_dict in transcript_en:
        start = pt_dict['start']
        durat = pt_dict['duration']
        text = pt_dict['text']
        chp1 = '<div class="f-grid">\n'
        chp2 = '<div class="youtube-marker-l" data-start='+'"'+str(start)+'"' + ' data-end='+'"'+str(round(start+durat,3))+'"'+'>'+text+'</div>\n'
        chp3 = '<div class="youtube-marker-r" data-start='+'"'+str(start)+'"' + ' data-end='+'"'+str(round(start+durat,3))+'"'+'></div>\n'
        chp4 = '</div>\n' 
        chp = chp + chp1 + chp2 + chp3 +chp4
    # in chp de copy dan vao html     
    print(chp)    
  
    sty='''
        body{
            background:lightgray;
            /*background-color: darkgray;*/}
        .video-wrapper {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;}
        .video-wrapper iframe {
            position: absolute;
            top:0;
            left: 0;
            width: 100%;
            height: 100%;}
        .f-grid {
            display: flex;
            justify-content: space-between;
            margin-left:0rem;
            flex-flow: row wrap;
            margin-bottom: -1.5rem;}
        .youtube-marker-l{
            flex: 3 0;
            margin-left: 0.5rem;
            margin-bottom: 0rem;
            font-size: 0pt;
            padding: 1rem;}
        .youtube-marker-r{
            flex: 3 0;
            margin-left: 0.5rem;
            margin-bottom: 0rem;
            font-size: 0pt;
            padding: 1rem;
            color:darkblue;}
        .youtube-marker-r:hover {
            cursor: pointer;}
        .youtube-marker-r-current {
            color: brown;}
        .center {
            font-size: 13pt;
            display: flex;
            justify-content: center;
            align-items: center;}
        h2 { 
            font-size: 20pt;
            text-align: center;
            color:green;}
        #elm_url_yt{
            font-size: 0pt;}
        .rateread {
            font-size: 13pt;
            display: flex;
            justify-content: center;
            align-items: center;}
        #trudi{
            height: 30px;
            width: 30px;
            border-radius: 50%;
            border: none;} 
        #congthem {
            height: 30px;
            width: 30px;
            border-radius: 50%;
            border: none;}
        #vnoi {
            height: 40px;
            width: 40px;
            border: 4;}
        '''

    js1='''
        //bien global
        var strBuffer = {};
        var btn_elm = document.getElementById('btn');
        var k=0;
        var lang_dich_ra;
        var voice_speak_dich;
        var rate =  Number(document.getElementById('vnoi').innerHTML).toFixed(1);   

        //tao menu select_target_dialect lang dich ra tu dong dich 
        let l_target_language = ['Danish', 'English', 'French', 'German', 'Italian', 'Japanese', 'Korean', 'Mexico', 'Nederlands', 'Rusian', 'Taiwan', 'Thai', 'Vietnamese']; 
        let l_target_voices = ['da-DK', 'en-US', 'fr-FR', 'de-DE', 'it-IT', 'ja-JP', 'ko-KR', 'es-MX', 'nl-NL', 'ru-RU', 'zh-TW', 'th-TH', 'vi-VN']; 
        let l_target_voices_tg = []; 

        //---------------------------------
        function populateVoiceList() {
            if (typeof speechSynthesis === "undefined") {
                return;
            }
            const voices = speechSynthesis.getVoices();
            for (let i = 0; i < voices.length; i++) {
                //neu voices[i].lang co trong l_target_voices va voices[i].lang chua co trong l_target_voices_tg thi lay 
                //l_target_language[l_target_voices.indexOf(voices[i].lang] dua vao  select_target_language
                if ( l_target_voices.indexOf(voices[i].lang) >= 0 ){
                    select_target_language.options.add(new Option(l_target_language[l_target_voices.indexOf(voices[i].lang)]+' ('+voices[i].lang+') - '+voices[i].name));
                    //cai nay de kiem tra voices[i].lang dem vao chi 1 lan
                    l_target_voices_tg.push(voices[i].lang);
                    
                    //chon default
                    //if (voices[i].lang.includes('vi-VN') && (voices[i].name.includes('Linh') || voices[i].name.includes('An')) ){
                    if (voices[i].lang.includes('vi-VN') ){
                        //hai bien global lay gia tri ghi vao memory
                        lang_dich_ra = voices[i].lang.slice(0, 2) ;
                        voice_speak_dich = voices[i].lang;
             
                        //chi dinh default trong menu se hien ra
                        let indexChon = l_target_voices_tg.indexOf(voices[i].lang);
                        select_target_language.selectedIndex = indexChon;
                        t_translate(lang_source='en', lang_dich_ra=lang_dich_ra);
                        //return;
                    }
                }
            }
        }
        //---------------------
        populateVoiceList();
        if (typeof speechSynthesis !== "undefined" && speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = populateVoiceList;
        }
        //-----------------------------------------------
        function active_target_lang() {
            //let selectedValue = select_target_language.options[select_target_language.selectedIndex].text;
            let index_chon = select_target_language.selectedIndex;
            //let text_brow = select_target_language.value;
            let lang_rut = l_target_voices_tg[index_chon];
            //alert(lang_rut);
            if (typeof speechSynthesis === "undefined") {
                return;
            }
            const voices = speechSynthesis.getVoices();
            for (let i = 0; i < voices.length; i++) {
                if (voices[i].lang.includes(lang_rut)){
                    lang_dich_ra = lang_rut.slice(0, 2);
                    voice_speak_dich =  voices[i].lang;
                    t_translate(lang_source='en', lang_dich_ra=lang_dich_ra);
                    return;
                }  
            }
        }
        //---Dich ra ----------------------------------------- 
        function t_translate(lang_source, lang_dich_ra) { 
            const sourceLanguage = lang_source;
            const targetLanguage = lang_dich_ra;
            var els = document.getElementsByClassName("youtube-marker-l"); // Creates an HTMLObjectList not an array.
            var elsd = document.getElementsByClassName("youtube-marker-r")

            Array.prototype.forEach.call(els, function(el,i) {
                let inputText = el.innerText;
                let outputTextEle = elsd[i];

                const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${sourceLanguage}&tl=${targetLanguage}&dt=t&q=${encodeURI(inputText)}`;

                const xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200){
                        const responseReturned = JSON.parse(this.responseText);
                        const translations = responseReturned[0].map((text) => text[0]);
                        const outputText = translations.join(" ");
                        outputTextEle.textContent = outputText;
                    }
                };
                //---------------------
                xhttp.open("GET", url);
                xhttp.send();
            });
        }
        //======== Cua youtube API ====================================
        let videoIDcurrent = document.getElementById("elm_url_yt").innerText;
        //---------------------------------
        let player;
        let timeStart = 0;
        let timeStartl = -1;

        //-----------------------------------
        function onYouTubeIframeAPIReady() {

            //3a-Instantiate the Player, phai co player=... de iframeWindow hoat dong
            player = new YT.Player("player", {
                //da co iframe quy dinh roi
                height: "300",
                width: "480",
                videoId: videoIDcurrent
            });
            //3b- This is the source "window" that will emit the events.
            var iframeWindow = player.getIframe().contentWindow;

            //3c- So we can compare against new updates.
            var lastTimeUpdate = 0;
            //3d- Listen to events triggered by postMessage ,this is how different windows in a browser (such as a popup or iFrame) can communicate. // See: https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage
            window.addEventListener("message", function(event) {
                // Check that the event was sent from the YouTube IFrame.
                if (event.source === iframeWindow) {
                    var data = JSON.parse(event.data);
                    // The "infoDelivery" event is used by YT to transmit any kind of information change in the player, such as the current time or a playback quality change.
                    //===SPEAK SUB HERE=======================================================
                    if (data.event === "infoDelivery" && data.info && data.info.currentTime) {
                        //console.log(data.info.currentTime);
                        //time co dang 212.544 giay
                        //var time = Math.round(data.info.currentTime * 1000) / 1000;
                        var time = Math.round(data.info.currentTime);//lam tron sec

                        const [strBuffer, strBuffer2] = lay_strBuffer();
                        //dang cua strBuffer la {1.224:'Toi', 2.16:'Anh', 3.111: 'No'}

                        timeStart = time;
                        let text = strBuffer[timeStart];
                        let ellay = strBuffer2[timeStart];

                        //Neu timeStart khac voi timeStartl luu va text khac trong  
                        if (timeStart !== timeStartl && text){
                            console.log(timeStart, ellay);
                            timeStartl = time; 
                            subtitle.innerText = text;
                            ellay.classList.add("youtube-marker-r-current");
                            //phat am----------------------------------------
                            Read_Sub(text);
                        }//--------------------------------------------------

                        //Cu sau moi sec thi hien thi thoi gian
                        // currentTime is emitted very frequently (milliseconds), but we only care about whole second changes.
                        //var time = Math.floor(data.info.currentTime);
                        //var time = data.info.currentTime;
                        if (time !== lastTimeUpdate) {
                            lastTimeUpdate = time;
                            // It's now up to you to format the time. tinh ra phan tram thoi gian da chay youtub
                            document.getElementById("time").innerHTML = '(' + Math.round(100*time/player.getDuration()) +' %) &nbsp;';
                        }  
                    }
                }
            });
        }
                            //marker.dom.classList.add("youtube-marker-r-current");

        //---------Lay strBuffer phu de moi sec--------------------------
        function lay_strBuffer(){
            let strBuffer = {},
                strBuffer2 = {};
            var elsd = document.getElementsByClassName("youtube-marker-r");
            Array.prototype.forEach.call(elsd, function(el,i) {
                let start = Math.round(el.attributes[1].value);
                let text = el.innerHTML;
                strBuffer[start] = text;
                strBuffer2[start] = el;

            });
            return [strBuffer, strBuffer2];
        }
        //------------------------------------------------------
        function cong1(){
            rate =  Number(document.getElementById('vnoi').innerHTML).toFixed(1);
            if (rate >= 0.0 && rate < 3.0) {
                document.getElementById('vnoi').innerHTML = (Number(document.getElementById('vnoi').innerHTML) + Number("0.1")).toFixed(1);
            }
        }
        //----------------    
        function tru1(){
            rate =  Number(document.getElementById('vnoi').innerHTML).toFixed(1);
            if (rate <= 3 && rate > 0) {
                document.getElementById('vnoi').innerHTML = (Number(document.getElementById('vnoi').innerHTML) - Number("0.1")).toFixed(1);
            }
        }
        //------Moi lan click thi hien thi hoac an di subtitles-------
        btn_elm.onclick = function(){
            k=k+1;
            //alert(k);
            if (k % 2 === 1){
                var el = document.querySelectorAll(".youtube-marker-l");
                for ( var i = 0; i < el.length; i ++ ) {
                    el[i].style.fontSize = "14pt";
                }
                var el = document.querySelectorAll(".youtube-marker-r");
                for ( var i = 0; i < el.length; i ++ ) {
                    el[i].style.fontSize = "14pt";
                }
            } else {   
                var el = document.querySelectorAll(".youtube-marker-l");
                for ( var i = 0; i < el.length; i ++ ) {
                    el[i].style.fontSize = "0pt";
                }
                var el = document.querySelectorAll(".youtube-marker-r");
                for ( var i = 0; i < el.length; i ++ ) {
                    el[i].style.fontSize = "0pt";
                }
            }
        }
        //--------------------------
        function Read_Sub(text){
            rate = Number(document.getElementById('vnoi').innerHTML).toFixed(1);
            var msg     = new SpeechSynthesisUtterance();
            msg.volume = 1;
            msg.rate = rate; // 0 to 1, does not seem to work
            msg.lang = voice_speak_dich;
            msg.text = text;
            speechSynthesis.speak(msg);
        
        }
        //--------------------------------------------------------------
        '''
    components.html(f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Video Translate Speak Subtitle</title>

                    <style>{sty}</style>
                    </head>
                    <body>
                    <div class="video-wrapper">
                        <div id="player"></div>
                    </div>
                    <p id="elm_url_yt">{videoID}</p>

                    <hr>
                    <div class="center">
                        Voice &nbsp; <select id="select_target_language" onchange ="active_target_lang()"></select>&emsp;<span id="time"></span>
                    </div><br>

                    <div class="rateread">
                        <button id="read_sub" onclick="Read_Sub()">Speak</button>&emsp; &emsp; 
                        <button id="trudi" onclick="tru1()">-</button>&emsp; &emsp; 
                        <button id="vnoi">1.2</button>&emsp; &emsp; 
                        <button id="congthem" onclick="cong1()">+</button>&emsp;&emsp;
                        <button id="btn">Sub</button>
                    </div>

                    <hr>
                    <h2 id="subtitle"></h2>


                    {chp}

                    <script>{js1}</script>

                    <!-- Phai co dong sau thi moi speak duoc-->
                    <script src="https://www.youtube.com/iframe_api"></script>

                </body>
                </html>
                """,height=900,scrolling=True)


#==============================================================================
#https://youtu.be/3c-iBn73dDE?si=loeUZPwUmmh0iGW4   2h 40phut
#https://youtu.be/DpxxTryJ2fY?si=oMvtK4Nqt-y6Een9   BIGATE          ok en vi
#https://youtu.be/zBHxv8gbleg?si=zeo5OQ_cx5XsQgeG   TRUMP           ok en vi
#https://www.youtube.com/embed/lcZDWo6hiuI          Gs University   ok en vi
#https://www.youtube.com/watch?v=Z2iXr8On3LI        voa anh van     no en no vi (not is yt)
#https://youtu.be/Zgfi7wnGZlE?si=TzeWpiERRxzdJKVA   obama           ok en vi (#1h)

#---Bat Dau Main ------------------------------------------------------------------------------------------------
#st.title('Speak Youtube Subtitles')
st.markdown("<h1 style='text-align: center; color: green;'>Speak Youtube Subtitles</h1>", unsafe_allow_html=True)
link_vidu = "https://www.youtube.com/embed/5MgBikgcWnY?enablejsapi=1"
st.markdown("<h6 style='text-align: center; color: lightgrey;'>"+link_vidu+"</h6>", unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------------

state=st.session_state
if 'texts' not in state:
    state.texts = ""
    
url_vid_input = input_box(min_lines=1,max_lines=3,just_once=True)
#st.text(url_vid_input)

#url_vid_input = st.text_input("<h2 style='text-align: center; font-size: 2pt;'>'+link_vidu+'</h2>",link_vidu, label_visibility="hidden", key='IP1')

if url_vid_input :
    #st.text(text)
    try:
        t1=time.time()
        # B0: Chuyen doi cac URL noi chung sang URL YOUTUBE "https://www.youtube.com/embed/" + VIDEO-ID
        videoID = extract.video_id(url_vid_input)
        
        # url_vid_input dat lai
        url_vid_input = "https://www.youtube.com/embed/" + videoID
        yt = YouTube(url_vid_input)
        tieude = yt.title
        st.markdown("<h4 style='text-align: center; color: brown;'>"+tieude+"</h4>", unsafe_allow_html=True)

        # B1: lay vai thong tin ngan tu url trong do co list cac ban ghi phu de
        transcript_en = YouTubeTranscriptApi.get_transcript(videoID)

        Lap_html_video(transcript_en, videoID)

        st.write('---')
        #st.write(transcript_en)

        #--------------
        t2=time.time()
        st.success('Thoi gian chay: ' + str(int(t2-t1)) + ' sec', icon="✅")
        st.balloons()
    except:
        st.error('Unsuccessful !', icon="🚨")

#------------------
