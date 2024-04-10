# import time
# import numpy as np
# import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd


# def streamlit_config():
#     # page configuration
#     st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)

#     # title and position
#     st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)

# class linkedin_scraper:

#     def webdriver_setup():
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')

#         driver = webdriver.Chrome(options=options)
#         driver.maximize_window()
#         return driver

#     def get_userinput():
#         add_vertical_space(2)
#         with st.form(key='linkedin_scarp'):
#             add_vertical_space(1)
#             col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
#             with col1:
#                 job_title_input = st.text_input(label='Job Title')
#                 job_title_input = job_title_input.split(',')
#             with col2:
#                 job_location = st.text_input(label='Job Location', value='India')
#             with col3:
#                 company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

#             # Submit Button
#             add_vertical_space(1)
#             submit = st.form_submit_button(label='Submit')
#             add_vertical_space(1)
        
#         return job_title_input, job_location, company_count, submit

#     def build_url(job_title, job_location):
#         b = []
#         for i in job_title:
#             x = i.split()
#             y = '%20'.join(x)
#             b.append(y)

#         job_title = '%2C%20'.join(b)
#         link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

#         return link
    
#     def open_link(driver, link):
#         while True:
#             # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
#             try:
#                 driver.get(link)
#                 driver.implicitly_wait(5)
#                 time.sleep(3)
#                 driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
#                 return
            
#             # Retry Loading the Page
#             except NoSuchElementException:
#                 continue

#     def link_open_scrolldown(driver, link, company_count):
#         # Open the Link in LinkedIn
#         linkedin_scraper.open_link(driver, link)
#         time.sleep(3)
        
#         # Scraping the Company Data
#         companies_scraped = 0
#         while companies_scraped < company_count:
#             # Scroll Down the Page to load more companies
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Check if there's a "See more" button and click it
#             try:
#                 see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
#                 see_more_button.click()
#                 time.sleep(3)
#             except NoSuchElementException:
#                 break  # No more "See more" button, exit the loop
            
#             # Update the number of scraped companies
#             companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

#         return

#     def scrap_company_data(driver, job_title_input, job_location):
#         # scraping the Company Data
#         company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
#         company_name = [i.text for i in company]

#         location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
#         company_location = [i.text for i in location]

#         title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
#         job_title = [i.text for i in title]

#         url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
#         website_url = [i.get_attribute('href') for i in url]

#         # combine the all data to single dataframe
#         df = pd.DataFrame(company_name, columns=['Company Name'])
#         df['Job Title'] = pd.DataFrame(job_title)
#         df['Location'] = pd.DataFrame(company_location)
#         df['Website URL'] = pd.DataFrame(website_url)

#         # Return Job Title if there are more than 1 matched word else return NaN
#         df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

#         # Return Location if User Job Location in Scraped Location else return NaN
#         df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
#         # Drop Null Values and Reset Index
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)

#         return df 

#     def scrap_job_description(driver, df, company_count):
#         # Get URL into List
#         website_url = df['Website URL'].tolist()
        
#         # Scrap the Job Description
#         job_description, description_count = [], 0
#         for i in range(0, len(website_url)):
#             try:
#                 # Open the Link in LinkedIn
#                 linkedin_scraper.open_link(driver, website_url[i])

#                 # Click on Show More Button
#                 driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
#                 driver.implicitly_wait(5)
#                 time.sleep(1)

#                 # Get Job Description
#                 description = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')
#                 data = [i.text for i in description][0]

#                 if len(data.strip()) > 0:
#                     job_description.append(data)
#                     description_count += 1
#                 else:
#                     job_description.append('Description Not Available')
            
#             # If URL cannot Loading Properly 
#             except:
#                 job_description.append('Description Not Available')
            
#             # Check Description Count Meets User Job Count
#             if description_count == company_count:
#                 break

#         # Filter the Job Description
#         df = df.iloc[:len(job_description), :]

#         # Add Job Description in Dataframe
#         df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
#         df['Job Description'] = df['Job Description'].apply(lambda x: np.nan if x=='Description Not Available' else x)
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)
#         return df

#     def display_data_userinterface(df_final):
#         # Display the Data in User Interface
#         add_vertical_space(1)
#         if len(df_final) > 0:
#             for i in range(0, len(df_final)):
                
#                 st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
#                 st.write(f"Company Name : {df_final.iloc[i,0]}")
#                 st.write(f"Job Title    : {df_final.iloc[i,1]}")
#                 st.write(f"Location     : {df_final.iloc[i,2]}")
#                 st.write(f"Website URL  : {df_final.iloc[i,3]}")

#                 with st.expander(label='Job Desription'):
#                     st.write(df_final.iloc[i, 4])
#                 add_vertical_space(3)
        
#         else:
#             st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
#                                 unsafe_allow_html=True)

#     def job_title_filter(scrap_job_title, user_job_title_input):
#         # User Job Title Convert into Lower Case
#         user_input = [i.lower().strip() for i in user_job_title_input]

#         # scraped Job Title Convert into Lower Case
#         scrap_title = [i.lower().strip() for i in [scrap_job_title]]

#         # Verify Any User Job Title in the scraped Job Title
#         confirmation_count = 0
#         for i in user_input:
#             if all(j in scrap_title[0] for j in i.split()):
#                 confirmation_count += 1

#         # Return Job Title if confirmation_count greater than 0 else return NaN
#         if confirmation_count > 0:
#             return scrap_job_title
#         else:
#             return np.nan

#     def main():
#         # Initially set driver to None
#         driver = None
        
#         try:
#             job_title_input, job_location, company_count, submit = linkedin_scraper.get_userinput()
#             add_vertical_space(2)
            
#             if submit:
#                 if job_title_input != [] and job_location != '':
                    
#                     with st.spinner('Chrome Webdriver Setup Initializing...'):
#                         driver = linkedin_scraper.webdriver_setup()
                                       
#                     with st.spinner('Loading More Company Listings...'):
#                         # build URL based on User Job Title Input
#                         link = linkedin_scraper.build_url(job_title_input, job_location)
#                         # Open the Link in LinkedIn and Scroll Down the Page
#                         linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
#                     with st.spinner('Scraping Company Details...'):
#                         # Scraping the Company Name, Location, Job Title and URL Data
#                         df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location)
                    
#                     with st.spinner('Scraping Job Descriptions...'):
#                         # Scraping the Job Descriptin Data
#                         df_final = linkedin_scraper.scrap_job_description(driver, df, company_count)
                    
#                     # Display the Data in User Interface
#                     linkedin_scraper.display_data_userinterface(df_final)
                
#                 # If User Click Submit Button and Job Title is Empty
#                 elif job_title_input == []:
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
#                                 unsafe_allow_html=True)
                
#                 elif job_location == '':
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
#                                 unsafe_allow_html=True)

#         except Exception as e:
#             add_vertical_space(2)
#             st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
#         finally:
#             if driver:
#                 driver.quit()

# # Streamlit Configuration Setup
# streamlit_config()
# add_vertical_space(5)

# # Main function call
# linkedin_scraper.main()
# import time
# import numpy as np
# import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd


# def streamlit_config():
#     # page configuration
#     st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)

#     # title and position
#     st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)

# class linkedin_scraper:

#     def webdriver_setup():
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')

#         driver = webdriver.Chrome(options=options)
#         driver.maximize_window()
#         return driver

#     def get_userinput():
#         add_vertical_space(2)
#         with st.form(key='linkedin_scarp'):
#             add_vertical_space(1)
#             col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
#             with col1:
#                 job_title_input = st.text_input(label='Job Title')
#                 job_title_input = job_title_input.split(',')
#             with col2:
#                 job_location = st.text_input(label='Job Location', value='India')
#             with col3:
#                 company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

#             add_vertical_space(1)
#             skill_input = st.text_input(label='Skills')
#             skill_input = skill_input.split(',')

#             # Submit Button
#             add_vertical_space(1)
#             submit = st.form_submit_button(label='Submit')
#             add_vertical_space(1)
        
#         return job_title_input, job_location, company_count, skill_input, submit

#     def build_url(job_title, job_location):
#         b = []
#         for i in job_title:
#             x = i.split()
#             y = '%20'.join(x)
#             b.append(y)

#         job_title = '%2C%20'.join(b)
#         link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

#         return link
    
#     def open_link(driver, link):
#         while True:
#             # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
#             try:
#                 driver.get(link)
#                 driver.implicitly_wait(5)
#                 time.sleep(3)
#                 driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
#                 return
            
#             # Retry Loading the Page
#             except NoSuchElementException:
#                 continue

#     def link_open_scrolldown(driver, link, company_count):
#         # Open the Link in LinkedIn
#         linkedin_scraper.open_link(driver, link)
#         time.sleep(3)
        
#         # Scraping the Company Data
#         companies_scraped = 0
#         while companies_scraped < company_count:
#             # Scroll Down the Page to load more companies
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Check if there's a "See more" button and click it
#             try:
#                 see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
#                 see_more_button.click()
#                 time.sleep(3)
#             except NoSuchElementException:
#                 break  # No more "See more" button, exit the loop
            
#             # Update the number of scraped companies
#             companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

#         return

#     def scrap_company_data(driver, job_title_input, job_location):
#         # scraping the Company Data
#         company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
#         company_name = [i.text for i in company]

#         location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
#         company_location = [i.text for i in location]

#         title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
#         job_title = [i.text for i in title]

#         url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
#         website_url = [i.get_attribute('href') for i in url]

#         # combine the all data to single dataframe
#         df = pd.DataFrame(company_name, columns=['Company Name'])
#         df['Job Title'] = pd.DataFrame(job_title)
#         df['Location'] = pd.DataFrame(company_location)
#         df['Website URL'] = pd.DataFrame(website_url)

#         # Return Job Title if there are more than 1 matched word else return NaN
#         df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

#         # Return Location if User Job Location in Scraped Location else return NaN
#         df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
#         # Drop Null Values and Reset Index
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)

#         return df 

#     def scrap_job_description(driver, df, company_count, skills):
#         # Get URL into List
#         website_url = df['Website URL'].tolist()
        
#         # Scrap the Job Description
#         job_description, description_count = [], 0
#         for i in range(0, len(website_url)):
#             try:
#                 # Open the Link in LinkedIn
#                 linkedin_scraper.open_link(driver, website_url[i])

