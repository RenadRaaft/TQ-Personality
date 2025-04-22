import streamlit as st
import pandas as pd
import joblib
import os
from collections import Counter
import plotly.graph_objects as go

# تحميل نموذج KMeans
k_fit = joblib.load('models/kmeans_model.pkl')

st.set_page_config(page_title="تصنيف الشخصيات حسب آراء الآخرين", layout="wide")

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

# وصف كل كلستر
cluster_descriptions = {
    0: "😌 ذا الواحد اللي عايش حياته على مود رايق. كل شيء عنده \"عادي\"، يقهوي نفسه الساعة ٥ العصر ويحوس بالبلانر يوم ويختفي سنة...",
    1: "🎭 ذا اللي قلبه ألين من خبز التنور. يبكي من إعلان زين ويكتب خواطر عن ذكرى منديل...",
    2: "📚 ذا اللي لو قلت له \"خل نروح الطايف\" قالك: \"طيب أرسل لي على الإيميل الخطة\"...",
    3: "🔕 ذا اللي تحسبه طالع من مسلسل كوري، بس هو ساكن في حي الربيع، بس ما أحد قد شافه...",
    4: "🎢 هذا بركان عواطف. يغير اهتماماته أسرع من عروض نون، وكل شوي يدخل هواية جديدة..."
}

# تعريف جميع مجموعات الأسئلة
question_groups = {
    "EXT": [
        'هو/هي جو الحفلة',
        "هو/هي ما يسولف كثير",
        'هو/هي يكون مرتاح مع الناس',
        'هو/هي يكون في الخلفية وخلف الأضواء',
        'هو/هي يبادر ويبدأ السوالف',
        'هو/هي ما عنده/عندها كلام كثير يقوله',
        'هو/هي يسولف مع ناس كثير بالحفلات',
        "هو/هي ما يحب يلفت الانتباه لنفسه/لنفسها",
        "هو/هي ما عنده/عندها مشكلة يكون مركز الاهتمام",
        'هو/هي يكون ساكت مع الغرباء'
    ],
    "EST": [
        'هو/هي يتوتر بسرعة',
        'هو/هي يكون رايق أغلب الوقت',
        'هو/هي يشيل هم الأشياء',
        'هو/هي نادراً يحس بالكآبة',
        'هو/هي يتأثر بسهولة',
        'هو/هي ينقهر بسرعة',
        'هو/هي مزاجه يتغير كثير',
        'هو/هي دايم يتقلب مزاجه',
        'هو/هي يعصب بسهولة',
        'هو/هي غالباً يحس بالكآبة'
    ],
    "AGR": [
        'هو/هي ما يهتم بالناس كثير',
        'هو/هي يحب ومهتم يعرف عن الناس',
        'هو/هي يجرح الناس بكلامه',
        "هو/هي يحس بمشاعر الناس",
        "هو/هي ما تهمه مشاكل الناس",
        'هو/هي قلبه طيب',
        'هو/هي مب مرة يهتم بالناس',
        'هو/هي يخصص وقت للناس',
        "هو/هي يحس بمشاعر غيره",
        'الناس يحسون بالراحة معه/معها'
    ],
    "CSN": [
        'هو/هي دايم مستعد وصامل',
        'هو/هي أغراضه مكركبة وحوسة',
        'هو/هي يركز على التفاصيل',
        'هو/هي يخرب الأمور',
        'هو/هي يخلص شغله على طول',
        'هو/هي ينسى يرجع الأشياء مكانها',
        'هو/هي يحب الترتيب',
        'هو/هي يتهرب من شغله',
        'هو/هي يمشي على جدول',
        'هو/هي يكون دقيق بشغله'
    ],
    "OPN": [
        'هو/هي عنده محصول كلمات يعرف يستخدمه',
        'هو/هي يلقى صعوبة يفهم الأفكار العميقة',
        'هو/هي خياله واسع',
        'هو/هي ما يحب الأفكار العميقة',
        'هو/هي عنده أفكار رهيبة',
        'هو/هي خياله مو مرة قوي',
        'هو/هي يفهم الأمور بسرعة',
        'هو/هي يستخدم كلمات صعبة',
        'هو/هي يحب يقعد يفكر بالأشياء',
        'هو/هي دايم عنده أفكار جديدة'
    ]
}

# إنشاء قائمة الأسئلة
all_questions = {}
for trait, questions in question_groups.items():
    for i, q in enumerate(questions, start=1):
        all_questions[f"{trait}{i}"] = q

# ترتيب الأسئلة
ordered_keys = sorted(all_questions.keys(), key=lambda x: (x[:3], int(x[3:])))
questions_ordered = {k: all_questions[k] for k in ordered_keys}

# ملف التصويتات
CSV_FILE = "personality_votes.csv"

# إعداد الواجهة
st.title("👥 تطبيق تصنيف الشخصية حسب تقييم الزملاء")

