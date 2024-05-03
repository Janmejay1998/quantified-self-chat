import os
import streamlit as st
import pandas as pd
import google.generativeai as genai

# Set the background image
st.set_page_config(page_title="Quantified Self Chat", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded", menu_items=None)
st.markdown(
    """
    <style>
    body {
        background-image: url("quantified_image.jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Set the environment variable
os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]

def configure_model():
    """Configure the generative model."""
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    return genai.GenerativeModel('gemini-pro')

def load_data():
    """Load and preprocess the data."""
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, delimiter=',')
        df.drop(columns=['Person ID', 'Gender', 'Age', 'Occupation', 'Nurse ID'], inplace=True)
        return df.to_dict(orient='list')

def get_response(model, user_input, sleep_data):
    """Generate a response from the model."""
    input_prompt = f"This is user asking : {user_input}\n\n based on what user asked, this is the sleep data: {str(sleep_data)}\n\n Give me short quantified answer in 1 to 5 lines only based on the sleep data: "
    return model.generate_content(input_prompt).text

def main():
    """Main function to run the app."""
    st.title('The Quantified Self Chat')
    model = configure_model()
    sleep_data = load_data()

    if sleep_data is not None:
    
        st.subheader('Sleep dataset')
        st.write(pd.DataFrame.from_dict(sleep_data))

        # Initialize session state for chat history
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        user_input = st.text_input("Ask Questions", "")

        if st.button("Submit"):  # Check if user input is not empty
            response = get_response(model, user_input, sleep_data)
            # Update chat history
            st.session_state['chat_history'].append({"User": user_input, "Gemini Pro": response})

        # Display chat history
        for chat in st.session_state['chat_history']:
            st.write(f"User: {chat['User']}")
            st.write(f"Gemini Pro: {chat['Gemini Pro']}")
    
    else:
        st.write("Please upload a CSV file to load the sleep data.")

if __name__ == "__main__":
    main()