#                 # Click on Show More Button
#                 driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
#                 driver.implicitly_wait(5)
#                 time.sleep(1)

#                 # Get Job Description
#                 description = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')
#                 data = [i.text for i in description][0]

#                 if len(data.strip()) > 0:
#                     job_description.append(data)
#                     description_count += 1
#                 else:
#                     job_description.append('Description Not Available')
            
#             # If URL cannot Loading Properly 
#             except:
#                 job_description.append('Description Not Available')
            
#             # Check Description Count Meets User Job Count
#             if description_count == company_count:
#                 break

#         # Filter the Job Description
#         df = df.iloc[:len(job_description), :]

#         # Add Job Description in Dataframe
#         df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
#         df['Job Description'] = df['Job Description'].apply(lambda x: np.nan if x=='Description Not Available' else x)
#         df = df.dropna()

#         # Calculate probability of matching skills
#         df['Match Probability'] = df['Job Description'].apply(lambda desc: sum(skill.lower() in desc.lower() for skill in skills) / len(skills))
#         df.reset_index(drop=True, inplace=True)
#         return df

#     def display_data_userinterface(df_final):
#         # Display the Data in User Interface
#         add_vertical_space(1)
#         if len(df_final) > 0:
#             for i in range(0, len(df_final)):
                
#                 st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
#                 st.write(f"Company Name : {df_final.iloc[i,0]}")
#                 st.write(f"Job Title    : {df_final.iloc[i,1]}")
#                 st.write(f"Location     : {df_final.iloc[i,2]}")
#                 st.write(f"Website URL  : {df_final.iloc[i,3]}")

#                 with st.expander(label='Job Desription'):
#                     st.write(df_final.iloc[i, 4])
                
#                 st.write(f"Match Probability: {df_final.iloc[i, 5]*100:.2f}%")
#                 add_vertical_space(3)
        
#         else:
#             st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
#                                 unsafe_allow_html=True)

#     def job_title_filter(scrap_job_title, user_job_title_input):
#         # User Job Title Convert into Lower Case
#         user_input = [i.lower().strip() for i in user_job_title_input]

#         # scraped Job Title Convert into Lower Case
#         scrap_title = [i.lower().strip() for i in [scrap_job_title]]

#         # Verify Any User Job Title in the scraped Job Title
#         confirmation_count = 0
#         for i in user_input:
#             if all(j in scrap_title[0] for j in i.split()):
#                 confirmation_count += 1

#         # Return Job Title if confirmation_count greater than 0 else return NaN
#         if confirmation_count > 0:
#             return scrap_job_title
#         else:
#             return np.nan

#     def main():
#         # Initially set driver to None
#         driver = None
        
#         try:
#             job_title_input, job_location, company_count, skills, submit = linkedin_scraper.get_userinput()
#             add_vertical_space(2)
            
#             if submit:
#                 if job_title_input != [] and job_location != '':
                    
#                     with st.spinner('Chrome Webdriver Setup Initializing...'):
#                         driver = linkedin_scraper.webdriver_setup()
                                       
#                     with st.spinner('Loading More Company Listings...'):
#                         # build URL based on User Job Title Input
#                         link = linkedin_scraper.build_url(job_title_input, job_location)
#                         # Open the Link in LinkedIn and Scroll Down the Page
#                         linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
#                     with st.spinner('Scraping Company Details...'):
#                         # Scraping the Company Name, Location, Job Title and URL Data
#                         df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location)
                    
#                     with st.spinner('Scraping Job Descriptions...'):
#                         # Scraping the Job Descriptin Data
#                         df_final = linkedin_scraper.scrap_job_description(driver, df, company_count, skills)
                    
#                     # Display the Data in User Interface
#                     linkedin_scraper.display_data_userinterface(df_final)
                
#                 # If User Click Submit Button and Job Title is Empty
#                 elif job_title_input == []:
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
#                                 unsafe_allow_html=True)
                
#                 elif job_location == '':
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
#                                 unsafe_allow_html=True)

#         except Exception as e:
#             add_vertical_space(2)
#             st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
#         finally:
#             if driver:
#                 driver.quit()

# # Streamlit Configuration Setup
# streamlit_config()
# add_vertical_space(5)

# # Main function call
# linkedin_scraper.main()


# ---------------------------------------------------------------------------------------------
# import time
# import numpy as np
# import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd


# def streamlit_config():
#     # page configuration
#     st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)

#     # title and position
#     st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)

# class linkedin_scraper:

#     def webdriver_setup():
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')

#         driver = webdriver.Chrome(options=options)
#         driver.maximize_window()
#         return driver

#     def get_userinput():
#         add_vertical_space(2)
#         with st.form(key='linkedin_scarp'):
#             add_vertical_space(1)
#             col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
#             with col1:
#                 job_title_input = st.text_input(label='Job Title')
#                 job_title_input = job_title_input.split(',')
#             with col2:
#                 job_location = st.text_input(label='Job Location', value='India')
#             with col3:
#                 company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

#             add_vertical_space(1)
#             skill_input = st.text_input(label='Skills')
#             skill_input = skill_input.split(',')

#             # Submit Button
#             add_vertical_space(1)
#             submit = st.form_submit_button(label='Submit')
#             add_vertical_space(1)
        
#         return job_title_input, job_location, company_count, skill_input, submit

#     def build_url(job_title, job_location):
#         b = []
#         for i in job_title:
#             x = i.split()
#             y = '%20'.join(x)
#             b.append(y)

#         job_title = '%2C%20'.join(b)
#         link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

#         return link
    
#     def open_link(driver, link):
#         while True:
#             # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
#             try:
#                 driver.get(link)
#                 driver.implicitly_wait(5)
#                 time.sleep(3)
#                 driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
#                 return
            
#             # Retry Loading the Page
#             except NoSuchElementException:
#                 continue

#     def link_open_scrolldown(driver, link, company_count):
#         # Open the Link in LinkedIn
#         linkedin_scraper.open_link(driver, link)
#         time.sleep(3)
        
#         # Scraping the Company Data
#         companies_scraped = 0
#         while companies_scraped < company_count:
#             # Scroll Down the Page to load more companies
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Check if there's a "See more" button and click it
#             try:
#                 see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
#                 see_more_button.click()
#                 time.sleep(3)
#             except NoSuchElementException:
#                 break  # No more "See more" button, exit the loop
            
#             # Update the number of scraped companies
#             companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

#         return

#     def scrap_company_data(driver, job_title_input, job_location):
#         # scraping the Company Data
#         company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
#         company_name = [i.text for i in company]

#         location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
#         company_location = [i.text for i in location]

#         title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
#         job_title = [i.text for i in title]

#         url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
#         website_url = [i.get_attribute('href') for i in url]

#         # combine the all data to single dataframe
#         df = pd.DataFrame(company_name, columns=['Company Name'])
#         df['Job Title'] = pd.DataFrame(job_title)
#         df['Location'] = pd.DataFrame(company_location)
#         df['Website URL'] = pd.DataFrame(website_url)

#         # Return Job Title if there are more than 1 matched word else return NaN
#         df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

#         # Return Location if User Job Location in Scraped Location else return NaN
#         df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
#         # Drop Null Values and Reset Index
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)

#         return df 

#     def scrap_job_description(driver, df, company_count, skills):
#         # Get URL into List
#         website_url = df['Website URL'].tolist()
        
#         # Scrap the Job Description
#         job_description, description_count = [], 0
#         for i in range(0, len(website_url)):
#             try:
#                 # Open the Link in LinkedIn
#                 linkedin_scraper.open_link(driver, website_url[i])

#                 # Click on Show More Button
#                 driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
#                 driver.implicitly_wait(5)
#                 time.sleep(1)

#                 # Get Job Description
#                 description = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')
#                 data = [i.text for i in description][0]

#                 if len(data.strip()) > 0:
#                     job_description.append(data)
#                     description_count += 1
#                 else:
#                     job_description.append('Description Not Available')
            
#             # If URL cannot Loading Properly 
#             except:
#                 job_description.append('Description Not Available')
            
#             # Check Description Count Meets User Job Count
#             if description_count == company_count:
#                 break

#         # Filter the Job Description
#         df = df.iloc[:len(job_description), :]

#         # Add Job Description in Dataframe
#         df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
#         df['Job Description'] = df['Job Description'].apply(lambda x: np.nan if x=='Description Not Available' else x)
#         df = df.dropna()

#         # Calculate probability of matching skills
#         df['Match Probability'] = df['Job Description'].apply(lambda desc: sum(skill.lower() in desc.lower() for skill in skills) / len(skills) * 100)
#         df.reset_index(drop=True, inplace=True)
#         return df

#     def display_data_userinterface(df_final):
#         # Display the Data in User Interface
#         add_vertical_space(1)
#         if len(df_final) > 0:
#             for i in range(0, len(df_final)):
                
#                 st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
#                 st.write(f"Company Name : {df_final.iloc[i,0]}")
#                 st.write(f"Job Title    : {df_final.iloc[i,1]}")
#                 st.write(f"Location     : {df_final.iloc[i,2]}")
#                 st.write(f"Website URL  : {df_final.iloc[i,3]}")

#                 with st.expander(label='Job Desription'):
#                     st.write(df_final.iloc[i, 4])
                
#                 st.write(f"Match Probability: {df_final.iloc[i, 5]:.2f}%")
#                 add_vertical_space(3)
        
#         else:
#             st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
#                                 unsafe_allow_html=True)

#     def job_title_filter(scrap_job_title, user_job_title_input):
#         # User Job Title Convert into Lower Case
#         user_input = [i.lower().strip() for i in user_job_title_input]

#         # scraped Job Title Convert into Lower Case
#         scrap_title = [i.lower().strip() for i in [scrap_job_title]]

#         # Verify Any User Job Title in the scraped Job Title
#         confirmation_count = 0
#         for i in user_input:
#             if all(j in scrap_title[0] for j in i.split()):
#                 confirmation_count += 1

#         # Return Job Title if confirmation_count greater than 0 else return NaN
#         if confirmation_count > 0:
#             return scrap_job_title
#         else:
#             return np.nan

#     def main():
#         # Initially set driver to None
#         driver = None
        
#         try:
#             job_title_input, job_location, company_count, skills, submit = linkedin_scraper.get_userinput()
#             add_vertical_space(2)
            
#             if submit:
#                 if job_title_input != [] and job_location != '':
                    
