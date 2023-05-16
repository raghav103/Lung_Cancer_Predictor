import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Define the input features and their respective default values
default_age = 50
default_gender = 'Male'
default_smoking_history = 'Never'
default_exposure_history = 'No'

# Define the categorical variables and their respective options
gender_options = ['Male', 'Female']
smoking_history_options = ['Never', 'Former', 'Current']
exposure_history_options = ['No', 'Yes']

# Load the trained model
model = joblib.load('model.pkl')

# Define the function to preprocess the user inputs
def preprocess_input(age, gender, smoking_history, exposure_history):
    # Encode the categorical variables
    gender_male = 1 if gender == 'Male' else 0
    smoking_history_encoded = smoking_history_options.index(smoking_history)
    exposure_history_encoded = exposure_history_options.index(exposure_history)
    
    # Concatenate the input features
    input_features = np.array([age, gender_male, smoking_history_encoded, exposure_history_encoded]).reshape(1, -1)
    
    return input_features

# Define the function to predict the lung cancer risk
def predict_cancer(input_features):
    # Predict the probability of lung cancer
    cancer_prob = model.predict_proba(input_features)[:,1][0]
    
    return cancer_prob

# Define the streamlit app
def app():
    # Set the title and the page icon
    st.set_page_config(page_title='Lung Cancer Risk Calculator', page_icon=':hospital:')
    
    # Set the app title
    st.title('Lung Cancer Risk Calculator')
    
    # Define the input widgets
    age = st.slider('Age', 18, 100, default_age)
    gender = st.selectbox('Gender', gender_options, index=gender_options.index(default_gender))
    smoking_history = st.selectbox('Smoking History', smoking_history_options, index=smoking_history_options.index(default_smoking_history))
    exposure_history = st.selectbox('Exposure History', exposure_history_options, index=exposure_history_options.index(default_exposure_history))
    
    # Preprocess the input features
    input_features = preprocess_input(age, gender, smoking_history, exposure_history)
    
    # Make the prediction
    cancer_prob = predict_cancer(input_features)
    
    # Display the prediction
    st.subheader('Results')
    if cancer_prob >= 0.5:
        st.write('Based on the input features, the patient is predicted to have a high risk of lung cancer.')
    else:
        st.write('Based on the input features, the patient is predicted to have a low risk of lung cancer.')
    st.write(f'Predicted Probability of Lung Cancer: {cancer_prob:.2%}')
