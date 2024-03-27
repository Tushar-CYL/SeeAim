
# import streamlit as st
# import docx2txt
# import re
# import pickle
# import re
# # import nltk
# from sklearn.feature_extraction.text import TfidfVectorizer
# # nltk.download('punkt')
# # nltk.download('stopwords')

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
#     st.title(":blue[Upload] :green[your] :red[resume]")
#     uploaded_file = st.file_uploader(":red[Upload a resume:]", key="resume_uploader", type=['pdf', 'docx'])
#     if uploaded_file is not None:
#         try:
#             resume_bytes = uploaded_file.read()
#             if uploaded_file.type == "application/pdf":
#                 st.write("blue[PDF file format not supported yet. Please upload a DOCX file.]")
#                 return
#             elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#                 resume_text = extract_text_from_docx(uploaded_file)
#                 st.write(resume_text)
                
#                 skills = extract_skills(resume_text)
#                 name, phone = extract_name_and_phone(resume_text)
#                 st.header(":blue[Name and Phone Number]")
#                 st.write(f":blue[Name:] {name}")
#                 st.write(f":blue[Phone Number:] {phone}")
#                 st.header(":blue[Extracted Skills]")
#                 if skills:
#                     for skill in skills:
#                         st.write(skill)
#                 else:
#                     st.write(":red[No skills extracted.]")

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
#                     15: "Android Developer",
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
#                 st.header(":red[Predicted Category:]")
#                 if prediction_id in category_mapping:
#                     st.markdown(f"**{category_name}**")
#                 else:
#                     st.write(":red[Unknown category]")

#         except UnicodeDecodeError:
#             st.write(":red[Error: Unable to read the file. Please ensure it is in a readable format.]")

# if __name__ == "__main__":
#     main()




# import streamlit as st
# import docx2txt
# import re
# import pickle
# from sklearn.feature_extraction.text import TfidfVectorizer

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
#     st.title(":blue[Resume Analyzer]")
#     uploaded_file = st.file_uploader("Upload your resume:", type=['pdf', 'docx'])
#     if uploaded_file is not None:
#         try:
#             resume_bytes = uploaded_file.read()
#             if uploaded_file.type == "application/pdf":
#                 st.warning("PDF file format not supported yet. Please upload a DOCX file.")
#                 return
#             elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#                 resume_text = extract_text_from_docx(uploaded_file)
#                 st.write(resume_text)
                
#                 skills = extract_skills(resume_text)
#                 name, phone = extract_name_and_phone(resume_text)

#                 st.subheader("Name and Phone Number")
#                 st.write(f"Name: {name}")
#                 st.write(f"Phone Number: {phone}")

#                 st.subheader("Extracted Skills")
#                 if skills:
#                     for skill in skills:
#                         st.write(skill)
#                 else:
#                     st.warning("No skills extracted.")

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
#                     15: "Android Developer",
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

#                 st.subheader("Predicted Category:")
#                 st.write(category_name)

#         except UnicodeDecodeError:
#             st.error("Error: Unable to read the file. Please ensure it is in a readable format.")

# if __name__ == "__main__":
#     main()













import streamlit as st
import docx2txt
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

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
    # Custom CSS styles
    custom_css = """
    <style>
    .title-text {
        color: #0066cc;
        font-size: 32px;
        text-align: center;
        margin-bottom: 20px;
    }
    .file-upload {
        text-align: center;
        margin-bottom: 20px;
    }
    .file-upload input[type="file"] {
        display: none;
    }
    .file-upload label {
        background-color: #0066cc;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .file-upload label:hover {
        background-color: #005cbf;
    }
    .info-section {
        margin-bottom: 20px;
    }
    .info-section-header {
        font-size: 24px;
        color: #333333;
        margin-bottom: 10px;
    }
    .info-text {
        font-size: 18px;
        color: #666666;
    }
    .predicted-category {
        font-size: 24px;
        color: #cc0000;
        margin-top: 20px;
    }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

    st.markdown('<h1 class="title-text">📄 Resume Analyzer</h1>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader('', type=['pdf', 'docx'], help="Supported formats: PDF, DOCX", key='file_uploader')

    if uploaded_file is not None:
        try:
            resume_bytes = uploaded_file.read()
            if uploaded_file.type == "application/pdf":
                st.error("PDF file format is not supported yet. Please upload a DOCX file.")
                return
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(uploaded_file)
                
                skills = extract_skills(resume_text)
                name, phone = extract_name_and_phone(resume_text)

                st.markdown('<div class="info-section">', unsafe_allow_html=True)
                st.markdown('<h2 class="info-section-header">Name and Phone Number</h2>', unsafe_allow_html=True)
                st.markdown(f'<p class="info-text"><strong>Name:</strong> {name}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="info-text"><strong>Phone Number:</strong> {phone}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="info-section">', unsafe_allow_html=True)
                st.markdown('<h2 class="info-section-header">Extracted Skills</h2>', unsafe_allow_html=True)
                if skills:
                    for skill in skills:
                        st.markdown(f'<p class="info-text">{skill}</p>', unsafe_allow_html=True)
                else:
                    st.warning("No skills extracted.")
                st.markdown('</div>', unsafe_allow_html=True)

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
                    15: "Android Developer",
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

                st.markdown('<div class="predicted-category">', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Predicted Category:</strong> {category_name}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        except UnicodeDecodeError:
            st.error("Error: Unable to read the file. Please ensure it is in a readable format.")

if __name__ == "__main__":
    main()