#                     with st.spinner('Chrome Webdriver Setup Initializing...'):
#                         driver = linkedin_scraper.webdriver_setup()
                                       
#                     with st.spinner('Loading More Company Listings...'):
#                         # build URL based on User Job Title Input
#                         link = linkedin_scraper.build_url(job_title_input, job_location)
#                         # Open the Link in LinkedIn and Scroll Down the Page
#                         linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
#                     with st.spinner('Scraping Company Details...'):
#                         # Scraping the Company Name, Location, Job Title and URL Data
#                         df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location)
                    
#                     with st.spinner('Scraping Job Descriptions...'):
#                         # Scraping the Job Descriptin Data
#                         df_final = linkedin_scraper.scrap_job_description(driver, df, company_count, skills)
                    
#                     # Display the Data in User Interface
#                     linkedin_scraper.display_data_userinterface(df_final)
                
#                 # If User Click Submit Button and Job Title is Empty
#                 elif job_title_input == []:
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
#                                 unsafe_allow_html=True)
                
#                 elif job_location == '':
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
#                                 unsafe_allow_html=True)

#         except Exception as e:
#             add_vertical_space(2)
#             st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
#         finally:
#             if driver:
#                 driver.quit()

# # Streamlit Configuration Setup
# streamlit_config()
# add_vertical_space(5)

# # Main function call
# linkedin_scraper.main()






# # -----------------------------------------2nd--------------------------


# import time
# import numpy as np
# import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd


# def streamlit_config():
#     # page configuration
#     st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)

#     # title and position
#     st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)
#     st.info('It will be take time keep patience')
# class linkedin_scraper:

#     def webdriver_setup():
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')

#         driver = webdriver.Chrome(options=options)
#         driver.maximize_window()
#         return driver

#     def get_userinput():
#         add_vertical_space(2)
#         with st.form(key='linkedin_scarp'):
#             add_vertical_space(1)
#             col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
#             with col1:
#                 job_title_input = st.text_input(label='Job Title')
#                 job_title_input = job_title_input.split(',')
#             with col2:
#                 job_location = st.text_input(label='Job Location', value='India')
#             with col3:
#                 company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

#             add_vertical_space(1)
#             skill_input = st.text_input(label='Skills')
#             skill_input = skill_input.split(',')

#             # Submit Button
#             add_vertical_space(1)
#             submit = st.form_submit_button(label='Submit')
#             add_vertical_space(1)
        
#         return job_title_input, job_location, company_count, skill_input, submit

#     def build_url(job_title, job_location):
#         b = []
#         for i in job_title:
#             x = i.split()
#             y = '%20'.join(x)
#             b.append(y)

#         job_title = '%2C%20'.join(b)
#         link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

#         return link
    
#     def open_link(driver, link):
#         while True:
#             # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
#             try:
#                 driver.get(link)
#                 driver.implicitly_wait(5)
#                 time.sleep(3)
#                 driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
#                 return
            
#             # Retry Loading the Page
#             except NoSuchElementException:
#                 continue

#     def link_open_scrolldown(driver, link, company_count):
#         # Open the Link in LinkedIn
#         linkedin_scraper.open_link(driver, link)
#         time.sleep(3)
        
#         # Scraping the Company Data
#         companies_scraped = 0
#         while companies_scraped < company_count:
#             # Scroll Down the Page to load more companies
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Check if there's a "See more" button and click it
#             try:
#                 see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
#                 see_more_button.click()
#                 time.sleep(3)
#             except NoSuchElementException:
#                 break  # No more "See more" button, exit the loop
            
#             # Update the number of scraped companies
#             companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

#         return

#     def scrap_company_data(driver, job_title_input, job_location):
#         # scraping the Company Data
#         company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
#         company_name = [i.text for i in company]

#         location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
#         company_location = [i.text for i in location]

#         title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
#         job_title = [i.text for i in title]

#         url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
#         website_url = [i.get_attribute('href') for i in url]

#         # combine the all data to single dataframe
#         df = pd.DataFrame(company_name, columns=['Company Name'])
#         df['Job Title'] = pd.DataFrame(job_title)
#         df['Location'] = pd.DataFrame(company_location)
#         df['Website URL'] = pd.DataFrame(website_url)

#         # Return Job Title if there are more than 1 matched word else return NaN
#         df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

#         # Return Location if User Job Location in Scraped Location else return NaN
#         df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
#         # Drop Null Values and Reset Index
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)

#         return df 

#     def scrap_job_description(driver, df, skills):
#         # Get URL into List
#         website_url = df['Website URL'].tolist()
        
#         # Scrap the Job Description
#         job_description, match_probabilities = [], []
#         for url in website_url:
#             try:
#                 # Open the Link in LinkedIn
#                 linkedin_scraper.open_link(driver, url)

#                 # Click on Show More Button
#                 driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
#                 driver.implicitly_wait(5)
#                 time.sleep(1)

#                 # Get Job Description
#                 description = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')
#                 desc_text = [i.text for i in description][0]

#                 if len(desc_text.strip()) > 0:
#                     job_description.append(desc_text)
#                 else:
#                     job_description.append('Description Not Available')

#                 # Calculate probability of matching skills
#                 match_probability = sum(skill.lower() in desc_text.lower() for skill in skills) / max(len(skills), 1) * 100
#                 match_probabilities.append(match_probability)
            
#             # If URL cannot Loading Properly 
#             except:
#                 job_description.append('Description Not Available')
#                 match_probabilities.append(0)

#         # Add Job Description and Match Probability in Dataframe
#         df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
#         df['Match Probability'] = pd.DataFrame(match_probabilities, columns=['Probability'])
#         df['Match Probability'] = df['Match Probability'].astype(float)
        
#         df = df[df['Job Description'] != 'Description Not Available']
#         df.reset_index(drop=True, inplace=True)

#         return df

#     def display_data_userinterface(df_final):
#         # Display the Data in User Interface
#         add_vertical_space(1)
#         if len(df_final) > 0:
#             for i in range(0, len(df_final)):
                
#                 st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
#                 st.write(f"Company Name : {df_final.iloc[i,0]}")
#                 st.write(f"Job Title    : {df_final.iloc[i,1]}")
#                 st.write(f"Location     : {df_final.iloc[i,2]}")
#                 st.write(f"Website URL  : {df_final.iloc[i,3]}")

#                 with st.expander(label='Job Desription'):
#                     st.write(df_final.iloc[i, 4])
                
#                 st.write(f"Match Probability: {df_final.iloc[i, 5]:.2f}%")
#                 add_vertical_space(3)
        
#         else:
#             st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
#                                 unsafe_allow_html=True)

#     def job_title_filter(scrap_job_title, user_job_title_input):
#         # User Job Title Convert into Lower Case
#         user_input = [i.lower().strip() for i in user_job_title_input]

#         # scraped Job Title Convert into Lower Case
#         scrap_title = [i.lower().strip() for i in [scrap_job_title]]

#         # Verify Any User Job Title in the scraped Job Title
#         confirmation_count = 0
#         for i in user_input:
#             if all(j in scrap_title[0] for j in i.split()):
#                 confirmation_count += 1

#         # Return Job Title if confirmation_count greater than 0 else return NaN
#         if confirmation_count > 0:
#             return scrap_job_title
#         else:
#             return np.nan

#     def main():
#         # Initially set driver to None
#         driver = None
        
#         try:
#             job_title_input, job_location, company_count, skills, submit = linkedin_scraper.get_userinput()
#             add_vertical_space(2)
            
#             if submit:
#                 if job_title_input != [] and job_location != '':
                    
#                     with st.spinner('Chrome Webdriver Setup Initializing...'):
#                         driver = linkedin_scraper.webdriver_setup()
                                       
#                     with st.spinner('Loading More Company Listings...'):
#                         # build URL based on User Job Title Input
#                         link = linkedin_scraper.build_url(job_title_input, job_location)
#                         # Open the Link in LinkedIn and Scroll Down the Page
#                         linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
#                     with st.spinner('Scraping Company Details...'):
#                         # Scraping the Company Name, Location, Job Title and URL Data
#                         df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location)
                    
#                     with st.spinner('Scraping Job Descriptions...'):
#                         # Scraping the Job Descriptin Data
#                         df_final = linkedin_scraper.scrap_job_description(driver, df, skills)
                    
#                     # Display the Data in User Interface
#                     linkedin_scraper.display_data_userinterface(df_final)
                
#                 # If User Click Submit Button and Job Title is Empty
#                 elif job_title_input == []:
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
#                                 unsafe_allow_html=True)
                
#                 elif job_location == '':
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
#                                 unsafe_allow_html=True)

#         except Exception as e:
#             add_vertical_space(2)
#             st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
#         finally:
#             if driver:
#                 driver.quit()

# # Streamlit Configuration Setup
# streamlit_config()
# add_vertical_space(5)

# # Main function call
# linkedin_scraper.main()


















































# import time
# import numpy as np
# import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd


# def streamlit_config():
#     # page configuration
#     st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)

#     # title and position
#     st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)
#     st.info('It will be take time keep patience')


# class linkedin_scraper:

#     def webdriver_setup():
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')

#         driver = webdriver.Chrome(options=options)
#         driver.maximize_window()
#         return driver

#     def get_userinput():
#         add_vertical_space(2)
#         with st.form(key='linkedin_scarp'):
#             add_vertical_space(1)
#             col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
#             with col1:
#                 job_title_input = st.text_input(label='Job Title')
#                 job_title_input = job_title_input.split(',')
#             with col2:
#                 job_location = st.text_input(label='Job Location', value='India')
#             with col3:
#                 company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

#             add_vertical_space(1)
#             skill_input = st.text_input(label='Skills')
#             skill_input = skill_input.split(',')

#             # Submit Button
#             add_vertical_space(1)
#             submit = st.form_submit_button(label='Submit')
#             add_vertical_space(1)
        
#         return job_title_input, job_location, company_count, skill_input, submit

#     def build_url(job_title, job_location):
#         b = []
#         for i in job_title:
#             x = i.split()
#             y = '%20'.join(x)
#             b.append(y)

#         job_title = '%2C%20'.join(b)
#         link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

#         return link
    
#     def open_link(driver, link):
#         while True:
#             # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
#             try:
#                 driver.get(link)
#                 driver.implicitly_wait(5)
#                 time.sleep(3)
#                 driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
#                 return
            
