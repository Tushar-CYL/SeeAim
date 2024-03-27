import streamlit as st
import pickle
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Loading models
clf = pickle.load(open('clf.pkl','rb'))
tfidfd = pickle.load(open('tfidf.pkl','rb'))

def clean_resume(resume_txt):
    clean_text = re.sub('http\S+\s', ' ', resume_txt)
    clean_text = re.sub('@\S+', ' ', clean_text)
    clean_text = re.sub('#\S+', ' ', clean_text)
    clean_text = re.sub('RT|cc', ' ', clean_text)
    clean_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', ' ', clean_text)
    clean_text = re.sub('\s+', ' ', clean_text)
    return clean_text

# Web app
def main():
    st.title("Resume Screening App")
    uploaded_file = st.file_uploader('Upload Resume', type=['txt', 'pdf'])

    if uploaded_file is not None:
        try:
            resume_bytes = uploaded_file.read()
            resume_text = resume_bytes.decode('utf-8')
            st.p(resume_text)
        except UnicodeDecodeError:
            # If UTF-8 decoding fails, try decoding with 'latin-1'
            resume_text = resume_bytes.decode('latin-1')

        cleaned_resume = clean_resume(resume_text)
        

# Transform the cleaned resume using the trained TfidfVectorizer
        input_features = tfidfd.transform([cleaned_resume])

# Make the prediction using the loaded classifier
        prediction_id = clf.predict(input_features)[0]

        # Map category ID to category name
        category_mapping = {
            0: "Advocate",
            1: "Arts",
            2: "Automation Testing",
            3: "Blockchain",
            4: "Business Analyst",
            5: "Civil Engineer",
            6: "Data Science",
            7: "Database",
            8: "DevOps Engineer",
            9: "DotNet Developer",
            10: "ETL Developer",
            11: "Electrical Engineering",
            12: "HR",
            13: "Hadoop",
            14: "Health and fitness",
            15: "Java Developer",
            16: "Mechanical Engineer",
            17: "Network Security Engineer",
            18: "Operations Manager",
            19: "PMO",
            20: "Python Developer",
            21: "SAP Developer",
            22: "Sales",
            23: "Testing",
            24: "Web Designing"
        }

        category_name = category_mapping.get(prediction_id, "Unknown")
        st.write("Predicted Category:", category_name)

# Python main
if __name__ == "__main__":
    main()











import streamlit as st
import pickle
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Load the trained classifier
clf = pickle.load(open('clf.pkl', 'rb'))
# Load the trained TfidfVectorizer
tfidf = pickle.load(open('tfidf.pkl', 'rb'))

def clean_resume(resume_txt):
    clean_text = re.sub(r'http\S+', ' ', resume_txt)
    clean_text = re.sub(r'@\S+', ' ', clean_text)
    clean_text = re.sub(r'#\S+', ' ', clean_text)
    clean_text = re.sub(r'RT|cc', ' ', clean_text)
    clean_text = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text

def main():
    st.title("Resume Screening App")
    myresume = st.text_area("Paste your resume here:")
    
    if st.button("Predict"):
        cleaned_resume = clean_resume(myresume)
        input_features = tfidf.transform([cleaned_resume])
        prediction_id = clf.predict(input_features)[0]

        # Map category ID to category name
        category_mapping = {
            15: "Java Developer",
            23: "Testing",
            8: "DevOps Engineer",
            20: "Python Developer",
            24: "Web Designing",
            12: "HR",
            13: "Hadoop",
            3: "Blockchain",
            10: "ETL Developer",
            18: "Operations Manager",
            6: "Data Science",
            22: "Sales",
            16: "Mechanical Engineer",
            1: "Arts",
            7: "Database",
            11: "Electrical Engineering",
            14: "Health and fitness",
            19: "PMO",
            4: "Business Analyst",
            9: "DotNet Developer",
            2: "Automation Testing",
            17: "Network Security Engineer",
            21: "SAP Developer",
            5: "Civil Engineer",
            0: "Advocate",
        }

        category_name = category_mapping.get(prediction_id, "Unknown")
        st.write("Predicted Category:", category_name)

if __name__ == "__main__":
    main()










import streamlit as st
import docx2txt
import re
import pickle
import re
import nltk


nltk.download('punkt')
nltk.download('stopwords')

# Load the trained classifier
clf = pickle.load(open('clf.pkl', 'rb'))
# Load the trained TfidfVectorizer
tfidf = pickle.load(open('tfidf.pkl', 'rb'))



def extract_text_from_docx(file_path):
    text = docx2txt.process(file_path)
    return text

def extract_skills(text):
    # Regular expression to find sections that contain skills
    # Modify this regex based on the structure of the resumes you expect
    # This example assumes that skills are listed in bullet points or as comma-separated values
    skill_sections = re.findall(r'(?<=skills)[:\n]?(.*?)(?=\n\n|\n\w+:|$)', text, re.IGNORECASE | re.DOTALL)
    skills = []
    for section in skill_sections:
        skills.extend(re.findall(r'\b\w+\b', section))
    return skills

