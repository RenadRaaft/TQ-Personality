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

# عنوان الموقع
st.title("تحليل شخصيتك بطريقتنا الخاصة")

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
    'EXT1': 'I am the life of the party',
    'EXT2': "I don't talk a lot",
    'EXT3': 'I feel comfortable around people',
    'EXT4': 'I keep in the background',
    'EXT5': 'I start conversations',
    'EXT6': 'I have little to say',
    'EXT7': 'I talk to a lot of different people at parties',
    'EXT8': "I don't like to draw attention to myself",
    'EXT9': "I don't mind being the center of attention",
    'EXT10': 'I am quiet around strangers'
}

est_questions = {
    'EST1': 'I get stressed out easily',
    'EST2': 'I am relaxed most of the time',
    'EST3': 'I worry about things',
    'EST4': 'I seldom feel blue',
    'EST5': 'I am easily disturbed',
    'EST6': 'I get upset easily',
    'EST7': 'I change my mood a lot',
    'EST8': 'I have frequent mood swings',
    'EST9': 'I get irritated easily',
    'EST10': 'I often feel blue'
}

agr_questions = {
    'AGR1': 'I feel little concern for others',
    'AGR2': 'I am interested in people',
    'AGR3': 'I insult people',
    'AGR4': "I sympathize with others' feelings",
    'AGR5': "I am not interested in other people's problems",
    'AGR6': 'I have a soft heart',
    'AGR7': 'I am not really interested in others',
    'AGR8': 'I take time out for others',
    'AGR9': "I feel others' emotions",
    'AGR10': 'I make people feel at ease'
}

csn_questions = {
    'CSN1': 'I am always prepared',
    'CSN2': 'I leave my belongings around',
    'CSN3': 'I pay attention to details',
    'CSN4': 'I make a mess of things',
    'CSN5': 'I get chores done right away',
    'CSN6': 'I often forget to put things back in their proper place',
    'CSN7': 'I like order',
    'CSN8': 'I shirk my duties',
    'CSN9': 'I follow a schedule',
    'CSN10': 'I am exacting in my work'
}

opn_questions = {
    'OPN1': 'I have a rich vocabulary',
    'OPN2': 'I have difficulty understanding abstract ideas',
    'OPN3': 'I have a vivid imagination',
    'OPN4': 'I am not interested in abstract ideas',
    'OPN5': 'I have excellent ideas',
    'OPN6': 'I do not have a good imagination',
    'OPN7': 'I am quick to understand things',
    'OPN8': 'I use difficult words',
    'OPN9': 'I spend time reflecting on things',
    'OPN10': 'I am full of ideas'
}

# دمج وترتيب الأسئلة
all_questions = {**ext_questions, **est_questions, **agr_questions, **csn_questions, **opn_questions}
ordered_keys = sorted(all_questions.keys(), key=lambda x: (x[:3], int(x[3:])))
questions_ordered = {k: all_questions[k] for k in ordered_keys}

# واجهة المستخدم
responses = {}
with st.form("form_full_arabic"):
    for key, question in questions_ordered.items():
        responses[key] = st.slider(f"{key}: {question}", min_value=0, max_value=5, value=3, key=key)
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