#             # Retry Loading the Page
#             except NoSuchElementException:
#                 continue

#     def link_open_scrolldown(driver, link, company_count):
#         # Open the Link in LinkedIn
#         linkedin_scraper.open_link(driver, link)
#         time.sleep(3)
        
#         # Scraping the Company Data
#         companies_scraped = 0
#         while companies_scraped < company_count:
#             # Scroll Down the Page to load more companies
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Check if there's a "See more" button and click it
#             try:
#                 see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
#                 see_more_button.click()
#                 time.sleep(3)
#             except NoSuchElementException:
#                 break  # No more "See more" button, exit the loop
            
#             # Update the number of scraped companies
#             companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

#         return

#     def scrap_company_data(driver, job_title_input, job_location, company_count):
#         # scraping the Company Data
#         company = driver.find_elements(by=By.CSS_SELECTOR, value='h4.base-search-card__subtitle')
#         company_name = [i.text for i in company]

#         location = driver.find_elements(by=By.CSS_SELECTOR, value='span.job-search-card__location')
#         company_location = [i.text for i in location]

#         title = driver.find_elements(by=By.CSS_SELECTOR, value='h3.base-search-card__title')
#         job_title = [i.text for i in title]

#         url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
#         website_url = [i.get_attribute('href') for i in url]

#         # combine the all data to single dataframe
#         df = pd.DataFrame({'Company Name': company_name[:company_count], 
#                            'Job Title': job_title[:company_count], 
#                            'Location': company_location[:company_count], 
#                            'Website URL': website_url[:company_count]})

#         # Return Job Title if there are more than 1 matched word else return NaN
#         df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

#         # Return Location if User Job Location in Scraped Location else return NaN
#         df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
#         # Drop Null Values and Reset Index
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)

#         return df 

#     def scrap_job_description(driver, df, skills):
#         # Get URL into List
#         website_url = df['Website URL'].tolist()
        
#         # Scrap the Job Description
#         job_description, match_probabilities = [], []
#         for url in website_url:
#             try:
#                 # Open the Link in LinkedIn
#                 linkedin_scraper.open_link(driver, url)

#                 # Click on Show More Button
#                 driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
#                 driver.implicitly_wait(5)
#                 time.sleep(1)

#                 # Get Job Description
#                 description = driver.find_elements(by=By.CSS_SELECTOR, value='div.show-more-less-html__markup')
#                 desc_text = [i.text for i in description][0]

#                 if len(desc_text.strip()) > 0:
#                     job_description.append(desc_text)
#                 else:
#                     job_description.append('Description Not Available')

#                 # Calculate probability of matching skills
#                 match_probability = sum(skill.lower() in desc_text.lower() for skill in skills) / max(len(skills), 1) * 100
#                 match_probabilities.append(match_probability)
            
#             # If URL cannot Loading Properly 
#             except:
#                 job_description.append('Description Not Available')
#                 match_probabilities.append(0)

#         # Add Job Description and Match Probability in Dataframe
#         df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
#         df['Match Probability'] = pd.DataFrame(match_probabilities, columns=['Probability'])
#         df['Match Probability'] = df['Match Probability'].astype(float)
        
#         df = df[df['Job Description'] != 'Description Not Available']
#         df.reset_index(drop=True, inplace=True)

#         return df

#     def display_data_userinterface(df_final):
#         # Display the Data in User Interface
#         add_vertical_space(1)
#         if len(df_final) > 0:
#             for i in range(0, len(df_final)):
                
#                 st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
#                 st.write(f"Company Name : {df_final.iloc[i,0]}")
#                 st.write(f"Job Title    : {df_final.iloc[i,1]}")
#                 st.write(f"Location     : {df_final.iloc[i,2]}")
#                 st.write(f"Website URL  : {df_final.iloc[i,3]}")

#                 with st.expander(label='Job Desription'):
#                     st.write(df_final.iloc[i, 4])
                
#                 st.write(f"Match Probability: {df_final.iloc[i, 5]:.2f}%")
#                 add_vertical_space(3)
        
#         else:
#             st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
#                                 unsafe_allow_html=True)

#     def job_title_filter(scrap_job_title, user_job_title_input):
#         # User Job Title Convert into Lower Case
#         user_input = [i.lower().strip() for i in user_job_title_input]

#         # scraped Job Title Convert into Lower Case
#         scrap_title = [i.lower().strip() for i in [scrap_job_title]]

#         # Verify Any User Job Title in the scraped Job Title
#         confirmation_count = 0
#         for i in user_input:
#             if all(j in scrap_title[0] for j in i.split()):
#                 confirmation_count += 1

#         # Return Job Title if confirmation_count greater than 0 else return NaN
#         if confirmation_count > 0:
#             return scrap_job_title
#         else:
#             return np.nan

#     def main():
#         # Initially set driver to None
#         driver = None
        
#         try:
#             job_title_input, job_location, company_count, skills, submit = linkedin_scraper.get_userinput()
#             add_vertical_space(2)
            
#             if submit:
#                 if job_title_input != [] and job_location != '':
                    
#                     with st.spinner('Chrome Webdriver Setup Initializing...'):
#                         driver = linkedin_scraper.webdriver_setup()
                                       
#                     with st.spinner('Loading More Company Listings...'):
#                         # build URL based on User Job Title Input
#                         link = linkedin_scraper.build_url(job_title_input, job_location)
#                         # Open the Link in LinkedIn and Scroll Down the Page
#                         linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
#                     with st.spinner('Scraping Company Details...'):
#                         # Scraping the Company Name, Location, Job Title and URL Data
#                         df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location, company_count)
                    
#                     with st.spinner('Scraping Job Descriptions...'):
#                         # Scraping the Job Description Data
#                         df_final = linkedin_scraper.scrap_job_description(driver, df, skills)
                    
#                     # Display the Data in User Interface
#                     linkedin_scraper.display_data_userinterface(df_final)
                
#                 # If User Click Submit Button and Job Title is Empty
#                 elif job_title_input == []:
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
#                                 unsafe_allow_html=True)
                
#                 elif job_location == '':
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
#                                 unsafe_allow_html=True)

#         except Exception as e:
#             add_vertical_space(2)
#             st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
#         finally:
#             if driver:
#                 driver.quit()

# # Streamlit Configuration Setup
# streamlit_config()
# add_vertical_space(5)

# # Main function call
# linkedin_scraper.main()
















































# import time
# import numpy as np
# import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd


# def streamlit_config():
#     # page configuration
#     st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)

#     # title and position
#     st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)
#     st.info('It will take some time. Please be patient.')


# class linkedin_scraper:

#     def webdriver_setup():
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')

#         driver = webdriver.Chrome(options=options)
#         driver.maximize_window()
#         return driver

#     def get_userinput():
#         add_vertical_space(2)
#         with st.form(key='linkedin_scarp'):
#             add_vertical_space(1)
#             col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
#             with col1:
#                 job_title_input = st.text_input(label='Job Title')
#                 job_title_input = job_title_input.split(',')
#             with col2:
#                 job_location = st.text_input(label='Job Location', value='India')
#             with col3:
#                 company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

#             add_vertical_space(1)
#             skill_input = st.text_input(label='Skills')
#             skills = skill_input.split(',')

#             # Submit Button
#             add_vertical_space(1)
#             submit = st.form_submit_button(label='Submit')
#             add_vertical_space(1)
        
#         return job_title_input, job_location, company_count, skills, submit

#     def build_url(job_title, job_location):
#         b = []
#         for i in job_title:
#             x = i.split()
#             y = '%20'.join(x)
#             b.append(y)

#         job_title = '%2C%20'.join(b)
#         link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

#         return link
    
#     def open_link(driver, link):
#         while True:
#             # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
#             try:
#                 driver.get(link)
#                 driver.implicitly_wait(5)
#                 time.sleep(3)
#                 driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
#                 return
            
#             # Retry Loading the Page
#             except NoSuchElementException:
#                 continue

#     def link_open_scrolldown(driver, link, company_count):
#         # Open the Link in LinkedIn
#         linkedin_scraper.open_link(driver, link)
#         time.sleep(3)
        
#         # Scraping the Company Data
#         companies_scraped = 0
#         while companies_scraped < company_count:
#             # Scroll Down the Page to load more companies
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Check if there's a "See more" button and click it
#             try:
#                 see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
#                 see_more_button.click()
#                 time.sleep(3)
#             except NoSuchElementException:
#                 break  # No more "See more" button, exit the loop
            
#             # Update the number of scraped companies
#             companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

#         return

#     def scrap_company_data(driver, job_title_input, job_location, company_count):
#         # scraping the Company Data
#         company = driver.find_elements(by=By.CSS_SELECTOR, value='h4.base-search-card__subtitle')
#         company_name = [i.text for i in company]

#         location = driver.find_elements(by=By.CSS_SELECTOR, value='span.job-search-card__location')
#         company_location = [i.text for i in location]

#         title = driver.find_elements(by=By.CSS_SELECTOR, value='h3.base-search-card__title')
#         job_title = [i.text for i in title]

#         url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
#         website_url = [i.get_attribute('href') for i in url]

#         # combine the all data to single dataframe
#         df = pd.DataFrame({'Company Name': company_name[:company_count], 
#                            'Job Title': job_title[:company_count], 
#                            'Location': company_location[:company_count], 
#                            'Website URL': website_url[:company_count]})

#         # Return Job Title if there are more than 1 matched word else return NaN
#         df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

#         # Return Location if User Job Location in Scraped Location else return NaN
#         df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
#         # Drop Null Values and Reset Index
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)

#         return df 

#     def scrap_job_description(driver, df, skills):
#         # Get URL into List
#         website_url = df['Website URL'].tolist()
        
#         # Scrap the Job Description
#         job_description, match_probabilities = [], []
#         for url in website_url:
#             try:
#                 # Open the Link in LinkedIn
#                 linkedin_scraper.open_link(driver, url)

#                 # Click on Show More Button
#                 driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
#                 driver.implicitly_wait(5)
#                 time.sleep(1)

#                 # Get Job Description
#                 description = driver.find_elements(by=By.CSS_SELECTOR, value='div.show-more-less-html__markup')
#                 desc_text = [i.text for i in description][0]

#                 if len(desc_text.strip()) > 0:
#                     job_description.append(desc_text)
#                 else:
#                     job_description.append('Description Not Available')

