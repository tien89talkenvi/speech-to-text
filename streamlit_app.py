# https://tien89.streamlit.app/     # up ngay 15-11-2023

import streamlit as st
import pyttsx3
import base64
import time

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 125)

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id) # female voice (1)

    def convert(self, text:str, filename: str="hello.mp3"):
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()

        print(f"Saved audio to {filename}")

###########################
txt2speech = TextToSpeech()

st.title('Text To Speech Example')

conversion_text = st.text_input('Text to convert', 'I am Vietnamese. I am from Saigon.')

if st.button('Convert'):
    txt2speech.convert(text=conversion_text)
    audio_placeholder=st.empty()
    with open('hello.mp3', 'rb') as audio_file:
        audio_bytes = audio_file.read()
    #st.audio(audio_bytes, format='audio/mp3')
    audio_b64 = base64.b64encode(audio_bytes).decode()
    my_html=f'''
            <audio controls autoplay>
            <source src="data:audio/mp3;base64,{audio_b64}">
            </audio>
            '''
    audio_placeholder.empty()
    time.sleep(0.2)
    #html(my_html) 
    audio_placeholder.markdown(my_html,unsafe_allow_html=True)

