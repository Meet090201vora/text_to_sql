import streamlit as st
import requests
import pandas as pd

st.title("Text-to-SQL Query Executor")

query = st.text_input("Enter your query:")
if st.button("Generate & Execute Query"):
    response = requests.post("http://localhost:8000/text-to-sql", json={"user_query": query})
    if response.status_code == 200:
        data = response.json()
        st.write("### Generated SQL Query")
        st.code(data["query"], language="sql")
        st.write("### Query Results")
        df = pd.DataFrame(data["result"])
        st.dataframe(df)
    else:
        print(response)
        st.error("Error: " + response.json()["detail"])