def extract_name_and_phone(text):
    # Regular expression to extract name and phone number
    # Modify this regex based on the structure of the resumes you expect
    name_match = re.search(r'\b[a-zA-Z\s]+\b', text)
    name = name_match.group() if name_match else "Name not found"
    
    phone_match = re.search(r'\b\d{10}\b', text)
    phone = phone_match.group() if phone_match else "Phone number not found"
    
    return name, phone

def main():
    st.title("Resume Analysis")
    uploaded_file = st.file_uploader("Upload a resume", type=['pdf', 'docx'])
    if uploaded_file is not None:
        try:
            resume_bytes = uploaded_file.read()
            resume_text = resume_bytes.decode('utf-8')
            st.p(resume_text)
        except UnicodeDecodeError:
            # If UTF-8 decoding fails, try decoding with 'latin-1'
            resume_text = resume_bytes.decode('latin-1')
            
            
            
    if uploaded_file is not None:
        text = ""
        if uploaded_file.type == "application/pdf":
            st.write("PDF file format not supported yet. Please upload a DOCX file.")
            return
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
        skills = extract_skills(text)
        name, phone = extract_name_and_phone(text)
        st.header("Name and Phone Number")
        st.write(f"Name: {name}")
        st.write(f"Phone Number: {phone}")
        st.header("Extracted Skills")
        if skills:
            for skill in skills:
                st.write(skill)
        else:
            st.write("No skills extracted.")
            
        cleaned_resume = clean_resume(resume_text)
        input_features = tfidfd.transform([cleaned_resume])

# Make the prediction using the loaded classifier
        prediction_id = clf.predict(input_features)[0]

        # Map category ID to category name
        category_mapping = {
            0: "Advocate",
            1: "Arts",
            2: "Automation Testing",
            3: "Blockchain",
            4: "Business Analyst",
            5: "Civil Engineer",
            6: "Data Science",
            7: "Database",
            8: "DevOps Engineer",
            9: "DotNet Developer",
            10: "ETL Developer",
            11: "Electrical Engineering",
            12: "HR",
            13: "Hadoop",
            14: "Health and fitness",
            15: "Java Developer",
            16: "Mechanical Engineer",
            17: "Network Security Engineer",
            18: "Operations Manager",
            19: "PMO",
            20: "Python Developer",
            21: "SAP Developer",
            22: "Sales",
            23: "Testing",
            24: "Web Designing"
        }

        category_name = category_mapping.get(prediction_id, "Unknown")
        st.write("Predicted Category:", category_name)

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# import streamlit as st
# import docx2txt
# import re
# import pickle
# import nltk
# from sklearn.feature_extraction.text import TfidfVectorizer

# nltk.download('punkt')
# nltk.download('stopwords')

# # Load the trained classifier
# clf = pickle.load(open('clf.pkl', 'rb'))
# # Load the trained TfidfVectorizer
# tfidf = pickle.load(open('tfidf.pkl', 'rb'))

# def extract_text_from_docx(file_path):
#     text = docx2txt.process(file_path)
#     return text

# def extract_skills(text):
#     # Regular expression to find sections that contain skills
#     # Modify this regex based on the structure of the resumes you expect
#     # This example assumes that skills are listed in bullet points or as comma-separated values
#     skill_sections = re.findall(r'(?<=skills)[:\n]?(.*?)(?=\n\n|\n\w+:|$)', text, re.IGNORECASE | re.DOTALL)
#     skills = []
#     for section in skill_sections:
#         skills.extend(re.findall(r'\b\w+\b', section))
#     return skills

# def extract_name_and_phone(text):
#     # Regular expression to extract name and phone number
#     # Modify this regex based on the structure of the resumes you expect
#     name_match = re.search(r'\b[a-zA-Z\s]+\b', text)
#     name = name_match.group() if name_match else "Name not found"
    
#     phone_match = re.search(r'\b\d{10}\b', text)
#     phone = phone_match.group() if phone_match else "Phone number not found"
    
#     return name, phone

# def main():
#     st.title("Resume Analysis")
#     uploaded_file = st.file_uploader("Upload a resume", key="resume_uploader", type=['pdf', 'docx'])
#     if uploaded_file is not None:
#         try:
#             resume_bytes = uploaded_file.read()
#             if uploaded_file.type == "application/pdf":
#                 st.write("PDF file format not supported yet. Please upload a DOCX file.")
#                 return
#             elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#                 resume_text = extract_text_from_docx(uploaded_file)
#                 st.write(resume_text)
                
