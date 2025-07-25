import streamlit as st
import requests

API_URL = "https://machine-predictive-maintenance-i9kc.onrender.com/predict"

st.set_page_config(page_title='Machine Predictive Maintenance Classification')
st.title('Machine Predictive Maintenance Classification')
st.write("This is a simple web application that uses a machine learning model to classify machine failures.")
st.markdown("Enter the following parameters to classify the machine failure:")
with st.form("my_form"):
    Type=st.selectbox("Type", ["L", "M", "H"])
    Air_temperature =st.number_input("Air temperature [K]", min_value=250.0, max_value=400.0, value=298.0)
    Process_temperature  =st.number_input("Process temperature [K]", min_value=250.0, max_value=500.0, value=310.0)
    Rotational_speed= st.number_input("Rotational speed [rpm]", min_value=100.0, max_value=5000.0, value=1500.0)
    Torque= st.number_input("Torque [Nm]", min_value=0.0, max_value=100.0, value=40.0)
    Tool_wear=st.number_input("Tool wear [min]", min_value=0.0, max_value=500.0, value=200.0)
    submit = st.form_submit_button("Predict Failure")

if submit:
    if not all([Type, Air_temperature, Process_temperature, Rotational_speed, Torque, Tool_wear ]): 
        st.error("Please fill in all the fields")
    else:
        with st.spinner("Classifying..."):
            
            response = requests.post(API_URL, json={"Type": Type, "Air temperature [K]": Air_temperature,"Process temperature [K]":Process_temperature,"Rotational speed [rpm]":Rotational_speed,"Torque [Nm]":Torque,"Tool wear [min]":Tool_wear})
            if response.status_code == 200:
              result = response.json()
              st.success(f"✅ Classified as: **{result['predicted_failure_type']}**")
            else:
             st.error(f"❌ Failed to classify (Status code: {response.status_code})")
             st.json(response.json())

        