#                 # Calculate probability of matching skills
#                 match_probability = sum(skill.lower() in desc_text.lower() for skill in skills) / len(skills) * 100
#                 match_probabilities.append(match_probability)
            
#             # If URL cannot Loading Properly 
#             except:
#                 job_description.append('Description Not Available')
#                 match_probabilities.append(0)

#         # Add Job Description and Match Probability in Dataframe
#         df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
#         df['Match Probability'] = pd.DataFrame(match_probabilities, columns=['Probability'])
#         df['Match Probability'] = df['Match Probability'].astype(float)
        
#         df = df[df['Job Description'] != 'Description Not Available']
#         df.reset_index(drop=True, inplace=True)

#         return df

#     def display_data_userinterface(df_final):
#         # Display the Data in User Interface
#         add_vertical_space(1)
#         if len(df_final) > 0:
#             for i in range(0, len(df_final)):
                
#                 st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
#                 st.write(f"Company Name : {df_final.iloc[i,0]}")
#                 st.write(f"Job Title    : {df_final.iloc[i,1]}")
#                 st.write(f"Location     : {df_final.iloc[i,2]}")
#                 st.write(f"Website URL  : {df_final.iloc[i,3]}")

#                 with st.expander(label='Job Description'):
#                     st.write(df_final.iloc[i, 4])
                
#                 st.write(f"Match Probability: {df_final.iloc[i, 5]:.2f}%")
#                 add_vertical_space(3)
        
#         else:
#             st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
#                                 unsafe_allow_html=True)

#     def job_title_filter(scrap_job_title, user_job_title_input):
#         # User Job Title Convert into Lower Case
#         user_input = [i.lower().strip() for i in user_job_title_input]

#         # scraped Job Title Convert into Lower Case
#         scrap_title = [i.lower().strip() for i in [scrap_job_title]]

#         # Verify Any User Job Title in the scraped Job Title
#         confirmation_count = 0
#         for i in user_input:
#             if all(j in scrap_title[0] for j in i.split()):
#                 confirmation_count += 1

#         # Return Job Title if confirmation_count greater than 0 else return NaN
#         if confirmation_count > 0:
#             return scrap_job_title
#         else:
#             return np.nan

#     def main():
#         # Initially set driver to None
#         driver = None
        
#         try:
#             job_title_input, job_location, company_count, skills, submit = linkedin_scraper.get_userinput()
#             add_vertical_space(2)
            
#             if submit:
#                 if job_title_input != [] and job_location != '':
                    
#                     with st.spinner('Chrome Webdriver Setup Initializing...'):
#                         driver = linkedin_scraper.webdriver_setup()
                                       
#                     with st.spinner('Loading More Company Listings...'):
#                         # build URL based on User Job Title Input
#                         link = linkedin_scraper.build_url(job_title_input, job_location)
#                         # Open the Link in LinkedIn and Scroll Down the Page
#                         linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
#                     with st.spinner('Scraping Company Details...'):
#                         # Scraping the Company Name, Location, Job Title and URL Data
#                         df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location, company_count)
                    
#                     with st.spinner('Scraping Job Descriptions...'):
#                         # Scraping the Job Description Data
#                         df_final = linkedin_scraper.scrap_job_description(driver, df, skills)
                    
#                     # Display the Data in User Interface
#                     linkedin_scraper.display_data_userinterface(df_final)
                
#                 # If User Click Submit Button and Job Title is Empty
#                 elif job_title_input == []:
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
#                                 unsafe_allow_html=True)
                
#                 elif job_location == '':
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
#                                 unsafe_allow_html=True)

#         except Exception as e:
#             add_vertical_space(2)
#             st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
#         finally:
#             if driver:
#                 driver.quit()

# # Streamlit Configuration Setup
# streamlit_config()
# add_vertical_space(5)

# # Main function call
# linkedin_scraper.main()





























































































# import time
# import numpy as np
# import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd


# def streamlit_config():
#     # page configuration
#     st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)

#     # title and position
#     st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)

# class linkedin_scraper:

#     def webdriver_setup():
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')

#         driver = webdriver.Chrome(options=options)
#         driver.maximize_window()
#         return driver

#     def get_userinput():
#         add_vertical_space(2)
#         with st.form(key='linkedin_scarp'):
#             add_vertical_space(1)
#             col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
#             with col1:
#                 job_title_input = st.text_input(label='Job Title')
#                 job_title_input = job_title_input.split(',')
#             with col2:
#                 job_location = st.text_input(label='Job Location', value='India')
#             with col3:
#                 company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

#             # Submit Button
#             add_vertical_space(1)
#             submit = st.form_submit_button(label='Submit')
#             add_vertical_space(1)
        
#         return job_title_input, job_location, company_count, submit

#     def build_url(job_title, job_location):
#         b = []
#         for i in job_title:
#             x = i.split()
#             y = '%20'.join(x)
#             b.append(y)

#         job_title = '%2C%20'.join(b)
#         link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

#         return link
    
#     def open_link(driver, link):
#         while True:
#             # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
#             try:
#                 driver.get(link)
#                 driver.implicitly_wait(5)
#                 time.sleep(3)
#                 driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
#                 return
            
#             # Retry Loading the Page
#             except NoSuchElementException:
#                 continue

#     def link_open_scrolldown(driver, link, company_count):
#         # Open the Link in LinkedIn
#         linkedin_scraper.open_link(driver, link)
#         time.sleep(3)
        
#         # Scraping the Company Data
#         companies_scraped = 0
#         while companies_scraped < company_count:
#             # Scroll Down the Page to load more companies
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Check if there's a "See more" button and click it
#             try:
#                 see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
#                 see_more_button.click()
#                 time.sleep(3)
#             except NoSuchElementException:
#                 break  # No more "See more" button, exit the loop
            
#             # Update the number of scraped companies
#             companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

#         return

#     def scrap_company_data(driver, job_title_input, job_location):
#         # scraping the Company Data
#         company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
#         company_name = [i.text for i in company]

#         location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
#         company_location = [i.text for i in location]

#         title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
#         job_title = [i.text for i in title]

#         url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
#         website_url = [i.get_attribute('href') for i in url]

#         # combine the all data to single dataframe
#         df = pd.DataFrame(company_name, columns=['Company Name'])
#         df['Job Title'] = pd.DataFrame(job_title)
#         df['Location'] = pd.DataFrame(company_location)
#         df['Website URL'] = pd.DataFrame(website_url)

#         # Return Job Title if there are more than 1 matched word else return NaN
#         df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

#         # Return Location if User Job Location in Scraped Location else return NaN
#         df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
#         # Drop Null Values and Reset Index
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)

#         return df 

#     def scrap_job_description(driver, df, company_count):
#         # Get URL into List
#         website_url = df['Website URL'].tolist()
        
#         # Scrap the Job Description
#         job_description, description_count = [], 0
#         for i in range(0, len(website_url)):
#             try:
#                 # Open the Link in LinkedIn
#                 linkedin_scraper.open_link(driver, website_url[i])

#                 # Click on Show More Button
#                 driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
#                 driver.implicitly_wait(5)
#                 time.sleep(1)

#                 # Get Job Description
#                 description = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')
#                 data = [i.text for i in description][0]

#                 if len(data.strip()) > 0:
#                     job_description.append(data)
#                     description_count += 1
#                 else:
#                     job_description.append('Description Not Available')
            
#             # If URL cannot Loading Properly 
#             except:
#                 job_description.append('Description Not Available')
            
#             # Check Description Count Meets User Job Count
#             if description_count == company_count:
#                 break

#         # Filter the Job Description
#         df = df.iloc[:len(job_description), :]

#         # Add Job Description in Dataframe
#         df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
#         df['Job Description'] = df['Job Description'].apply(lambda x: np.nan if x=='Description Not Available' else x)
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)
#         return df

#     def display_data_userinterface(df_final):
#         # Display the Data in User Interface
#         add_vertical_space(1)
#         if len(df_final) > 0:
#             for i in range(0, len(df_final)):
                
#                 st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
#                 st.write(f"Company Name : {df_final.iloc[i,0]}")
#                 st.write(f"Job Title    : {df_final.iloc[i,1]}")
#                 st.write(f"Location     : {df_final.iloc[i,2]}")
#                 st.write(f"Website URL  : {df_final.iloc[i,3]}")

#                 with st.expander(label='Job Desription'):
#                     st.write(df_final.iloc[i, 4])
#                 add_vertical_space(3)
        
#         else:
#             st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
#                                 unsafe_allow_html=True)

#     def job_title_filter(scrap_job_title, user_job_title_input):
#         # User Job Title Convert into Lower Case
#         user_input = [i.lower().strip() for i in user_job_title_input]

#         # scraped Job Title Convert into Lower Case
#         scrap_title = [i.lower().strip() for i in [scrap_job_title]]

#         # Verify Any User Job Title in the scraped Job Title
#         confirmation_count = 0
#         for i in user_input:
#             if all(j in scrap_title[0] for j in i.split()):
#                 confirmation_count += 1

#         # Return Job Title if confirmation_count greater than 0 else return NaN
#         if confirmation_count > 0:
#             return scrap_job_title
#         else:
#             return np.nan

#     def main():
#         # Initially set driver to None
#         driver = None
        
#         try:
#             job_title_input, job_location, company_count, submit = linkedin_scraper.get_userinput()
#             add_vertical_space(2)
            
#             if submit:
#                 if job_title_input != [] and job_location != '':
                    
#                     with st.spinner('Chrome Webdriver Setup Initializing...'):
#                         driver = linkedin_scraper.webdriver_setup()
                                       
#                     with st.spinner('Loading More Company Listings...'):
#                         # build URL based on User Job Title Input
#                         link = linkedin_scraper.build_url(job_title_input, job_location)
#                         # Open the Link in LinkedIn and Scroll Down the Page
#                         linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
#                     with st.spinner('Scraping Company Details...'):
#                         # Scraping the Company Name, Location, Job Title and URL Data
#                         df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location)
                    
#                     with st.spinner('Scraping Job Descriptions...'):
#                         # Scraping the Job Descriptin Data
#                         df_final = linkedin_scraper.scrap_job_description(driver, df, company_count)
                    
#                     # Display the Data in User Interface
#                     linkedin_scraper.display_data_userinterface(df_final)
                
