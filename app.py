## this file is responsible for creating LLM applicaton

from dotenv import load_dotenv
load_dotenv() ## load all the environment variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
#configure Genai key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Function to load Google Gemini Modle and provide query as response

def get_gemini_response(question,prompt):
    model= genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text
 
## Function To retrival quwry from the data base

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Pormpt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL datavase has the name STUDENT and has the following columns - NAME, CLASS, SECTION \n\nFor example,\nExample 1 - How many entries of records are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 -Tell me all the students studing in Data Science class ?,
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT where CLASS="Data Science";
    also the SQL code  should not have ''' in beginning or end and sql word in output


    """

]

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Date")

question=st.text_input("Input:",key="input")

submit=st.button("Ask the Question")

## If submit is clicked

if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"student.db")
    st.subheader("The Response is")

    for row in response:
        print(row)
        st.header(row)