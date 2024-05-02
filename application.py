import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai

import os

# Set the environment variable
os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

st.title('The Quantified Self Chat')

model = genai.GenerativeModel('gemini-pro')

df = pd.read_csv('sleep_data.csv', delimiter=',')
df.drop(columns=['Person ID', 'Gender', 'Age', 'Occupation', 'Nurse ID'], inplace=True)

sleep_data = df.to_dict(orient='list')

st.subheader('Sleep dataset')
st.write(df)

user_input = st.text_input("Ask Questions", "")

if user_input:  # Check if user input is not empty

    better_prompt = "Make this:" + user_input + " into this good question to be asked"
    prompt = model.generate_content(better_prompt).text
    input_prompt = "This is user asking : " + prompt + "\n\n based on what user asked, this is the sleep data:" + str(sleep_data) + "\n\n Give me short quantified answer in 1 to 5 lines only based on the sleep data: "
    response = model.generate_content(input_prompt).text
    st.write("Gemini Pro:\n", response)

else:
    st.write("Waiting for user input...")