#                 # If User Click Submit Button and Job Title is Empty
#                 elif job_title_input == []:
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
#                                 unsafe_allow_html=True)
                
#                 elif job_location == '':
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
#                                 unsafe_allow_html=True)

#         except Exception as e:
#             add_vertical_space(2)
#             st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
#         finally:
#             if driver:
#                 driver.quit()

# # Streamlit Configuration Setup
# streamlit_config()
# add_vertical_space(5)

# # Main function call
# linkedin_scraper.main()
# import time
# import numpy as np
# import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd


# def streamlit_config():
#     # page configuration
#     st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)

#     # title and position
#     st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)

# class linkedin_scraper:

#     def webdriver_setup():
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')

#         driver = webdriver.Chrome(options=options)
#         driver.maximize_window()
#         return driver

#     def get_userinput():
#         add_vertical_space(2)
#         with st.form(key='linkedin_scarp'):
#             add_vertical_space(1)
#             col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
#             with col1:
#                 job_title_input = st.text_input(label='Job Title')
#                 job_title_input = job_title_input.split(',')
#             with col2:
#                 job_location = st.text_input(label='Job Location', value='India')
#             with col3:
#                 company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

#             add_vertical_space(1)
#             skill_input = st.text_input(label='Skills')
#             skill_input = skill_input.split(',')

#             # Submit Button
#             add_vertical_space(1)
#             submit = st.form_submit_button(label='Submit')
#             add_vertical_space(1)
        
#         return job_title_input, job_location, company_count, skill_input, submit

#     def build_url(job_title, job_location):
#         b = []
#         for i in job_title:
#             x = i.split()
#             y = '%20'.join(x)
#             b.append(y)

#         job_title = '%2C%20'.join(b)
#         link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

#         return link
    
#     def open_link(driver, link):
#         while True:
#             # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
#             try:
#                 driver.get(link)
#                 driver.implicitly_wait(5)
#                 time.sleep(3)
#                 driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
#                 return
            
#             # Retry Loading the Page
#             except NoSuchElementException:
#                 continue

#     def link_open_scrolldown(driver, link, company_count):
#         # Open the Link in LinkedIn
#         linkedin_scraper.open_link(driver, link)
#         time.sleep(3)
        
#         # Scraping the Company Data
#         companies_scraped = 0
#         while companies_scraped < company_count:
#             # Scroll Down the Page to load more companies
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Check if there's a "See more" button and click it
#             try:
#                 see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
#                 see_more_button.click()
#                 time.sleep(3)
#             except NoSuchElementException:
#                 break  # No more "See more" button, exit the loop
            
#             # Update the number of scraped companies
#             companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

#         return

#     def scrap_company_data(driver, job_title_input, job_location):
#         # scraping the Company Data
#         company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
#         company_name = [i.text for i in company]

#         location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
#         company_location = [i.text for i in location]

#         title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
#         job_title = [i.text for i in title]

#         url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
#         website_url = [i.get_attribute('href') for i in url]

#         # combine the all data to single dataframe
#         df = pd.DataFrame(company_name, columns=['Company Name'])
#         df['Job Title'] = pd.DataFrame(job_title)
#         df['Location'] = pd.DataFrame(company_location)
#         df['Website URL'] = pd.DataFrame(website_url)

#         # Return Job Title if there are more than 1 matched word else return NaN
#         df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

#         # Return Location if User Job Location in Scraped Location else return NaN
#         df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
#         # Drop Null Values and Reset Index
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)

#         return df 

#     def scrap_job_description(driver, df, company_count, skills):
#         # Get URL into List
#         website_url = df['Website URL'].tolist()
        
#         # Scrap the Job Description
#         job_description, description_count = [], 0
#         for i in range(0, len(website_url)):
#             try:
#                 # Open the Link in LinkedIn
#                 linkedin_scraper.open_link(driver, website_url[i])

#                 # Click on Show More Button
#                 driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
#                 driver.implicitly_wait(5)
#                 time.sleep(1)

#                 # Get Job Description
#                 description = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')
#                 data = [i.text for i in description][0]

#                 if len(data.strip()) > 0:
#                     job_description.append(data)
#                     description_count += 1
#                 else:
#                     job_description.append('Description Not Available')
            
#             # If URL cannot Loading Properly 
#             except:
#                 job_description.append('Description Not Available')
            
#             # Check Description Count Meets User Job Count
#             if description_count == company_count:
#                 break

#         # Filter the Job Description
#         df = df.iloc[:len(job_description), :]

#         # Add Job Description in Dataframe
#         df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
#         df['Job Description'] = df['Job Description'].apply(lambda x: np.nan if x=='Description Not Available' else x)
#         df = df.dropna()

#         # Calculate probability of matching skills
#         df['Match Probability'] = df['Job Description'].apply(lambda desc: sum(skill.lower() in desc.lower() for skill in skills) / len(skills))
#         df.reset_index(drop=True, inplace=True)
#         return df

#     def display_data_userinterface(df_final):
#         # Display the Data in User Interface
#         add_vertical_space(1)
#         if len(df_final) > 0:
#             for i in range(0, len(df_final)):
                
#                 st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
#                 st.write(f"Company Name : {df_final.iloc[i,0]}")
#                 st.write(f"Job Title    : {df_final.iloc[i,1]}")
#                 st.write(f"Location     : {df_final.iloc[i,2]}")
#                 st.write(f"Website URL  : {df_final.iloc[i,3]}")

#                 with st.expander(label='Job Desription'):
#                     st.write(df_final.iloc[i, 4])
                
#                 st.write(f"Match Probability: {df_final.iloc[i, 5]*100:.2f}%")
#                 add_vertical_space(3)
        
#         else:
#             st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
#                                 unsafe_allow_html=True)

#     def job_title_filter(scrap_job_title, user_job_title_input):
#         # User Job Title Convert into Lower Case
#         user_input = [i.lower().strip() for i in user_job_title_input]

#         # scraped Job Title Convert into Lower Case
#         scrap_title = [i.lower().strip() for i in [scrap_job_title]]

#         # Verify Any User Job Title in the scraped Job Title
#         confirmation_count = 0
#         for i in user_input:
#             if all(j in scrap_title[0] for j in i.split()):
#                 confirmation_count += 1

#         # Return Job Title if confirmation_count greater than 0 else return NaN
#         if confirmation_count > 0:
#             return scrap_job_title
#         else:
#             return np.nan

#     def main():
#         # Initially set driver to None
#         driver = None
        
#         try:
#             job_title_input, job_location, company_count, skills, submit = linkedin_scraper.get_userinput()
#             add_vertical_space(2)
            
#             if submit:
#                 if job_title_input != [] and job_location != '':
                    
#                     with st.spinner('Chrome Webdriver Setup Initializing...'):
#                         driver = linkedin_scraper.webdriver_setup()
                                       
#                     with st.spinner('Loading More Company Listings...'):
#                         # build URL based on User Job Title Input
#                         link = linkedin_scraper.build_url(job_title_input, job_location)
#                         # Open the Link in LinkedIn and Scroll Down the Page
#                         linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
#                     with st.spinner('Scraping Company Details...'):
#                         # Scraping the Company Name, Location, Job Title and URL Data
#                         df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location)
                    
#                     with st.spinner('Scraping Job Descriptions...'):
#                         # Scraping the Job Descriptin Data
#                         df_final = linkedin_scraper.scrap_job_description(driver, df, company_count, skills)
                    
#                     # Display the Data in User Interface
#                     linkedin_scraper.display_data_userinterface(df_final)
                
#                 # If User Click Submit Button and Job Title is Empty
#                 elif job_title_input == []:
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
#                                 unsafe_allow_html=True)
                
#                 elif job_location == '':
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
#                                 unsafe_allow_html=True)

#         except Exception as e:
#             add_vertical_space(2)
#             st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
#         finally:
#             if driver:
#                 driver.quit()

# # Streamlit Configuration Setup
# streamlit_config()
# add_vertical_space(5)

# # Main function call
# linkedin_scraper.main()


# ---------------------------------------------------------------------------------------------
# import time
# import numpy as np
# import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd


# def streamlit_config():
#     # page configuration
#     st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)

#     # title and position
#     st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)

# class linkedin_scraper:

#     def webdriver_setup():
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')

#         driver = webdriver.Chrome(options=options)
#         driver.maximize_window()
#         return driver

#     def get_userinput():
#         add_vertical_space(2)
#         with st.form(key='linkedin_scarp'):
#             add_vertical_space(1)
#             col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
#             with col1:
#                 job_title_input = st.text_input(label='Job Title')
#                 job_title_input = job_title_input.split(',')
#             with col2:
#                 job_location = st.text_input(label='Job Location', value='India')
#             with col3:
#                 company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

#             add_vertical_space(1)
#             skill_input = st.text_input(label='Skills')
#             skill_input = skill_input.split(',')

#             # Submit Button
#             add_vertical_space(1)
#             submit = st.form_submit_button(label='Submit')
#             add_vertical_space(1)
        
#         return job_title_input, job_location, company_count, skill_input, submit

#     def build_url(job_title, job_location):
#         b = []
#         for i in job_title:
#             x = i.split()
#             y = '%20'.join(x)
#             b.append(y)

#         job_title = '%2C%20'.join(b)
#         link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

#         return link
    
#     def open_link(driver, link):
#         while True:
#             # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
#             try:
#                 driver.get(link)
#                 driver.implicitly_wait(5)
#                 time.sleep(3)
#                 driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
#                 return
            
#             # Retry Loading the Page
#             except NoSuchElementException:
#                 continue

#     def link_open_scrolldown(driver, link, company_count):
#         # Open the Link in LinkedIn
#         linkedin_scraper.open_link(driver, link)
#         time.sleep(3)
        
#         # Scraping the Company Data
#         companies_scraped = 0
#         while companies_scraped < company_count:
#             # Scroll Down the Page to load more companies
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Check if there's a "See more" button and click it
#             try:
#                 see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
#                 see_more_button.click()
#                 time.sleep(3)
#             except NoSuchElementException:
#                 break  # No more "See more" button, exit the loop
            
#             # Update the number of scraped companies
#             companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

#         return

#     def scrap_company_data(driver, job_title_input, job_location):
#         # scraping the Company Data
#         company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
#         company_name = [i.text for i in company]

#         location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
#         company_location = [i.text for i in location]

#         title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
#         job_title = [i.text for i in title]