#                 skills = extract_skills(resume_text)
#                 name, phone = extract_name_and_phone(resume_text)
#                 st.header("Name and Phone Number")
#                 st.write(f"Name: {name}")
#                 st.write(f"Phone Number: {phone}")
#                 st.header("Extracted Skills")
#                 if skills:
#                     for skill in skills:
#                         st.write(skill)
#                 else:
#                     st.write("No skills extracted.")

#                 input_features = tfidf.transform([resume_text])

#                 prediction_id = clf.predict(input_features)[0]

#                 category_mapping = {
#                     0: "Advocate",
#                     1: "Arts",
#                     2: "Automation Testing",
#                     3: "Blockchain",
#                     4: "Business Analyst",
#                     5: "Civil Engineer",
#                     6: "Data Science",
#                     7: "Database",
#                     8: "DevOps Engineer",
#                     9: "DotNet Developer",
#                     10: "ETL Developer",
#                     11: "Electrical Engineering",
#                     12: "HR",
#                     13: "Hadoop",
#                     14: "Health and fitness",
#                     15: "Java Developer",
#                     16: "Mechanical Engineer",
#                     17: "Network Security Engineer",
#                     18: "Operations Manager",
#                     19: "PMO",
#                     20: "Python Developer",
#                     21: "SAP Developer",
#                     22: "Sales",
#                     23: "Testing",
#                     24: "Web Designing"
#                 }

#                 category_name = category_mapping.get(prediction_id, "Unknown")
#                 st.write("Predicted Category:", category_name)
#         except UnicodeDecodeError:
#             st.write("Error: Unable to read the file. Please ensure it is in a readable format.")

# if __name__ == "__main__":
#     main()







import streamlit as st
import docx2txt
import re
import pickle
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')

# Load the trained classifier
clf = pickle.load(open('clf.pkl', 'rb'))
# Load the trained TfidfVectorizer
tfidf = pickle.load(open('tfidf.pkl', 'rb'))

def extract_text_from_docx(file_path):
    text = docx2txt.process(file_path)
    return text

def extract_skills(text):
    # Regular expression to find sections that contain skills
    # Modify this regex based on the structure of the resumes you expect
    # This example assumes that skills are listed in bullet points or as comma-separated values
    skill_sections = re.findall(r'(?<=skills)[:\n]?(.*?)(?=\n\n|\n\w+:|$)', text, re.IGNORECASE | re.DOTALL)
    skills = []
    for section in skill_sections:
        skills.extend(re.findall(r'\b\w+\b', section))
    return skills

def extract_name_and_phone(text):
    # Regular expression to extract name and phone number
    # Modify this regex based on the structure of the resumes you expect
    name_match = re.search(r'\b[a-zA-Z\s]+\b', text)
    name = name_match.group() if name_match else "Name not found"
    
    phone_match = re.search(r'\b\d{10}\b', text)
    phone = phone_match.group() if phone_match else "Phone number not found"
    
    return name, phone

def main():
    st.title("Resume Analysis")
    uploaded_file = st.file_uploader("Upload a resume", key="resume_uploader", type=['pdf', 'docx'])
    if uploaded_file is not None:
        try:
            resume_bytes = uploaded_file.read()
            if uploaded_file.type == "application/pdf":
                st.write("PDF file format not supported yet. Please upload a DOCX file.")
                return
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(uploaded_file)
                st.write(resume_text)
                
                skills = extract_skills(resume_text)
                name, phone = extract_name_and_phone(resume_text)
                st.header("Name and Phone Number")
                st.write(f"Name: {name}")
                st.write(f"Phone Number: {phone}")
                st.header("Extracted Skills")
                if skills:
                    for skill in skills:
                        st.write(skill)
                else:
                    st.write("No skills extracted.")

                input_features = tfidf.transform([resume_text])

                prediction_id = clf.predict(input_features)[0]

                category_mapping = {
                    0: "Advocate",
                    1: "Arts",
                    2: "Automation Testing",
                    3: "Blockchain",
                    4: "Business Analyst",
                    5: "Civil Engineer",
                    6: "Data Science",
                    7: "Database",
                    8: "DevOps Engineer",
                    9: "DotNet Developer",
                    10: "ETL Developer",
                    11: "Electrical Engineering",
                    12: "HR",
                    13: "Hadoop",
                    14: "Health and fitness",
                    15: "Java Developer",
                    16: "Mechanical Engineer",
                    17: "Network Security Engineer",
                    18: "Operations Manager",
                    19: "PMO",
                    20: "Python Developer",
                    21: "SAP Developer",
                    22: "Sales",
                    23: "Testing",
                    24: "Web Designing"
                }

                category_name = category_mapping.get(prediction_id, "Unknown")
                st.header("Predicted Category:")
                if prediction_id in category_mapping:
                    st.markdown(f"**{category_name}**")
                else:
                    st.write("Unknown category")

        except UnicodeDecodeError:
            st.write("Error: Unable to read the file. Please ensure it is in a readable format.")

if __name__ == "__main__":
    main()




