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
df.drop(columns=['Person ID', 'Gender', 'Age', 'Occupation'], inplace=True)

sleep_data = df.to_dict(orient='list')

st.subheader('Sleep dataset')
st.write(df)

user_input = st.text_input("Ask Questions", "")

if user_input:  # Check if user input is not empty

    input_prompt = "This is user input: " + user_input + "\n\n and" + "This is sleep data: " + str(sleep_data)
    response = model.generate_content(input_prompt).text
    st.write("Gemini Pro:\n", response)

else:
    st.write("Waiting for user input...")