#         url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
#         website_url = [i.get_attribute('href') for i in url]

#         # combine the all data to single dataframe
#         df = pd.DataFrame(company_name, columns=['Company Name'])
#         df['Job Title'] = pd.DataFrame(job_title)
#         df['Location'] = pd.DataFrame(company_location)
#         df['Website URL'] = pd.DataFrame(website_url)

#         # Return Job Title if there are more than 1 matched word else return NaN
#         df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

#         # Return Location if User Job Location in Scraped Location else return NaN
#         df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
#         # Drop Null Values and Reset Index
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)

#         return df 

#     def scrap_job_description(driver, df, company_count, skills):
#         # Get URL into List
#         website_url = df['Website URL'].tolist()
        
#         # Scrap the Job Description
#         job_description, description_count = [], 0
#         for i in range(0, len(website_url)):
#             try:
#                 # Open the Link in LinkedIn
#                 linkedin_scraper.open_link(driver, website_url[i])

#                 # Click on Show More Button
#                 driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
#                 driver.implicitly_wait(5)
#                 time.sleep(1)

#                 # Get Job Description
#                 description = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')
#                 data = [i.text for i in description][0]

#                 if len(data.strip()) > 0:
#                     job_description.append(data)
#                     description_count += 1
#                 else:
#                     job_description.append('Description Not Available')
            
#             # If URL cannot Loading Properly 
#             except:
#                 job_description.append('Description Not Available')
            
#             # Check Description Count Meets User Job Count
#             if description_count == company_count:
#                 break

#         # Filter the Job Description
#         df = df.iloc[:len(job_description), :]

#         # Add Job Description in Dataframe
#         df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
#         df['Job Description'] = df['Job Description'].apply(lambda x: np.nan if x=='Description Not Available' else x)
#         df = df.dropna()

#         # Calculate probability of matching skills
#         df['Match Probability'] = df['Job Description'].apply(lambda desc: sum(skill.lower() in desc.lower() for skill in skills) / len(skills) * 100)
#         df.reset_index(drop=True, inplace=True)
#         return df

#     def display_data_userinterface(df_final):
#         # Display the Data in User Interface
#         add_vertical_space(1)
#         if len(df_final) > 0:
#             for i in range(0, len(df_final)):
                
#                 st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
#                 st.write(f"Company Name : {df_final.iloc[i,0]}")
#                 st.write(f"Job Title    : {df_final.iloc[i,1]}")
#                 st.write(f"Location     : {df_final.iloc[i,2]}")
#                 st.write(f"Website URL  : {df_final.iloc[i,3]}")

#                 with st.expander(label='Job Desription'):
#                     st.write(df_final.iloc[i, 4])
                
#                 st.write(f"Match Probability: {df_final.iloc[i, 5]:.2f}%")
#                 add_vertical_space(3)
        
#         else:
#             st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
#                                 unsafe_allow_html=True)

#     def job_title_filter(scrap_job_title, user_job_title_input):
#         # User Job Title Convert into Lower Case
#         user_input = [i.lower().strip() for i in user_job_title_input]

#         # scraped Job Title Convert into Lower Case
#         scrap_title = [i.lower().strip() for i in [scrap_job_title]]

#         # Verify Any User Job Title in the scraped Job Title
#         confirmation_count = 0
#         for i in user_input:
#             if all(j in scrap_title[0] for j in i.split()):
#                 confirmation_count += 1

#         # Return Job Title if confirmation_count greater than 0 else return NaN
#         if confirmation_count > 0:
#             return scrap_job_title
#         else:
#             return np.nan

#     def main():
#         # Initially set driver to None
#         driver = None
        
#         try:
#             job_title_input, job_location, company_count, skills, submit = linkedin_scraper.get_userinput()
#             add_vertical_space(2)
            
#             if submit:
#                 if job_title_input != [] and job_location != '':
                    
#                     with st.spinner('Chrome Webdriver Setup Initializing...'):
#                         driver = linkedin_scraper.webdriver_setup()
                                       
#                     with st.spinner('Loading More Company Listings...'):
#                         # build URL based on User Job Title Input
#                         link = linkedin_scraper.build_url(job_title_input, job_location)
#                         # Open the Link in LinkedIn and Scroll Down the Page
#                         linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
#                     with st.spinner('Scraping Company Details...'):
#                         # Scraping the Company Name, Location, Job Title and URL Data
#                         df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location)
                    
#                     with st.spinner('Scraping Job Descriptions...'):
#                         # Scraping the Job Descriptin Data
#                         df_final = linkedin_scraper.scrap_job_description(driver, df, company_count, skills)
                    
#                     # Display the Data in User Interface
#                     linkedin_scraper.display_data_userinterface(df_final)
                
#                 # If User Click Submit Button and Job Title is Empty
#                 elif job_title_input == []:
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
#                                 unsafe_allow_html=True)
                
#                 elif job_location == '':
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
#                                 unsafe_allow_html=True)

#         except Exception as e:
#             add_vertical_space(2)
#             st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
#         finally:
#             if driver:
#                 driver.quit()

# # Streamlit Configuration Setup
# streamlit_config()
# add_vertical_space(5)

# # Main function call
# linkedin_scraper.main()




# import time
# import numpy as np
# import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd


# def streamlit_config():
#     # page configuration
#     st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)

#     # title and position
#     st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)

# class linkedin_scraper:

#     def webdriver_setup():
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')

#         driver = webdriver.Chrome(options=options)
#         driver.maximize_window()
#         return driver

#     def get_userinput():
#         add_vertical_space(2)
#         with st.form(key='linkedin_scarp'):
#             add_vertical_space(1)
#             col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
#             with col1:
#                 job_title_input = st.text_input(label='Job Title')
#                 job_title_input = job_title_input.split(',')
#             with col2:
#                 job_location = st.text_input(label='Job Location', value='India')
#             with col3:
#                 company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

#             add_vertical_space(1)
#             skill_input = st.text_input(label='Skills')
#             skill_input = skill_input.split(',')

#             # Submit Button
#             add_vertical_space(1)
#             submit = st.form_submit_button(label='Submit')
#             add_vertical_space(1)
        
#         return job_title_input, job_location, company_count, skill_input, submit

#     def build_url(job_title, job_location):
#         b = []
#         for i in job_title:
#             x = i.split()
#             y = '%20'.join(x)
#             b.append(y)

#         job_title = '%2C%20'.join(b)
#         link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

#         return link
    
#     def open_link(driver, link):
#         while True:
#             # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
#             try:
#                 driver.get(link)
#                 driver.implicitly_wait(5)
#                 time.sleep(3)
#                 driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
#                 return
            
#             # Retry Loading the Page
#             except NoSuchElementException:
#                 continue

#     def link_open_scrolldown(driver, link, company_count):
#         # Open the Link in LinkedIn
#         linkedin_scraper.open_link(driver, link)
#         time.sleep(3)
        
#         # Scraping the Company Data
#         companies_scraped = 0
#         while companies_scraped < company_count:
#             # Scroll Down the Page to load more companies
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Check if there's a "See more" button and click it
#             try:
#                 see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
#                 see_more_button.click()
#                 time.sleep(3)
#             except NoSuchElementException:
#                 break  # No more "See more" button, exit the loop
            
#             # Update the number of scraped companies
#             companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

#         return

#     def scrap_company_data(driver, job_title_input, job_location):
#         # scraping the Company Data
#         company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
#         company_name = [i.text for i in company]

#         location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
#         company_location = [i.text for i in location]

#         title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
#         job_title = [i.text for i in title]

#         url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
#         website_url = [i.get_attribute('href') for i in url]

#         # combine the all data to single dataframe
#         df = pd.DataFrame(company_name, columns=['Company Name'])
#         df['Job Title'] = pd.DataFrame(job_title)
#         df['Location'] = pd.DataFrame(company_location)
#         df['Website URL'] = pd.DataFrame(website_url)

#         # Return Job Title if there are more than 1 matched word else return NaN
#         df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

#         # Return Location if User Job Location in Scraped Location else return NaN
#         df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
#         # Drop Null Values and Reset Index
#         df = df.dropna()
#         df.reset_index(drop=True, inplace=True)

#         return df 

#     def scrap_job_description(driver, df, skills):
#         # Get URL into List
#         website_url = df['Website URL'].tolist()
        
#         # Scrap the Job Description
#         job_description, match_probabilities = [], []
#         for url in website_url:
#             try:
#                 # Open the Link in LinkedIn
#                 linkedin_scraper.open_link(driver, url)

#                 # Click on Show More Button
#                 driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
#                 driver.implicitly_wait(5)
#                 time.sleep(1)

#                 # Get Job Description
#                 description = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')
#                 desc_text = [i.text for i in description][0]

#                 if len(desc_text.strip()) > 0:
#                     job_description.append(desc_text)
#                 else:
#                     job_description.append('Description Not Available')

#                 # Calculate probability of matching skills
#                 match_probability = sum(skill.lower() in desc_text.lower() for skill in skills) / max(len(skills), 1) * 100
#                 match_probabilities.append(match_probability)
            
#             # If URL cannot Loading Properly 
#             except:
#                 job_description.append('Description Not Available')
#                 match_probabilities.append(0)

#         # Add Job Description and Match Probability in Dataframe
#         df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
#         df['Match Probability'] = pd.DataFrame(match_probabilities, columns=['Probability'])
#         df['Match Probability'] = df['Match Probability'].astype(float)
        
#         df = df[df['Job Description'] != 'Description Not Available']
#         df.reset_index(drop=True, inplace=True)

#         return df

#     def display_data_userinterface(df_final):
#         # Display the Data in User Interface
#         add_vertical_space(1)
#         if len(df_final) > 0:
#             for i in range(0, len(df_final)):
                
#                 st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
#                 st.write(f"Company Name : {df_final.iloc[i,0]}")
#                 st.write(f"Job Title    : {df_final.iloc[i,1]}")
#                 st.write(f"Location     : {df_final.iloc[i,2]}")
#                 st.write(f"Website URL  : {df_final.iloc[i,3]}")

#                 with st.expander(label='Job Desription'):
#                     st.write(df_final.iloc[i, 4])
                
#                 st.write(f"Match Probability: {df_final.iloc[i, 5]:.2f}%")
#                 add_vertical_space(3)
        
#         else:
#             st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
#                                 unsafe_allow_html=True)

