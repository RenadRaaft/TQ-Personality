import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="تحليل الشخصية الكامل", layout="wide")

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
        direction: rtl;
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

st.title("تحليل شخصيتك باستخدام 50 سؤال")

st.markdown("""
### جاوب على 50 سؤال، وكل إجابتك راح تساعدنا نحطك في الكلستر الأقرب لك 👇
""")

# الأسئلة بالإنجليزية (للتوافق مع النموذج)
ext_questions = {
    'EXT1': 'أنا جو الحفلة',
    'EXT2': 'أنا ما أتكلم كثير',
    'EXT3': 'أشعر بالراحة حول الناس',
    'EXT4': 'أفضل أكون في الخلفية',
    'EXT5': 'أبدأ المحادثات من نفسي',
    'EXT6': 'ما عندي كلام كثير أقوله',
    'EXT7': 'أتحدث مع كثير من الناس في الحفلات',
    'EXT8': 'ما أحب ألفت الانتباه لنفسي',
    'EXT9': 'ما عندي مشكلة أكون مركز الانتباه',
    'EXT10': 'أكون ساكت حول الغرباء'
}

est_questions = {
    'EST1': 'أتوتر بسهولة',
    'EST2': 'أكون مرتاح أغلب الوقت',
    'EST3': 'أقلق بشأن الأشياء',
    'EST4': 'نادراً ما أشعر بالكآبة',
    'EST5': 'أتأثر بسهولة',
    'EST6': 'أنزعج بسهولة',
    'EST7': 'مزاجي يتغير كثير',
    'EST8': 'أعاني من تقلبات مزاجية كثيرة',
    'EST9': 'أغضب بسهولة',
    'EST10': 'أشعر بالكآبة كثيراً'
}

agr_questions = {
    'AGR1': 'ما أهتم كثير بالناس',
    'AGR2': 'أحب التعرف على الناس',
    'AGR3': 'أهين الناس بكلامي',
    'AGR4': 'أتعاطف مع مشاعر الآخرين',
    'AGR5': 'ما يهمني مشاكل الناس',
    'AGR6': 'قلبي طيب',
    'AGR7': 'ماني مهتم كثير بالناس',
    'AGR8': 'أخصص وقت للناس',
    'AGR9': 'أشعر بمشاعر الآخرين',
    'AGR10': 'أجعل الناس يشعرون بالراحة'
}

csn_questions = {
    'CSN1': 'أنا دايم مستعد',
    'CSN2': 'أخلي أغراضي مبعثرة',
    'CSN3': 'أنتبه للتفاصيل',
    'CSN4': 'أخرب الأمور',
    'CSN5': 'أنهي المهام على طول',
    'CSN6': 'أنسى أرجع الأشياء مكانها',
    'CSN7': 'أحب الترتيب',
    'CSN8': 'أتهرب من مسؤولياتي',
    'CSN9': 'ألتزم بجدولي',
    'CSN10': 'أكون دقيق جداً في شغلي'
}

opn_questions = {
    'OPN1': 'مفرداتي قوية وغنية',
    'OPN2': 'أواجه صعوبة في فهم الأفكار المجردة',
    'OPN3': 'خيالي واسع',
    'OPN4': 'ما أهتم بالأفكار المجردة',
    'OPN5': 'عندي أفكار ممتازة',
    'OPN6': 'خيالي مو قوي',
    'OPN7': 'أفهم الأمور بسرعة',
    'OPN8': 'أستخدم كلمات صعبة',
    'OPN9': 'أقضي وقت أفكر بالأشياء',
    'OPN10': 'دايم عندي أفكار جديدة'
}

# دمج وترتيب الأسئلة
all_questions = {**ext_questions, **est_questions, **agr_questions, **csn_questions, **opn_questions}
ordered_keys = sorted(all_questions.keys(), key=lambda x: (x[:3], int(x[3:])))
questions_ordered = {k: all_questions[k] for k in ordered_keys}

responses = {}
with st.form("form_full_50"):
    for key, question in questions_ordered.items():
        responses[key] = st.slider(f"{key}: {question}", 0, 5, 3, key=key)
    submitted = st.form_submit_button("احللني!")

if submitted:
    try:
        res = requests.post("http://127.0.0.1:8000/analyze_50", json=responses)

        if res.status_code == 200:
            result = res.json()

            st.success("✨ تم التحليل! وهذه النتيجة 👇")
            st.markdown(f"### الكلستر الخاص بك: `{result['cluster']}`")
            st.markdown(f"**{result['description']}**")

            st.markdown("### ملخص الأبعاد الخمسة:")
            trait_scores = result["scores"]
            summary_df = pd.DataFrame([trait_scores])
            st.dataframe(summary_df.style.format(precision=1), use_container_width=True)

            # رسم بياني بـ Plotly
            st.markdown("### تمثيل مرئي لأبعادك")
            traits = list(trait_scores.keys())
            values = [trait_scores[t] * 10 for t in traits]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=traits,
                y=values,
                name='درجاتك',
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