import streamlit as st
import pandas as pd
import requests
from collections import Counter
import plotly.graph_objects as go

st.set_page_config(page_title="تصنيف الشخصيات حسب تقييم الزملاء", layout="wide")

# وصف كل كلستر
cluster_descriptions = {
    0: "😌 ذا الواحد اللي عايش حياته على مود رايق. كل شيء عنده \"عادي\"، يقهوي نفسه الساعة ٥ العصر ويحوس بالبلانر يوم ويختفي سنة...",
    1: "🎭 ذا اللي قلبه ألين من خبز التنور. يبكي من إعلان زين ويكتب خواطر عن ذكرى منديل...",
    2: "📚 ذا اللي لو قلت له \"خل نروح الطايف\" قالك: \"طيب أرسل لي على الإيميل الخطة\"...",
    3: "🔕 ذا اللي تحسبه طالع من مسلسل كوري، بس هو ساكن في حي الربيع، بس ما أحد قد شافه...",
    4: "🎢 هذا بركان عواطف. يغير اهتماماته أسرع من عروض نون، وكل شوي يدخل هواية جديدة..."
}

# تنسيق عام للصفحة
st.markdown("""
<style>
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
    .stSlider label, .stButton>button, .stForm {
        text-align: right;
    }
    .stForm {
        background-color: #f9f9f9;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        margin-bottom: 25px;
        border: 1px solid #e0e0e0;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

st.title("👥 تطبيق تصنيف الشخصية حسب تقييم الزملاء")
st.markdown("يتم تقييم كل شخص بواسطة الآخرين. يعرض النظام متوسط درجات السمات وتوقع الانتماء لأحد المجموعات.")

names = [
    "وسن عبدالهادي العتيبي", "عبدالعزيز فهد الحيزان", "أزهار سعود التميمي", "عبدالمحسن عادل الدغيم",
    "عمر سليمان السريع", "غادة عبدالرحمن العمري", "عبدالله عمر الدايل", "رهف عمر مسلمي",
    "رناد عبدالرحمن الحجي", "يوسف سعد الديحاني", "مهند إبراهيم أبوالسنون", "الهنوف عبدالمحسن السويد",
    "مجد عبدالله العتيبي", "عبدالله أحمد الزهراني", "فيصل فهد الخنين", "فراس حمد السويد",
    "دانية عماد الدبيسي", "فيصل عبدالله آل مفرح", "نجلاء باسم المرشدي", "محمد عبدالله الحسيني",
    "عبدالعزيز خالد عبدالعزيز آل فريان", "ريناد رأفت ياسين", "مروان فهد الهندي", "وريف عبدالله اليوسف",
    "عبدالعزيز سعد الخرجي"
]

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

# ===== نموذج الإدخال =====
st.subheader("✍️ أدخل تقييمك")
with st.form("submit_form"):
    target_person_name = st.selectbox("👤 من الشخص الذي تقوم بتقييمه؟", names, key="target")
    rater_name = st.selectbox("🧑 من أنت (المُقيّم)؟", names, key="rater")

    responses = {}
    for key, question in questions.items():
        responses[key] = st.slider(question, min_value=0, max_value=5, value=3, key=key)

    submitted = st.form_submit_button("إرسال التقييم")

# ===== تحليل وإرسال البيانات إلى API =====
if submitted:
    try:
        payload = {
            "target_person": target_person_name,
            "rater": rater_name,
            **responses  # يفك القاموس responses ويدمجه في الـ payload
        }
        res = requests.post("http://localhost:8000/analyze-peer", json=payload)

        if res.status_code == 200:
            result = res.json()
            st.success(f"✅ تم تسجيل تقييمك لـ {target_person_name} بنجاح!")

            st.markdown(f"### الكلستر الخاص بـ {target_person_name}: `{result['cluster']}`")
            st.markdown(f"**{result['description']}**")

            trait_scores = result["scores"]
            summary_df = pd.DataFrame([trait_scores])
            st.dataframe(summary_df.style.format(precision=1), use_container_width=True)

            st.markdown("### تمثيل مرئي لأبعاد الشخصية")
            traits = list(trait_scores.keys())
            values = [trait_scores[t] * 10 for t in traits]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=traits,
                y=values,
                name='السمات',
                marker_color='lightgreen',
                opacity=0.6
            ))
            fig.add_trace(go.Scatter(
                x=traits,
                y=values,
                mode='lines+markers',
                name='مؤشر الشخصية',
                line=dict(color='red'),
                marker=dict(size=10)
            ))
            fig.update_layout(
                title=f"تحليل السمات لـ {target_person_name}",
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
