import streamlit as st

# md = st.text_area('Type in your markdown string (without outer quotes)',
#                   "Happy Streamlit-ing! :balloon:")

# st.code(f"""
# import streamlit as st

# st.markdown('''{md}''')
# """)

# st.markdown(md)



st.title(':blue[A Data Science Project for Career Prediction and Company Recommendation]')

st.header(':green[Introduction]')
st.info(':yellow[At VIT (Vellore Institute of Technology), we are proud to present our innovative data science project aimed at revolutionizing career guidance and company recommendations. Leveraging cutting-edge technologies such as NLP (Natural Language Processing), Pandas, NumPy, Matplotlib, Seaborn, Pickle, and XGBoost, our team of five dedicated members embarked on a journey to empower individuals with data-driven insights into their career trajectories.]', icon="ℹ️")

st.header(':red[Data Acquisition and Cleaning]')
st.warning(':yellow[Our project begins with the extraction of data from various websites, encompassing a wide range of job postings, industry reports, and skill requirements. Through meticulous web scraping techniques, we amassed a rich dataset representing diverse job markets and domains. Subsequently, employing robust data cleaning methodologies, we ensured the integrity and quality of our dataset, eliminating noise and inconsistencies to lay a solid foundation for analysis.]')

st.header(':blue[Predictive Modeling]')
st.info(':yellow[Utilizing NLP techniques and XGBoost algorithms, we developed predictive models to extract key skills and qualifications from resumes. These models accurately predict the domain or field of expertise of individuals, empowering them with personalized career insights.]')

st.header(':green[Company Prediction]')
st.warning(':yellow[Our system recommends suitable companies based on user-input location and skill set. By analyzing location-based data and company profiles, we offer tailored recommendations, along with estimations of compatibility for each recommended company.]')





# Check if the file exists
import time
st.header(":red[Meet Our Team Members]")
if st.button('Our Team'):
    st.toast(':blue[Sunil!]')
    time.sleep(.5)
    st.toast(':green[Aritra!]')
    time.sleep(.5)
    st.toast(':red[Tushar!]')
    time.sleep(.5)
    st.toast(':blue[Anuj!]')
    time.sleep(.5)
    st.toast(':green[Rahul!]')

    # st.image('./assets/t.jpg')
    

# container = st.container(border=True)
# container.warning("")