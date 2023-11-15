import streamlit as st 
import pyttsx3

engine = pyttsx3.init()

# Lấy danh sách giọng nói
voices = engine.getProperty('voices')

butt=st.button('click')

if butt:
    # In thông tin về từng giọng nói
    for voice in voices:
        # print(f"ID: {voice.id}, Name: {voice.name}, Lang: {voice.languages}")
        st.write(f"ID: {voice.id}, Name: {voice.name}, Lang: {voice.languages}")

