import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
from sklearn.preprocessing import MinMaxScaler

# تحميل النموذج المدرب
k_fit = joblib.load('models/kmeans_model.pkl')

# وصف كل كلستر
cluster_descriptions = {
    0: "😌 ذا الواحد اللي عايش حياته على مود رايق. كل شيء عنده \"عادي\"، يقهوي نفسه الساعة ٥ العصر ويحوس بالبلانر يوم ويختفي سنة...",
    1: "🎭 ذا اللي قلبه ألين من خبز التنور. يبكي من إعلان زين ويكتب خواطر عن ذكرى منديل...",
    2: "📚 ذا اللي لو قلت له \"خل نروح الطايف\" قالك: \"طيب أرسل لي على الإيميل الخطة\"...",
    3: "🔕 ذا اللي تحسبه طالع من مسلسل كوري، بس هو ساكن في حي الربيع، بس ما أحد قد شافه...",
    4: "🎢 هذا بركان عواطف. يغير اهتماماته أسرع من عروض نون، وكل شوي يدخل هواية جديدة..."
}

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


# عنوان الموقع
st.markdown('<h1 style="color: black;">تحليل شخصيتك بطريقتنا الخاصة</h1>', unsafe_allow_html=True)

st.markdown("""
### هل عمرك حسّيت إنك كائن غريب؟
لا تشيل هم، احنا هنا نحلل شخصيتك ونطقطق عليها شوي (بحب طبعًا).

في هالموقع، ما راح نقول لك إنك "طموح ومبدع" وبس، لا لا...
راح نكشف لك الحقيقة كاملة: إنك مزاجي، تحب المفطّح، وتخاف من المشاعر 😌

جاوب على الأسئلة وخلّنا نبدأ حفلة التحليل ✨
""")

st.markdown("**اختر من 0 (لا أوافق أبدًا) إلى 5 (أوافق تمامًا)**")

# الأسئلة
ext_questions = {
    'EXT1': 'أنا جو الحفلة',
    'EXT2': "ما أسولف كثير",
    'EXT3': ' أكون مرتاح مع الناس',
    'EXT4': 'أكون في الخلفية وخلف الأضواء',
    'EXT5': 'أبادر وأبدأ السوالف',
    'EXT6': 'ما عندي كلام كثير أقوله',
    'EXT7': 'أسولف مع ناس كثير بالحفلات',
    'EXT8': "ما أحب ألفت الانتباه لنفسي",
    'EXT9': "ما عندي مشكلة أكون مركز الاهتمام",
    'EXT10': 'أكون ساكت مع الغرباء'
}

est_questions = {
    'EST1': 'أتوتر بسرعة',
    'EST2': 'أكون رايق أغلب الوقت',
    'EST3': 'أشيل هم الأشياء',
    'EST4': 'نادراً أحس بالكآبة',
    'EST5': 'أتأثر بسهولة',
    'EST6': 'أنقهر بسرعة',
    'EST7': 'مزاجي يتغير كثير',
    'EST8': 'دايم يتقلب مزاجي',
    'EST9': 'أعصب بسهولة',
    'EST10': 'غالباً أحس بالكآبة'
}

agr_questions = {
    'AGR1': 'ما أهتم بالناس كثير',
    'AGR2': 'أحب ومهتم أعرف عن الناس',
    'AGR3': 'أجرح الناس بكلامي',
    'AGR4': "أحس بمشاعر الناس",
    'AGR5': "ما تهمني مشاكل الناس",
    'AGR6': 'قلبي طيب',
    'AGR7': 'مب مرة أهتم بالناس',
    'AGR8': 'أخصص وقت للناس',
    'AGR9': "أحس بمشاعر غيري",
    'AGR10': 'الناس يحسون بالراحة معي'
}

csn_questions = {
    'CSN1': 'دايم مستعد وصامل',
    'CSN2': 'أغراضي مكركبة وحوسة',
    'CSN3': 'أركز على التفاصيل',
    'CSN4': 'أخرب الأمور',
    'CSN5': 'أخلص شغلي على طول',
    'CSN6': 'أنسى أرجع الأشياء مكانها',
    'CSN7': 'أحب الترتيب',
    'CSN8': 'أتهرب من شغلي',
    'CSN9': 'أمشي على جدول',
    'CSN10': 'أكون دقيق بشغلي'
}

opn_questions = {
    'OPN1': 'عندي محصول كلمات أعرف أستخدمه',
    'OPN2': 'ألقى صعوبة أفهم الأفكار العميقة',
    'OPN3': 'خيالي واسع',
    'OPN4': 'ما أحب الأفكار العميقة',
    'OPN5': 'عندي أفكار رهيبة',
    'OPN6': 'خيالي مو مرة قوي',
    'OPN7': 'أفهم الأمور بسرعة',
    'OPN8': 'أستخدم كلمات صعبة',
    'OPN9': 'أحب أقعد أفكر بالأشياء',
    'OPN10': 'دايم عندي أفكار جديدة'
}

# دمج وترتيب الأسئلة
all_questions = {**ext_questions, **est_questions, **agr_questions, **csn_questions, **opn_questions}
ordered_keys = sorted(all_questions.keys(), key=lambda x: (x[:3], int(x[3:])))
questions_ordered = {k: all_questions[k] for k in ordered_keys}

# واجهة المستخدم
responses = {}
with st.form("form_arabic"):
    for key, question in questions_ordered.items():
        responses[key] = st.slider(question, min_value=0, max_value=5, value=3, key=key)
    submitted = st.form_submit_button("احللني!")

if submitted:
    try:
        df = pd.DataFrame([responses])
        df = df[ordered_keys]

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler.fit(pd.DataFrame([[0]*50, [5]*50], columns=ordered_keys))
        scaled_df = scaler.transform(df)

        cluster = int(k_fit.predict(scaled_df)[0])
        cluster_description = cluster_descriptions.get(cluster, "🤷‍♂️ لا يوجد وصف لهذا الكلستر")

        trait_scores = {
            'extroversion': df[[f'EXT{i}' for i in range(1, 11)]].mean(axis=1).iloc[0],
            'neurotic': df[[f'EST{i}' for i in range(1, 11)]].mean(axis=1).iloc[0],
            'agreeable': df[[f'AGR{i}' for i in range(1, 11)]].mean(axis=1).iloc[0],
            'conscientious': df[[f'CSN{i}' for i in range(1, 11)]].mean(axis=1).iloc[0],
            'open': df[[f'OPN{i}' for i in range(1, 11)]].mean(axis=1).iloc[0],
        }

        st.success("✨ تم التحليل! وهذه النتيجة 👇")
        st.markdown(f"### الكلستر الخاص بك: `{cluster}`")
        st.markdown(f"**{cluster_description}**")

        st.markdown("### ملخص الأبعاد الخمسة:")
        summary_df = pd.DataFrame([trait_scores])
        st.dataframe(summary_df.style.format(precision=1), use_container_width=True)

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
            title=f"الكلستر رقم {cluster}",
            yaxis=dict(range=[0, 50]),
            xaxis_title="البُعد",
            yaxis_title="الدرجة (×10)",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ صار خطأ في التحليل: {e}")