#     def job_title_filter(scrap_job_title, user_job_title_input):
#         # User Job Title Convert into Lower Case
#         user_input = [i.lower().strip() for i in user_job_title_input]

#         # scraped Job Title Convert into Lower Case
#         scrap_title = [i.lower().strip() for i in [scrap_job_title]]

#         # Verify Any User Job Title in the scraped Job Title
#         confirmation_count = 0
#         for i in user_input:
#             if all(j in scrap_title[0] for j in i.split()):
#                 confirmation_count += 1

#         # Return Job Title if confirmation_count greater than 0 else return NaN
#         if confirmation_count > 0:
#             return scrap_job_title
#         else:
#             return np.nan

#     def main():
#         # Initially set driver to None
#         driver = None
        
#         try:
#             job_title_input, job_location, company_count, skills, submit = linkedin_scraper.get_userinput()
#             add_vertical_space(2)
            
#             if submit:
#                 if job_title_input != [] and job_location != '':
                    
#                     with st.spinner('Chrome Webdriver Setup Initializing...'):
#                         driver = linkedin_scraper.webdriver_setup()
                                       
#                     with st.spinner('Loading More Company Listings...'):
#                         # build URL based on User Job Title Input
#                         link = linkedin_scraper.build_url(job_title_input, job_location)
#                         # Open the Link in LinkedIn and Scroll Down the Page
#                         linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
#                     with st.spinner('Scraping Company Details...'):
#                         # Scraping the Company Name, Location, Job Title and URL Data
#                         df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location)
                    
#                     with st.spinner('Scraping Job Descriptions...'):
#                         # Scraping the Job Descriptin Data
#                         df_final = linkedin_scraper.scrap_job_description(driver, df, skills)
                    
#                     # Display the Data in User Interface
#                     linkedin_scraper.display_data_userinterface(df_final)
                
#                 # If User Click Submit Button and Job Title is Empty
#                 elif job_title_input == []:
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
#                                 unsafe_allow_html=True)
                
#                 elif job_location == '':
#                     st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
#                                 unsafe_allow_html=True)

#         except Exception as e:
#             add_vertical_space(2)
#             st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
#         finally:
#             if driver:
#                 driver.quit()

# # Streamlit Configuration Setup
# streamlit_config()
# add_vertical_space(5)

# # Main function call
# linkedin_scraper.main()



































import time
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def streamlit_config():
    # page configuration
    st.set_page_config(page_title='Aim🔎Seeker', layout="wide")

    # page header transparent color
    page_background_color = """
    <style>

    [data-testid="stHeader"] 
    {
    background: rgba(0,0,0,0);
    }

    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)

    # title and position
    st.markdown(f'<h1 style="text-align: center;"> Welcome to <br> Aim🔎Seeker</h1>', unsafe_allow_html=True)

class linkedin_scraper:

    def webdriver_setup():
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver

    def get_userinput():
        add_vertical_space(2)
        with st.form(key='linkedin_scarp'):
            add_vertical_space(1)
            col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
            with col1:
                job_title_input = st.text_input(label='Job Title')
                job_title_input = job_title_input.split(',')
            with col2:
                job_location = st.text_input(label='Job Location', value='')
            with col3:
                company_count = st.number_input(label='Company Count', min_value=1, value=1, step=1)

            add_vertical_space(1)
            skill_input = st.text_input(label='Skills')
            skill_input = skill_input.split(',')

            # Submit Button
            add_vertical_space(1)
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)
        
        return job_title_input, job_location, company_count, skill_input, submit

    def build_url(job_title, job_location):
        b = []
        for i in job_title:
            x = i.split()
            y = '%20'.join(x)
            b.append(y)

        job_title = '%2C%20'.join(b)
        link = f"https://www.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=&f_TPR=r604800&position=1&pageNum=0"

        return link
    
    def open_link(driver, link):
        while True:
            # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
            try:
                driver.get(link)
                driver.implicitly_wait(5)
                time.sleep(3)
                driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
                return
            
            # Retry Loading the Page
            except NoSuchElementException:
                continue

    def link_open_scrolldown(driver, link, company_count):
        # Open the Link in LinkedIn
        linkedin_scraper.open_link(driver, link)
        time.sleep(3)
        
        # Scraping the Company Data
        companies_scraped = 0
        while companies_scraped < company_count:
            # Scroll Down the Page to load more companies
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            # Check if there's a "See more" button and click it
            try:
                see_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more companies']")
                see_more_button.click()
                time.sleep(3)
            except NoSuchElementException:
                break  # No more "See more" button, exit the loop
            
            # Update the number of scraped companies
            companies_scraped = len(driver.find_elements(By.CSS_SELECTOR, "h4.base-search-card__subtitle"))

        return

    def scrap_company_data(driver, job_title_input, job_location):
        # scraping the Company Data
        company = driver.find_elements(by=By.CSS_SELECTOR, value='h4.base-search-card__subtitle')
        company_name = [i.text for i in company]

        location = driver.find_elements(by=By.CSS_SELECTOR, value='span.job-search-card__location')
        company_location = [i.text for i in location]

        title = driver.find_elements(by=By.CSS_SELECTOR, value='h3.base-search-card__title')
        job_title = [i.text for i in title]

        url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
        website_url = [i.get_attribute('href') for i in url]

        # combine the all data to single dataframe
        df = pd.DataFrame(company_name, columns=['Company Name'])
        df['Job Title'] = pd.DataFrame(job_title)
        df['Location'] = pd.DataFrame(company_location)
        df['Website URL'] = pd.DataFrame(website_url)

        # Return Job Title if there are more than 1 matched word else return NaN
        df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scraper.job_title_filter(x, job_title_input))

        # Return Location if User Job Location in Scraped Location else return NaN
        df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        
        # Drop Null Values and Reset Index
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)

        return df 

    def scrap_job_description(driver, df, skills):
        # Get URL into List
        website_url = df['Website URL'].tolist()
        
        # Scrap the Job Description
        job_description, match_probabilities = [], []
        for url in website_url:
            try:
                # Open the Link in LinkedIn
                linkedin_scraper.open_link(driver, url)

                # Click on Show More Button
                driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
                driver.implicitly_wait(5)
                time.sleep(1)

                # Get Job Description
                description = driver.find_elements(by=By.CSS_SELECTOR, value='div.show-more-less-html__markup.relative.overflow-hidden')
                desc_text = [i.text for i in description][0]

                if len(desc_text.strip()) > 0:
                    job_description.append(desc_text)
                else:
                    job_description.append('Description Not Available')

                # Calculate probability of matching skills
                match_probability = sum(skill.lower() in desc_text.lower() for skill in skills) / max(len(skills), 1) * 100
                match_probabilities.append(match_probability)
            
            # If URL cannot Loading Properly 
            except:
                job_description.append('Description Not Available')
                match_probabilities.append(0)

        # Add Job Description and Match Probability in Dataframe
        df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
        df['Match Probability'] = pd.DataFrame(match_probabilities, columns=['Probability'])
        df['Match Probability'] = df['Match Probability'].astype(float)
        
        df = df[df['Job Description'] != 'Description Not Available']
        df.reset_index(drop=True, inplace=True)

        return df

    def display_data_userinterface(df_final):
        # Display the Data in User Interface
        add_vertical_space(1)
        if len(df_final) > 0:
            for i in range(0, len(df_final)):
                
                st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i+1}</h3>', unsafe_allow_html=True)
                st.write(f"Company Name : {df_final.iloc[i,0]}")
                st.write(f"Job Title    : {df_final.iloc[i,1]}")
                st.write(f"Location     : {df_final.iloc[i,2]}")
                st.write(f"Website URL  : {df_final.iloc[i,3]}")

                with st.expander(label='Job Desription'):
                    st.write(df_final.iloc[i, 4])
                
                st.write(f"Match Probability: {df_final.iloc[i, 5]:.2f}%")
                add_vertical_space(3)
        
        else:
            st.markdown(f'<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', 
                                unsafe_allow_html=True)

    def job_title_filter(scrap_job_title, user_job_title_input):
        # User Job Title Convert into Lower Case
        user_input = [i.lower().strip() for i in user_job_title_input]

        # scraped Job Title Convert into Lower Case
        scrap_title = [i.lower().strip() for i in [scrap_job_title]]

        # Verify Any User Job Title in the scraped Job Title
        confirmation_count = 0
        for i in user_input:
            if all(j in scrap_title[0] for j in i.split()):
                confirmation_count += 1

        # Return Job Title if confirmation_count greater than 0 else return NaN
        if confirmation_count > 0:
            return scrap_job_title
        else:
            return np.nan

    def main():
        # Initially set driver to None
        driver = None
        
        try:
            job_title_input, job_location, company_count, skills, submit = linkedin_scraper.get_userinput()
            add_vertical_space(2)
            
            if submit:
                if job_title_input != [] and job_location != '':
                    
                    with st.spinner('Chrome Webdriver Setup Initializing...'):
                        driver = linkedin_scraper.webdriver_setup()
                                       
                    with st.spinner('Loading More Company Listings...'):
                        # build URL based on User Job Title Input
                        link = linkedin_scraper.build_url(job_title_input, job_location)
                        # Open the Link in LinkedIn and Scroll Down the Page
                        linkedin_scraper.link_open_scrolldown(driver, link, company_count)
                    
                    with st.spinner('Scraping Company Details...'):
                        # Scraping the Company Name, Location, Job Title and URL Data
                        df = linkedin_scraper.scrap_company_data(driver, job_title_input, job_location)
                    
                    with st.spinner('Scraping Job Descriptions...'):
                        # Scraping the Job Descriptin Data
                        df_final = linkedin_scraper.scrap_job_description(driver, df, skills)
                    
                    # Display the Data in User Interface
                    linkedin_scraper.display_data_userinterface(df_final)
                
                # If User Click Submit Button and Job Title is Empty
                elif job_title_input == []:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">Job Title is Empty</h5>', 
                                unsafe_allow_html=True)
                
                elif job_location == '':
                    st.markdown(f'<h5 style="text-align: center;color: orange;">Job Location is Empty</h5>', 
                                unsafe_allow_html=True)

        except Exception as e:
            add_vertical_space(2)
            st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
        
        finally:
            if driver:
                driver.quit()

# Streamlit Configuration Setup
streamlit_config()
add_vertical_space(5)

# Main function call
linkedin_scraper.main()
