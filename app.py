import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load model and data
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

st.title("💻 Laptop Price Predictor")

# Input fields
company = st.selectbox('Brand', df['Company'].unique())
type = st.selectbox('Type', df['TypeName'].unique())
ram = st.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
weight = st.number_input('Weight of the Laptop')

touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])
touchscreen = 1 if touchscreen == 'Yes' else 0

ips = st.selectbox('IPS Display', ['No', 'Yes'])
ips = 1 if ips == 'Yes' else 0

screen_size = st.slider('Screen Size (inches)', 10.0, 18.0, 13.0)

resolution = st.selectbox('Screen Resolution', [
    '1920x1080', '1366x768', '1600x900', '3840x2160',
    '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'
])
X_res, Y_res = map(int, resolution.split('x'))
ppi = ((X_res ** 2 + Y_res ** 2) ** 0.5) / screen_size

cpu = st.selectbox('CPU', df['Cpu brand'].unique())
hdd = st.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048])
ssd = st.selectbox('SSD (in GB)', [0, 8, 128, 256, 512, 1024])
gpu = st.selectbox('GPU Brand', df['Gpu brand'].unique())
os = st.selectbox('Operating System', df['os'].unique())

# Predict
if st.button('Predict Price'):
    input_df = pd.DataFrame([[company, type, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os]],
        columns=['Company', 'TypeName', 'Ram', 'Weight', 'TouchScreen', 'Ips', 'PPI',
                 'Cpu brand', 'HDD', 'SSD', 'Gpu brand', 'os'])

    predicted_log_price = pipe.predict(input_df)[0]
    predicted_price = int(np.exp(predicted_log_price))
    st.success(f"💰 The predicted price of this configuration is ₹ {predicted_price}")
