import streamlit as st
import time


def main():
    st.info('Registration', icon="ℹ️")
    
    # Text input for name
    f_name = st.text_input("First name")
    
    M_name = st.text_input("Middle name")
    
    l_name = st.text_input("Last name")
    
    # Text input for email
    email = st.text_input("Email")
    
    # Text input for phone number
    phone_number = st.text_input("Phone Number")
    
    p_company = st.text_input("Enter Your Current Company ") 
    
    
    # f_name = st.text_input("First name")
    
    
    agree = st.checkbox('I agree')
    if agree:
        st.write('Great!')
    
    # Submit button
    if st.button("Submit"):
        with st.spinner('Wait for it...'):
            time.sleep(5)
        # st.success('Done!')

        if f_name and M_name and l_name and email and phone_number and p_company:
            st.toast("Welcome to our DataSciHub!")
        else:
            st.error("Please fill out all the fields.")

if __name__ == "__main__":
    main()