st.markdown("يتم تقييم كل شخص بواسطة الآخرين. يعرض النظام متوسط درجات السمات وتوقع الانتماء لأحد المجموعات.")

# الأسماء
names = [
    "وسن عبدالهادي العتيبي", "عبدالعزيز فهد الحيزان", "أزهار سعود التميمي", "عبدالمحسن عادل الدغيم",
    "عمر سليمان السريع", "غادة عبدالرحمن العمري", "عبدالله عمر الدايل", "رهف عمر مسلمي",
    "رناد عبدالرحمن الحجي", "يوسف سعد الديحاني", "مهند إبراهيم أبوالسنون", "الهنوف عبدالمحسن السويد",
    "مجد عبدالله العتيبي", "عبدالله أحمد الزهراني", "فيصل فهد الخنين", "فراس حمد السويد",
    "دانية عماد الدبيسي", "فيصل عبدالله آل مفرح", "نجلاء باسم المرشدي", "محمد عبدالله الحسيني",
    "عبدالعزيز خالد عبدالعزيز آل فريان", "ريناد رأفت ياسين", "مروان فهد الهندي", "وريف عبدالله اليوسف",
    "عبدالعزيز سعد الخرجي"
]

# ========== 1. الإدخال ==========
st.subheader("✍️ أدخل تقييمك")

with st.form("submit_form"):
    target_person_name = st.selectbox("👤 من الشخص الذي تقوم بتقييمه؟", names, key="target")
    rater_name = st.selectbox("🧑 من أنت (المُقيّم)؟", names, key="rater")

    responses = {}
    for key, question in questions_ordered.items():
        responses[key] = st.slider(question, min_value=0, max_value=5, value=3, key=key)

    submitted = st.form_submit_button("إرسال التقييم")

if submitted:
    new_row = {
        "target_person_name": target_person_name,
        "rater_name": rater_name,
        **responses
    }

    df_new = pd.DataFrame([new_row])
    if os.path.exists(CSV_FILE):
        df_existing = pd.read_csv(CSV_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(CSV_FILE, index=False)
    st.success(f"✅ تم تسجيل تقييمك لـ {target_person_name} بنجاح!")

# ========== 2. التحليل ==========
st.subheader("📊 تحليل شخصية")

person_to_analyze = st.selectbox("اختر شخصًا لتحليل شخصيته", names, key="analysis")

if os.path.exists(CSV_FILE):
    df_all = pd.read_csv(CSV_FILE)
    df_person = df_all[df_all["target_person_name"] == person_to_analyze]

    if df_person.empty:
        st.info("لا يوجد تقييمات لهذا الشخص بعد.")
    else:
        trait_averages = {}

        for trait in question_groups.keys():
            cols = [f"{trait}{i}" for i in range(1, 11)]
            df_trait = df_person[cols]
            avg_per_rater = df_trait.mean(axis=1)
            total_avg = avg_per_rater.mean()
            trait_averages[trait] = total_avg

        # توقع المجموعة
        cluster_votes = []
        for _, row in df_person.iterrows():
            X = row[ordered_keys].values.reshape(1, -1)
            predicted_cluster = k_fit.predict(X)[0]
            cluster_votes.append(predicted_cluster)

        most_common_cluster = Counter(cluster_votes).most_common(1)[0][0]
        cluster_description = cluster_descriptions.get(most_common_cluster, "🧩 لا يوجد وصف متاح لهذا الكلستر")

        # عرض النتائج
        st.write("### 🌟 متوسط السمات من جميع المقيمين")
        trait_names = {
            "EXT": "الانبساطية",
            "EST": "العصبية",
            "AGR": "التوافق",
            "CSN": "الضمير الحي",
            "OPN": "الانفتاح"
        }

        summary_data = {trait_names[k]: round(v, 2) for k, v in trait_averages.items()}
        summary_data["المجموعة المتوقعة"] = most_common_cluster
        summary_df = pd.DataFrame([summary_data])
        st.dataframe(summary_df, use_container_width=True)

        st.markdown(f"### 🧠 وصف الكلستر `{most_common_cluster}`:")
        st.markdown(f"**{cluster_description}**")

        # رسم بياني
        st.write("### 🧬 تصور السمات")
        bars = [v * 10 for v in trait_averages.values()]
        labels = list(trait_names.values())

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=labels,
            y=bars,
            name='السمات',
            marker_color='lightblue',
            opacity=0.6
        ))
        fig.add_trace(go.Scatter(
            x=labels,
            y=bars,
            mode='lines+markers',
            name='معدل السمة',
            line=dict(color='red'),
            marker=dict(size=10)
        ))
        fig.update_layout(
            title=f"المجموعة {most_common_cluster} للشخص: {person_to_analyze}",
            xaxis_title="السمة",
            yaxis_title="الدرجة (0 - 50)",
            yaxis=dict(range=[0, 50]),
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("📝 لم يتم إدخال أي تقييمات بعد.")