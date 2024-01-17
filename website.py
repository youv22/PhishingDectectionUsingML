import streamlit as st
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re
import matplotlib.pyplot as plt
import time


st.title('Phishing Website Detection using Machine Learning')
st.write('This website has been developed for my ongoing Masters dissertation at University of Technology, Mauritius. '
         'The objective of the website is detecting phishing websites using content data. '
         'You can see the details of approach, data set, and feature set if you click on _"Project Details"_.')

with st.expander("PROJECT DETAILS"):

    st.subheader('Approach')

    st.write('I used _supervised learning_ to classify phishing and legitimate websites. '
             'I benefit from content-based approach and focus on html of the websites. '
             'Also, I used scikit-learn for the ML models. '
             )

    st.write('For my Masters thesis, '
             'I first created my own data set and defined features. '
             'Some features were derived from the literature review and others were based on manual analysis. '
             'The requests library was used to collect data, BeautifulSoup module to parse and extract features. ')

    st.subheader('Data set')
    st.write('_"phishtank.org"_ & _"tranco-list.eu"_ were used as data sources. ')
    st.write('Totally 26584 websites ==> **_16060_ legitimate** websites | **_10524_ phishing** websites')
    st.write('Data set was created in December 2023.')

    # ----- FOR THE PIE CHART ----- #
    labels = 'phishing', 'legitimate'
    phishing_rate = int(ml.phishing_df.shape[0] / (ml.phishing_df.shape[0] + ml.legitimate_df.shape[0]) * 100)
    legitimate_rate = 100 - phishing_rate
    sizes = [phishing_rate, legitimate_rate]
    explode = (0.1, 0)
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=90, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)
    # ----- !!!!! ----- #

    st.write('Features + URL + Label ==> Dataframe')
    st.markdown('label is 1 for phishing, 0 for legitimate')
    number = st.slider("Select row number to display", 0, 100)
    st.dataframe(ml.legitimate_df.head(number))

    st.subheader('Results')
    st.write('5 different ML classifiers of scikit-learn were used and tested by implementing k-fold cross validation. '
             'First, their confusion matrices were obtained. '
             'Then their accuracy, precision and recall scores were calculated accordingly. '
             '\nComparison table is displayed below: ')
    st.table(ml.df_results)
    st.write('NB --> Gaussian Naive Bayes')
    st.write('SVM --> Support Vector Machine')
    st.write('DT --> Decision Tree')
    st.write('RF --> Random Forest')
    st.write('AB --> AdaBoost')

choice = st.selectbox("Please select your machine learning model",
                      [
                          'Gaussian Naive Bayes', 'Support Vector Machine', 'Decision Tree', 'Random Forest',
                          'AdaBoost'
                      ]
                      )

model = ml.nb_model

if choice == 'Gaussian Naive Bayes':
    model = ml.nb_model
    st.write('GNB model is selected!')
elif choice == 'Support Vector Machine':
    model = ml.svm_model
    st.write('SVM model is selected!')
elif choice == 'Decision Tree':
    model = ml.dt_model
    st.write('DT model is selected!')
elif choice == 'Random Forest':
    model = ml.rf_model
    st.write('RF model is selected!')
elif choice == 'AdaBoost':
    model = ml.ab_model
    st.write('AB model is selected!')


url = st.text_input('Enter the URL')
# check the url is valid or not
if st.button('Check!'):
    try:
         start_time = time.time()  # Record the start time
         response = re.get(url, verify=False, timeout=4)
        if response.status_code != 200:
            print(". HTTP connection was not successful for the URL: ", url)
        else:
         response.raise_for_status()  # Check if the HTTP request was successful
         soup = BeautifulSoup(response.content, "html.parser")
         vector = [fe.create_vector(soup)]  # it should be 2d array, so I added []
         model_start_time = time.time()  # Record the start time for model prediction
         result = model.predict(vector)
         model_end_time = time.time()  # Record the end time for model prediction
                 
         if result[0] == 0:
                  st.success("This web page seems a legitimate!")
         else:
                  st.warning("Attention! This web page is a potential PHISHING!")

         end_time = time.time()  # Record the end time
         total_time = end_time - start_time
         model_time = model_end_time - model_start_time
         st.info(f"Total time: {total_time:.4f} seconds")
         st.info(f"Model prediction time: {model_time:.4f} seconds")

    except re.exceptions.HTTPError as e:
        st.error(f"HTTP error occurred: {e}")
    except re.exceptions.Timeout:
        st.error("Request timed out. This could be due to a slow or unresponsive server. Please try again later.")
    except re.exceptions.TooManyRedirects:
        st.error("Too many redirects. Please check the URL.")
    except re.exceptions.ConnectionError:
        st.error("Connection error. Please check the URL and try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
