# app.py (Welcome Page)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os


st.set_page_config(page_title="مرحبًا بك", layout="wide")

st.markdown("""
    <style>
    /* الخط العام */
    html, body, [class*="st-"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        background-color: #f5f7fa;
        color: #333;
    }
  
    h1, h2, h3 {
        color: #2e5cb8;
        margin-bottom: 10px;
        font-family: 'Cairo', sans-serif !important;

    }

    ul {
    background-color: #ffffff;
    padding: 15px 20px;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.06);
    max-width: 700px;
    margin: 10px 0 10px auto;  /* خلى auto بس لليسار */
    line-height: 2;
    text-align: right;
    }
    
    li {
    margin: 10px 0 10px auto;  /* خلى auto بس لليسار */
    font-size: 18px;
    }

    p {
        line-height: 1.8;
    }

    /* تحسين مظهر الصور */
    img {
        border-radius: 12px;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
    }

    /* تحسين الزر لاحقًا إن وجد */
    .stButton>button {
        background-color: #2e5cb8;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        transition: 0.3s;
        border: none;
    }

    .stButton>button:hover {
        background-color: #1c3f91;
    }
    </style>

    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

image_path = os.path.join(os.path.dirname(__file__), "public", "6963-Photoroom.png")
head_img = Image.open(image_path)
st.image(head_img, use_container_width=True)


# Title: Welcome Message
st.markdown("<h1 style='text-align: right; direction: rtl;'>مرحبًا بك في تطبيق تحليل الشخصية 🧠</h1>", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: right; direction: rtl; font-size: 18px;'>
هذا التطبيق يساعدك على فهم شخصيتك بشكل أعمق من خلال اختبار مبني على السمات الخمس الكبرى للشخصية.
يمكنك الاختيار من بين اختبارات متعددة، أو مشاركة الرابط مع أصدقائك لمعرفة كيف يرون شخصيتك!
</p>
""", unsafe_allow_html=True)

# Section: Big Five Traits
st.markdown("""
<h3 style='text-align: right; direction: rtl;'>السمات الخمس الكبرى:</h3>
<ul style='direction: rtl; text-align: right; font-size: 18px;'>
  <li>الانفتاح على التجارب: فضولي أو حذر</li>
  <li>الضمير الحي: منظم أم مهمل ومسترخٍ</li>
  <li>الانبساط: اجتماعي ونشيط مقابل منطوي ومحافظ</li>
  <li>القبول: ودود ومتعاطف مقابل صعب ومتحفظ</li>
  <li>العصابية: حساس وقلق مقابل واثق ومستقر</li>
</ul>
""", unsafe_allow_html=True)

# Centered Image
image_path = os.path.join(os.path.dirname(__file__), "public", "5personality-Photoroom.png")
image = Image.open(image_path)

left_co, cent_co, right_co = st.columns(3)
with cent_co:
    st.image(image, caption="السمات الخمس الكبرى", use_container_width=True)

# Explanation
st.markdown("""
<h3 style='text-align: right; direction: rtl;'>لماذا نستخدم هذا النموذج؟</h3>
<ul style='direction: rtl; text-align: right; font-size: 18px;'>
  <li>النموذج يعتمد على تحليل الكلمات التي تصف الشخصية.</li>
  <li>كمثال: الشخص المنضبط يوصف غالبًا بأنه "دائم الاستعداد".</li>
  <li>هذه النظرية شائعة وسهلة الفهم، وتُستخدم على نطاق واسع في علم النفس.</li>
</ul>
""", unsafe_allow_html=True)