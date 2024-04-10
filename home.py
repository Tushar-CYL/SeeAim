import streamlit as st
import time



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
    
      <h2>Ready to Shape Your Career?</h2>
    <
""", unsafe_allow_html=True)

# Introduction
st.success(' ? How To use ?')

st.info('**Step 1:** Begin by uploading your CV/Resume and confirming your domain expertise..', icon="ℹ️")
st.info('**Step 2:** Once your domain is confirmed, you can search for companies relevant to your expertise..', icon="ℹ️")
st.info('**Step 3:** If you re a new user, complete all fields and confirm your domain to access the platforms features..', icon="ℹ️")
st.info('**Step 2:** And you can see the probablity of get a job ..', icon="ℹ️")

html3="""
    <br><br><br>
   <i align="center">   Developed with 🎮🕹️👾 by Our Team</i>
    
      """
      
st.markdown(html3,unsafe_allow_html=True)

