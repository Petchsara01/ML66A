# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 16:04:41 2026

@author: Lab
"""

import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# โหลดโมเดล
riding_model = pickle.load(open("Riding_model.sav",'rb'))
loan_model = pickle.load(open("loan_model.sav",'rb'))
bmi_model = pickle.load(open("bmi_model.sav",'rb'))

with st.sidebar:
    select = option_menu(
        'Classification', ['Loan', 'Riding', 'BMI']
    )
    
    gender_map = {
        'Female': 0,
        'Male': 1
    }

    education_map = {
        'Associate': 0,
        'Bachelor': 1,
        'Doctorate': 2,
        'High School': 3,
        'Master': 4
    }

    home_map = {
        'MORTGAGE': 0,
        'OTHER': 1,
        'OWN': 2,
        'RENT': 3
    }

    intent_map = {
        'DEBTCONSOLIDATION': 0,
        'EDUCATION': 1,
        'HOMEIMPROVEMENT': 2,
        'MEDICAL': 3,
        'PERSONAL': 4,
        'VENTURE': 5
    }

    default_map = {
        'No': 0,
        'Yes': 1
    }

# ==========================================
# 1. หน้า Loan
# ==========================================
if select == 'Loan':
    st.title('Loan Classification')
    person_age = st.text_input('person_age')
    person_gender = st.selectbox('person_gender', gender_map) 
    person_education = st.selectbox('person_education', education_map)
    person_income = st.text_input('person_income')
    person_emp_exp = st.text_input('person_emp_exp')
    person_home_ownership = st.selectbox('person_home_ownership', home_map)
    loan_amnt = st.text_input('loan_amnt')
    loan_intent = st.selectbox('loan_intent', intent_map)
    loan_int_rate = st.text_input('loan_int_rate')
    loan_percent_income = st.text_input('loan_percent_income')
    cb_person_cred_hist_length = st.text_input('cb_person_cred_hist_length')
    credit_score = st.text_input('credit_score')
    previous_loan_defaults_on_file = st.selectbox(
        'previous_loan_defaults_on_file',
        default_map
    )
    
    loan_prediction = ''
    
    if st.button('Predict'):
        try:
            loan_prediction = loan_model.predict([
                [
                    float(person_age),
                    gender_map[person_gender],
                    education_map[person_education],
                    float(person_income),
                    float(person_emp_exp),
                    home_map[person_home_ownership],
                    float(loan_amnt),
                    intent_map[loan_intent],
                    float(loan_int_rate),
                    float(loan_percent_income),
                    float(cb_person_cred_hist_length),
                    float(credit_score),
                    default_map[previous_loan_defaults_on_file]
                ]
            ])
            if loan_prediction[0] == 0:
                loan_prediction_text = 'Non Accept'
            else:
                loan_prediction_text = 'Accept'
                
            st.success(loan_prediction_text)
        except ValueError:
            st.error("กรุณากรอกข้อมูลตัวเลขให้ครบถ้วนและถูกต้อง")

# ==========================================
# 2. หน้า BMI
# ==========================================
elif select == 'BMI':
    st.title('BMI Classification')
    
    # สร้าง Dictionary สำหรับแปลงค่าที่พยากรณ์ได้เป็นข้อความ
    bmi_category_map = {
        0: 'Extremly Weak',
        1: 'Weak',
        2: 'Normal',
        3: 'Overweight',
        4: 'Obesity',
        5: 'Extreme Obesity'
    }
    
    person_gender = st.selectbox('Gender', gender_map) 
    person_height = st.text_input('Height (cm)')
    person_weight = st.text_input('Weight (kg)')
    
    if st.button('Predict'):
        try:
            # นำค่าไปทำนายผล 
            bmi_prediction = bmi_model.predict([
                [
                    gender_map[person_gender], 
                    float(person_height), 
                    float(person_weight)
                ]
            ])
            
            # ดึงผลลัพธ์ที่เป็นตัวเลข (0-5) ออกมา
            predicted_class = int(bmi_prediction[0])
            
            # แปลงตัวเลขเป็นข้อความตาม Mapping ที่สร้างไว้
            result_text = bmi_category_map.get(predicted_class, "Unknown Category")
            
            # แสดงผลลัพธ์
            st.success(f'Predicted BMI Category: {result_text}')
            
        except ValueError:
            st.error("กรุณากรอกข้อมูลส่วนสูงและน้ำหนักเป็นตัวเลขให้ถูกต้อง")

# ==========================================
# 3. หน้า Riding Mower
# ==========================================
elif select == 'Riding':
    st.title('Riding Mower Classification')
    
    Income = st.text_input('รายได้')
    LotSize = st.text_input('พื้นที่บ้าน')
    
    if st.button('Predict'):
        try:
            Riding_prediction = riding_model.predict([
                [float(Income), float(LotSize)]
            ])
            if Riding_prediction[0] == 0:
                Riding_prediction_text = 'Non Owner'
            else:
                Riding_prediction_text = 'Owner'
                
            st.success(Riding_prediction_text)
        except ValueError:
            st.error("กรุณากรอกข้อมูลรายได้และพื้นที่บ้านเป็นตัวเลขให้ถูกต้อง")
