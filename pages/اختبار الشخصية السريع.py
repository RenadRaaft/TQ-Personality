import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# إعداد الصفحة والتنسيق العام
st.set_page_config(page_title="تحليل الشخصية", layout="wide")

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

st.markdown("""
<style>
    /* Base RTL settings */
    .rtl, .stMarkdown, .stTitle, p, h1, h2, h3, h4, h5, h6, .stButton {
        direction: rtl;
        text-align: right;
    }
    html, body, [class*="st-"] {
        background-color: #f5f7fa;
    }
            
    /* Ensure slider label text stays RTL */
    .stSlider label {
        text-align: right;
        width: 100%;
        display: block;
    }
    /* Set all text color to black */
    body, .stMarkdown, .stTitle, p, h1, h2, h3, h4, h5, h6, .stButton {
        color: black;
    }

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .stForm {
        background-color: #f9f9f9;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        margin-bottom: 25px;
        border: 1px solid #e0e0e0;
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 25px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }
    .stButton button:hover {
        background-color: #0056b3;
        transform: scale(1.05);
    }
    .stButton button:active {
        background-color: #004085;
        transform: scale(1);
    }
</style>
""", unsafe_allow_html=True)

# واجهة المستخدم
st.markdown('<h1 style="color: black;">تحليل شخصيتك بطريقتنا الخاصة</h1>', unsafe_allow_html=True)

st.markdown("""
### هل عمرك حسّيت إنك كائن غريب؟
لا تشيل هم، احنا هنا نحلل شخصيتك ونطقطق عليها شوي (بحب طبعًا).

في هالموقع، ما راح نقول لك إنك "طموح ومبدع" وبس، لا لا...
راح نكشف لك الحقيقة كاملة: إنك مزاجي، تحب المفطّح، وتخاف من المشاعر 😌

جاوب على الأسئلة وخلّنا نبدأ حفلة التحليل ✨
""")

st.markdown("**اختر من 0 (لا أوافق أبدًا) إلى 5 (أوافق تمامًا)**")

# الأسئلة حسب السمات
questions = {
    'EXT2': 'أنا ما أتكلم كثير',
    'EXT3': 'أشعر بالراحة حول الناس',
    'EXT4': 'أفضل أكون بالخلفية وما أكون مركز الانتباه',
    'EXT5': 'أبدأ المحادثات من نفسي',
    'EXT7': 'أتكلم مع ناس كثير في الحفلات',
    'EXT9': 'ما عندي مشكلة أكون مركز الانتباه',
    'EXT10': 'أكون ساكت لما أتعامل مع ناس ما أعرفهم',
    'EST6': 'أنزعج بسهولة',
    'EST8': 'مزاجي يتقلب كثير',
    'AGR7': 'ما أهتم كثير بالناس الآخرين',
    'OPN9': 'أقضي وقت أفكر في أشياء كثيرة',
    'CSN4': 'أخبص الأمور وما أرتبها'
}

# نموذج الإدخال
responses = {}
with st.form("form_arabic"):
    for key, question in questions.items():
        responses[key] = st.slider(question, min_value=0, max_value=5, value=3, key=key)
    submitted = st.form_submit_button("احللني!")

# إرسال وتحليل
if submitted:
    try:
        res = requests.post("http://127.0.0.1:8000/analyze", json=responses)

        if res.status_code == 200:
            result = res.json()

            st.success("✨ تم التحليل! وهذه النتيجة 👇")
            st.markdown(f"### الكلستر الخاص بك: `{result['cluster']}`")
            st.markdown(f"**{result['description']}**")

            st.markdown("### ملخص الأبعاد الخمسة:")
            trait_scores = result["scores"]
            summary_df = pd.DataFrame([trait_scores])
            st.dataframe(summary_df.style.format(precision=1), use_container_width=True)

            st.markdown("### تمثيل مرئي لأبعادك")
            traits = list(trait_scores.keys())
            values = [trait_scores[t] * 10 for t in traits]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=traits,
                y=values,
                name='قيمك',
                marker_color='lightgreen',
                opacity=0.6
            ))

            fig.add_trace(go.Scatter(
                x=traits,
                y=values,
                mode='lines+markers',
                name='خط التحليل',
                line=dict(color='red'),
                marker=dict(size=10)
            ))

            fig.update_layout(
                title=f"الكلستر رقم {result['cluster']}",
                yaxis=dict(range=[0, 50]),
                xaxis_title="البُعد",
                yaxis_title="الدرجة (×10)",
                template="plotly_white"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("💥 صار خطأ في الاتصال بالـ API. تأكد أنه شغال.")
    except Exception as e:
        st.error(f"❌ فشل الاتصال بالسيرفر: {e}")