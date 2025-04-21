import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os
from collections import Counter

# تحميل نموذج KMeans
k_fit = joblib.load('models/kmeans_model.pkl')

# تعريف جميع مجموعات الأسئلة
question_groups = {
    "EXT": ['He/She is the life of the party', "He/She doesn't talk a lot", 'He/She feels comfortable around people',
            'He/She keeps in the background', 'He/She starts conversations', 'He/She has little to say',
            'He/She talks to a lot of different people at parties', "He/She doesn't like to draw attention to himself/herself",
            "He/She doesn't mind being the center of attention", 'He/She is quiet around strangers'],

    "EST": ['He/She gets stressed out easily', 'He/She is relaxed most of the time', 'He/She worries about things',
            'He/She seldom feels blue', 'He/She is easily disturbed', 'He/She gets upset easily', 'He/She changes his/her mood a lot',
            'He/She has frequent mood swings', 'He/She gets irritated easily', 'He/She often feels blue'],

    "AGR": ['He/She feels little concern for others', 'He/She is interested in people', 'He/She insults people',
            "He/She sympathizes with others' feelings", "He/She is not interested in other people's problems",
            'He/She has a soft heart', 'He/She is not really interested in others', 'He/She takes time out for others',
            "He/She feels others' emotions", 'He/She makes people feel at ease'],

    "CSN": ['He/She is always prepared', 'He/She leaves his/her belongings around', 'He/She pays attention to details',
            'He/She makes a mess of things', 'He/She gets chores done right away', 'He/She often forgets to put things back in their proper place',
            'He/She likes order', 'He/She shirks his/her duties', 'He/She follows a schedule', 'He/She is exacting in his/her work'],

    "OPN": ['He/She has a rich vocabulary', 'He/She has difficulty understanding abstract ideas', 'He/She has a vivid imagination',
            'He/She is not interested in abstract ideas', 'He/She has excellent ideas', 'He/She does not have a good imagination',
            'He/She is quick to understand things', 'He/She uses difficult words', 'He/She spends time reflecting on things', 'He/She is full of ideas']
}

# إنشاء قائمة الأسئلة
all_questions = {}
for trait, questions in question_groups.items():
    for i, q in enumerate(questions, start=1):
        all_questions[f"{trait}{i}"] = q

# ترتيب الأسئلة
ordered_keys = sorted(all_questions.keys(), key=lambda x: (x[:3], int(x[3:])))
questions_ordered = {k: all_questions[k] for k in ordered_keys}

# مسار ملف CSV
CSV_FILE = "personality_votes.csv"

# واجهة ستريملت
st.set_page_config(page_title="تصنيف الشخصيات حسب آراء الآخرين", layout="wide")
st.title("👥 تطبيق تصنيف الشخصية حسب تقييم الزملاء")

st.markdown("يتم تقييم كل شخص بواسطة الآخرين. يعرض النظام متوسط درجات السمات وتوقع الانتماء لأحد المجموعات.")

# قائمة الأسماء
names = [
    "وسن عبدالهادي العتيبي", "عبدالعزيز فهد الحيزان", "أزهار سعود التميمي", "عبدالمحسن عادل الدغيم",
    "عمر سليمان السريع", "غادة عبدالرحمن العمري", "عبدالله عمر الدايل", "رهف عمر مسلمي",
    "رناد عبدالرحمن الحجي", "يوسف سعد الديحاني", "مهند إبراهيم أبوالسنون", "الهنوف عبدالمحسن السويد",
    "مجد عبدالله العتيبي", "عبدالله أحمد الزهراني", "فيصل فهد الخنين", "فراس حمد السويد",
    "دانية عماد الدبيسي", "فيصل عبدالله آل مفرح", "نجلاء باسم المرشدي", "محمد عبدالله الحسيني",
    "عبدالعزيز خالد عبدالعزيز آل فريان", "ريناد رأفت ياسين", "مروان فهد الهندي", "وريف عبدالله اليوسف",
    "عبدالعزيز سعد الخرجي"
]

# ========== 1. نموذج الإدخال ==========
st.subheader("✍️ أدخل تقييمك")

with st.form("submit_form"):
    target_person_name = st.selectbox("👤 من الشخص الذي تقوم بتقييمه؟", names, key="target")
    rater_name = st.selectbox("🧑 من أنت (المُقيّم)؟", names, key="rater")

    responses = {}
    for key, question in questions_ordered.items():
        responses[key] = st.slider(f"{key}: {question}", 0, 5, 3)

    submitted = st.form_submit_button("إرسال التقييم")

# ========== 2. حفظ التقييم ==========
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

# ========== 3. تحليل شخصية ==========
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

        # توقع المجموعة (Cluster)
        cluster_votes = []
        for _, row in df_person.iterrows():
            X = row[ordered_keys].values.reshape(1, -1)
            predicted_cluster = k_fit.predict(X)[0]
            cluster_votes.append(predicted_cluster)

        most_common_cluster = Counter(cluster_votes).most_common(1)[0][0]

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

        # رسم بياني
        st.write("### 🧬 تصور السمات")
        fig, ax = plt.subplots()
        bars = [v * 10 for v in trait_averages.values()]
        labels = list(trait_names.values())

        ax.bar(labels, bars, alpha=0.2, color="blue")
        ax.plot(labels, bars, color="red", marker="o")
        ax.set_ylim(0, 50)
        ax.set_ylabel("الدرجة (0 - 50)")
        ax.set_title(f"المجموعة {most_common_cluster} للشخص: {person_to_analyze}")
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    st.warning("📝 لم يتم إدخال أي تقييمات بعد.")