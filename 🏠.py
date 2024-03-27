from cgi import test
from turtle import home
import streamlit as st
import time

# Header
# st.header('Aim🔎Seeker', divider='rainbow')

st.markdown("""
    <div style="text-align:center;">
        <h2>Aim🔎Seeker</h2>
    </div>
""", unsafe_allow_html=True)
st.header('🔎', divider='rainbow')

# Images
col1, col2, col3 = st.columns(3)

with col1:
    st.image("./assets/Career _Isometric.png", use_column_width=True)

with col2:
    st.image("./assets/career.png", use_column_width=True)

with col3:
    st.image("./assets/Career _Outline.png", use_column_width=True)

# Call to Action
st.markdown("""
    <div style="text-align:center; text-shadow: 3px 1px 2px purple;">
      <h2>Ready to Shape Your Career?</h2>
    </div>
""", unsafe_allow_html=True)
# st.header(':blue[_FutureForge_] :green[is] :red[Advanced and Unique] :crown:')

# Introduction
st.markdown("""
    <div style="text-align:center; text-shadow: 3px 1px 2px purple;">
      <h2>How to Use Aim🔎Seeker</h2>
      <p>This platform helps you in finding the right career path and job opportunities based on your skills and preferences.</p>
    </div>
""", unsafe_allow_html=True)

# Explanation

st.markdown("""
    <div style="text-align:center; text-shadow: 3px 1px 2px purple;">
    <p><i><u> **Step 1:** Begin by uploading your CV/Resume and confirming your domain expertise.</u></i></p><br>
   <p><i><u> **Step 2:** Once your domain is confirmed, you can search for companies relevant to your expertise.</u></i></p><br>
    <p><i><u>**Step 3:** If you're a new user, complete all fields and confirm your domain to access the platform's features.</u></i></p>
    </div>
""", unsafe_allow_html=True)


html3="""

    <div style="color:yellow; margin:80px; text-align:center;">
      Developed with 🎮🕹️👾 by <a href=https://github.com/Tushar-CYL>Tushar</a>
      <a href=https://github.com/Tushar-CYL>Aritra</a>
      <a href=https://github.com/Tushar-CYL>Anuj</a>
      <a href=https://github.com/Tushar-CYL>Sunil</a>
      <a href=https://github.com/Tushar-CYL>Rahul</a>
    </div>
      """
      
st.markdown(html3,unsafe_allow_html=True)
# st.write("""
#     **Step 1:** Begin by uploading your CV/Resume and confirming your domain expertise.
    
#     **Step 2:** Once your domain is confirmed, you can search for companies relevant to your expertise.
    
#     **Step 3:** If you're a new user, complete all fields and confirm your domain to access the platform's features.
# """)

# Navigation Links
# st.page_link("Home.py", label="Home", icon="🏠")
# st.page_link("pages/🛄Find_job.py",  icon="🛄")
# st.page_link("pages/🙇‍♂️Predction.py", icon="📌")
# st.page_link("pages/👨‍✈️New_user.py", icon="👩🏻‍🎓")
# st.page_link("pages/📝about_us.py", icon="ℹ️")
# st.page_link("pages/🛡️Login.py",  icon="👤")
