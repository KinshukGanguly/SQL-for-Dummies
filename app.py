from dotenv import load_dotenv
load_dotenv()  

import streamlit as st
import os
import sqlite3
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content([prompt[0], question])
    return response.text


def execute_sql_command(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        if sql.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            return rows
        else:
            conn.commit()
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()


prompt = [
    """
You are an expert in converting natural language questions into accurate and optimized SQL queries. Your task is to analyze user input carefully and generate the most relevant SQL command. 

### **Instructions for Query Generation:**  
- The database name is flexible and not explicitly mentioned in queries.  
- Table names and column names are user-defined, so interpret user input contextually.  
- Adapt to synonyms, abbreviations, and variations in phrasing. For example:
  - "roll" refers to "Roll number"  
  - "grade" corresponds to "Grade"  
  - "how many students?" should translate to `SELECT COUNT(*) FROM STUDENT;`  
- Ensure the SQL syntax is correct, efficient, and follows best practices.  
- Avoid including unnecessary elements like "SQL" or enclosing the code in triple backticks (```).  

### **Example Cases:**  

1. **Table Creation Requests:**  
   - **User Input:** "Create a table TEACHER with columns NAME and SUBJECT."  
   - **Output:** `CREATE TABLE TEACHER (NAME VARCHAR(255), SUBJECT VARCHAR(255));`  

   - **User Input:** "Create a STUDENT table with NAME, CLASS, SECTION, and AGE."  
   - **Output:** `CREATE TABLE STUDENT (NAME VARCHAR(255), CLASS VARCHAR(255), SECTION VARCHAR(255), AGE INT);`  

2. **Data Insertion Requests:**  
   - **User Input:** "Add a new student named John in Data Science class A."  
   - **Output:** `INSERT INTO STUDENT (NAME, CLASS, SECTION) VALUES ('John', 'Data Science', 'A');`  

   - **User Input:** "Insert a teacher Jane who teaches Mathematics."  
   - **Output:** `INSERT INTO TEACHER (NAME, SUBJECT) VALUES ('Jane', 'Mathematics');`  

3. **Data Retrieval Queries:**  
   - **User Input:** "Show all students in class A."  
   - **Output:** `SELECT * FROM STUDENT WHERE SECTION = 'A';`  

   - **User Input:** "Get the total number of students."  
   - **Output:** `SELECT COUNT(*) FROM STUDENT;`  

4. **Update Requests:**  
   - **User Input:** "Update John's class to Machine Learning."  
   - **Output:** `UPDATE STUDENT SET CLASS = 'Machine Learning' WHERE NAME = 'John';`  

   - **User Input:** "Change the subject of Jane to Physics."  
   - **Output:** `UPDATE TEACHER SET SUBJECT = 'Physics' WHERE NAME = 'Jane';`  

5. **Deletion Requests:**  
   - **User Input:** "Remove the student named John."  
   - **Output:** `DELETE FROM STUDENT WHERE NAME = 'John';`  

   - **User Input:** "Drop the TEACHER table."  
   - **Output:** `DROP TABLE IF EXISTS TEACHER;`  

6. **Advanced Queries:**  
   - **User Input:** "List all students who scored above 80 in Mathematics."  
   - **Output:** `SELECT * FROM STUDENT WHERE SUBJECT = 'Mathematics' AND GRADE > 80;`  

   - **User Input:** "Find the average grade of students in Data Science."  
   - **Output:** `SELECT AVG(GRADE) FROM STUDENT WHERE CLASS = 'Data Science';`  

### **Additional Considerations:**  
- Handle plural and singular variations (e.g., "students" vs. "student").  
- Consider edge cases like missing column names or ambiguous phrases by making the best reasonable assumption.  
- Do not generate queries with hardcoded assumptions unless explicitly mentioned by the user.  
- Be cautious with SQL injection attacks by properly sanitizing user input.
"""
]


st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    result = execute_sql_command(response, "test.db")
    
    st.subheader("The Response is")
    if result is not None:
        for row in result:
            print(row)
            st.header(row)
    else:
        st.write("Command executed successfully or no results to display.")