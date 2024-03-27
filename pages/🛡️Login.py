# import streamlit as st
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import auth

# st.set_page_config(page_title="Registration", page_icon="ℹ️")

# if not firebase_admin._apps:
#     cred = credentials.Certificate("pages/datasci-45410-66555c180fd9.json")
#     firebase_admin.initialize_app(cred)

# def app():
#     st.title('Welcome to :blue[DataSciHub] ')

#     if 'username' not in st.session_state:
#         st.session_state.username = ''
#     if 'useremail' not in st.session_state:
#         st.session_state.useremail = ''

#     def f(email): 
#         try:
#             user = auth.get_user_by_email(email)
#             st.session_state.username = user.uid
#             st.session_state.useremail = user.email
#             st.session_state.signedout = True
#             st.session_state.signout = True    
#         except: 
#             st.warning('Login Failed')

#     def t():
#         st.session_state.signout = False
#         st.session_state.signedout = False   
#         st.session_state.username = ''
#         st.session_state.useremail = ''
    
#     if "signedout"  not in st.session_state:
#         st.session_state["signedout"] = False
#     if 'signout' not in st.session_state:
#         st.session_state['signout'] = False    
    
#     if not st.session_state["signedout"]:
#         choice = st.selectbox('Login/Signup',['Login','Sign up'])
#         email = st.text_input('Email Address')
#         password = st.text_input('Password',type='password')
        
#         if choice == 'Sign up':
#             username = st.text_input("Enter your unique username")
#             if st.button('Create my account'):
#                 if username and '@' in email and '.' in email:
#                     user = auth.create_user(email=email, password=password, uid=username)
#                     st.success('Account created successfully!')
#                     st.markdown('Please Login using your email and password')
#                     st.balloons()
#                 else:
#                     st.warning('Username cannot be empty and please provide a valid email address')
#         else:
#             if st.button('Login'):
#                 f(email)
                
#     if st.session_state.signout:
#         # st.text('Name '+st.session_state.username)
#         # st.text('Email id: '+st.session_state.useremail)
#         # st.button('Sign out', on_click=t) 
#         st.info('Login Successful')
                
#     def ap():
#         st.write('Posts')

# app()


# import streamlit as st
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import auth

# st.set_page_config(page_title="Registration", page_icon="ℹ️")

# if not firebase_admin._apps:
#     cred = credentials.Certificate("pages/datasci-45410-66555c180fd9.json")
#     firebase_admin.initialize_app(cred)

# def app():
#     st.title('Welcome to :blue[DataSciHub] ')

#     if 'username' not in st.session_state:
#         st.session_state.username = ''
#     if 'useremail' not in st.session_state:
#         st.session_state.useremail = ''

#     def f(email): 
#         try:
#             user = auth.get_user_by_email(email)
#             st.session_state.username = user.uid
#             st.session_state.useremail = user.email
#             st.session_state.signedout = True
#             st.session_state.signout = True    
#         except: 
#             st.error('Login Failed')
#             st.toast("Please fill out all the fields.")

#     def google_login():
#         try:
#             user = auth.get_user_by_provider_uid('google.com', 'project-672871393112')
#             st.session_state.username = user.uid
#             st.session_state.useremail = user.email
#             st.session_state.signedout = True
#             st.session_state.signout = True    
#         except: 
#             st.error('Google Login Failed')

#     def t():
#         st.session_state.signout = False
#         st.session_state.signedout = False   
#         st.session_state.username = ''
#         st.session_state.useremail = ''
    
#     if "signedout"  not in st.session_state:
#         st.session_state["signedout"] = False
#     if 'signout' not in st.session_state:
#         st.session_state['signout'] = False    
    
#     if not st.session_state["signedout"]:
#         choice = st.selectbox('Login/Signup',['Login','Sign up'])
#         if choice == 'Sign up':
#             email = st.text_input('Email Address')
#             username = st.text_input("Enter your unique username")
#             password = st.text_input('Password',type='password')
#             if st.button('Create my account'):
#                 if username and '@' in email and '.' in email:
#                     user = auth.create_user(email=email, password=password, uid=username)
#                     st.success('Account created successfully!')
#                     st.markdown('Please Login using your email and password')
#                     st.balloons()
#                 else:
#                     st.warning('Username cannot be empty and please provide a valid email address')
#         elif choice == 'Login':
#             email = st.text_input('Email Address')
#             password = st.text_input('Password',type='password')
#             if st.button('Login'):
#                 f(email)
#             st.markdown('Or')
#             if st.button('Login with Google'):
#                 google_login()
                
#     if st.session_state.signout:
#         # Redirect to another page after successful login or signup
#         st.query_params["page"] = "prediction"
                
#     def ap():
#         st.write('Posts')

# app()


import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from google.oauth2 import id_token
from google.auth.transport import requests
import time

# Set Streamlit page configuration
st.set_page_config(page_title="Registration", page_icon="ℹ️")

# Initialize Firebase app if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("pages/datasci-45410-66555c180fd9.json")
    firebase_admin.initialize_app(cred)

def app():
    st.title('Welcome to :blue[Aim🔎Seeker] ')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f(email): 
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True
            st.success("Login Successful! Thank You Welcome to DataSciHub")
            st.toast('You can now access all features.')
            st.snow()
            
        except: 
            st.warning('Login Failed')

    def google_login(id_token):
        try:
            # Verify Google ID token
            decoded_token = id_token.verify_oauth2_token(id_token, requests.Request())
            email = decoded_token['email']

            # Perform Firebase login
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True
            st.success("Login Successful! You can now access all features.")    
        except Exception as e: 
            st.warning(f'Google Login Failed: {str(e)}')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''
        st.session_state.useremail = ''
    
    if "signedout"  not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    
    
    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup',['Login','Sign up'])
        if choice == 'Sign up':
            email = st.text_input('Email Address')
            username = st.text_input("Enter your unique username")
            password = st.text_input('Password',type='password')
            if st.button('Create my account'):
                if username and '@' in email and '.' in email:
                    user = auth.create_user(email=email, password=password, uid=username)
                    st.success('Account created successfully!')
                    st.markdown('Please Login using your email and password')
                    st.balloons()
                else:
                    st.warning('Fill all the criteria')
        elif choice == 'Login':
            email = st.text_input('Email Address')
            password = st.text_input('Password',type='password')
            if st.button('Login'):
                f(email)
            
    
    if st.session_state.signout:
   
 
  
     def ap():
        st.write('Posts')

app()







