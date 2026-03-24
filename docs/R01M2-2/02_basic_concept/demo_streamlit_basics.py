# Demo File For Streamlit Basics 
import streamlit as st
import numpy as np
import pandas as pd

# Section1: formatted text elements
st.title("Streamlit Examples - know Basic Elements")
st.header("Header")
st.subheader("Sub Header")

st.text("This is a text")
st.markdown("__This__ is a _**markdown**_")
st.caption("This is a caption")
st.code("print('Hello, World!')", language="python", line_numbers=True)    
st.latex(r'''This\:is\:\LaTeX\:equation: e^{i\pi} + 1 = 0 ''')

with st.echo():
    st.write("This is an echo")

with st.chat_message(name="user"):
    st.write("This is a user chat message")
with st.chat_message(name="assistant"):
    st.write("This is a bot chat message")
    
# Section2: data display elements
df = pd.DataFrame(
    {
        "Ch. #": [1, 2, 3, 4, 5],
        "Title": [
            "Introduction to Streamlit",
            "Setting up the Development Environment",
            "Creating and Deploying Your First Streamlit App",
            "Exploring Streamit's Flow and Architecture",
            "Persisting Data and State Using Session State",
        ],
        "Rating": [3, 3, 3, 3, 3],
    },
)

st.write("This is a static table")
st.table(df)

st.write("This is an interactive table")
st.dataframe(df)

st.write("This is an editable table")
edited_df = st.data_editor(df)

st.write(
    f"Highest rated chapter: __{edited_df['Title'][edited_df['Rating'].idxmax()]}__"
)

st.metric(
    "__Average Rating__",
    edited_df["Rating"].mean(),
    edited_df["Rating"].mean() - df["Rating"].mean(),
)
