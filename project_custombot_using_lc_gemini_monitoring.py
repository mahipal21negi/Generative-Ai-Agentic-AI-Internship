import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# set up the api keys for both gemini api and langsmith api keys

gemini_api_key = os.getenv('GOOGLE_API_KEY')

os.environ['LANGSMITH_TRACING_V2'] = 'true'

langsmith_api_key = os.getenv('LANGSMITH_API_KEY')

# PROMPT TEMPLATE

prompt = ChatPromptTemplate.from_messages(
    [
    ("system", "You are a chatbot which is assisting the world about the latest news "),
    ("human", "Question: {Question}\nquestion: {question}")
      
    ]
)



st.title('My first chatbot')
input_text = st.text_input('How may I help you today ? if you write one word I may hallucinate' )


llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 1, max_output_token = 1000 )

out_parser = StrOutputParser()

chain = prompt | llm | out_parser

if input_text:
    with st.spinner('Generating response.....'):
        try:
            response = chain.invoke({'Question': input_text,
                                     "question": input_text})

            st.success('Response Generated Successfully !')
            st.write(response)
        except Exception as e:
            st.error(f'An error occurred: {e}')
