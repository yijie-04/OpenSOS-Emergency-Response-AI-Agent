import streamlit as st
import pandas as pd
import plotly.express as px
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import os
from io import StringIO
os.environ["OPENAI_API_KEY"] = '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'
llm = OpenAI(model_name="text-davinci-003",max_tokens=1024)
pandas_ai = PandasAI(llm, conversational=False)


st.title('DEMO#02')
st.header('data visualization & chatbot')
st.subheader('AQ_version')

uploaded_file = st.file_uploader("Choose a file in csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

#df = pd.read_csv('climate_data_ontario.csv')
df.columns = ['Date', 'Max Temp (°C)', 'Min Temp (°C)', 'Mean Temp (°C)', 'Total Rain (mm)', 'Total Snow (cm)', 'Total Precip (mm)', 'Snow on Grnd (cm)']
df['Date'] = pd.to_datetime(df['Date'], format = '%Y%m%d')

st.write(df)

df = pd.DataFrame(df)
df.index = df.iloc[:, 0].values

weather_options = df.columns
weather = st.multiselect('Which weather info would you like to see?', weather_options, ['Max Temp (°C)'])
chart = st.selectbox(
    'Which chart would you like to see?', 
    ('line chart', 'area chart', 'bar chart'))

for option in weather:
    o = df[option]
    if option == weather[0]:
        weather_info = o
    else:
        weather_info = pd.concat([weather_info, o], axis = 1)

if chart == 'line chart':
    st.line_chart(weather_info)
if chart == 'area chart':
    st.area_chart(weather_info)
if chart == 'bar chart':
    st.bar_chart(weather_info)

st.write('Some information about the data are given below')
st.write(weather_info.describe())

weather_info = pd.DataFrame(weather_info, columns = weather)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("say something"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    dumbot = pandas_ai(df, prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(dumbot)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": dumbot})


#df = df[:, df.columns.isin(weather)]

#fig = pd.DataFrame(climate, columns=['Max Temp (°C)', 'Min Temp (°C)', 'Mean Temp (°C)'], dtype=float)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.


# python3 -m venv .venv
# source ./.venv/bin/activate
# streamlit run graph_visualize_0803.py


# https://www.youtube.com/watch?v=VZ_tS4F6P2A


# Show the data in the column where 'Date'=='2022-01-08 00:00:00'
# Show the data of the outlier value in 'Max Temp (°C)'
# Can you summarize three key features of the data?
# Show the mean value of 'Max Temp (°C)' in May
