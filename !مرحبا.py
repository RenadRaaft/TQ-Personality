# app.py (Welcome Page)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="مرحبًا بك", layout="wide")

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
<h3 style='text-align: right; direction: rtl;'>ما هي السمات الخمس الكبرى؟</h3>
<ul style='direction: rtl; text-align: right; font-size: 18px;'>
  <li>الانفتاح على التجارب: فضولي أو حذر</li>
  <li>الضمير الحي: منظم أم مهمل ومسترخٍ</li>
  <li>الانبساط: اجتماعي ونشيط مقابل منطوي ومحافظ</li>
  <li>القبول: ودود ومتعاطف مقابل صعب ومتحفظ</li>
  <li>العصابية: حساس وقلق مقابل واثق ومستقر</li>
</ul>
""", unsafe_allow_html=True)

# Centered Image
image = Image.open("public/5personality.png")
left_co, cent_co, right_co = st.columns(3)
with cent_co:
    st.image(image, caption="السمات الخمس الكبرى", use_column_width=True)

# Explanation
st.markdown("""
<h3 style='text-align: right; direction: rtl;'>لماذا نستخدم هذا النموذج؟</h3>
<ul style='direction: rtl; text-align: right; font-size: 18px;'>
  <li>النموذج يعتمد على تحليل الكلمات التي تصف الشخصية.</li>
  <li>كمثال: الشخص المنضبط يوصف غالبًا بأنه "دائم الاستعداد".</li>
  <li>هذه النظرية شائعة وسهلة الفهم، وتُستخدم على نطاق واسع في علم النفس.</li>
</ul>
""", unsafe_allow_html=True)