from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

app = FastAPI()

# تحميل النموذج المدرب
model = joblib.load("../models/kmeans_small_model.pkl")

# وصف كل كلستر
cluster_descriptions = {
    0: "😌 ذا الواحد اللي عايش حياته على مود رايق. كل شيء عنده \"عادي\"، يقهوي نفسه الساعة ٥ العصر ويحوس بالبلانر يوم ويختفي سنة...",
    1: "🎭 ذا اللي قلبه ألين من خبز التنور. يبكي من إعلان زين ويكتب خواطر عن ذكرى منديل...",
    2: "📚 ذا اللي لو قلت له \"خل نروح الطايف\" قالك: \"طيب أرسل لي على الإيميل الخطة\"...",
    3: "🔕 ذا اللي تحسبه طالع من مسلسل كوري، بس هو ساكن في حي الربيع، بس ما أحد قد شافه...",
    4: "🎢 هذا بركان عواطف. يغير اهتماماته أسرع من عروض نون، وكل شوي يدخل هواية جديدة..."
}

# نموذج البيانات الواردة
class PersonalityRaw(BaseModel):
    EXT2: int
    EXT3: int
    EXT4: int
    EXT5: int
    EXT7: int
    EXT9: int
    EXT10: int
    EST6: int
    EST8: int
    AGR7: int
    OPN9: int
    CSN4: int

@app.post("/analyze")
def analyze(data: PersonalityRaw):
    raw = data.dict()
    input_df = pd.DataFrame([raw])

    # إنشاء MinMaxScaler بقيم min=0 و max=5
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(pd.DataFrame([[0]*12, [5]*12], columns=input_df.columns))  # نمرر القيم المتوقعة

    scaled_input = scaler.transform(input_df)

    # توقع الكلستر
    cluster = int(model.predict(scaled_input)[0])

    # وصف الكلستر
    description = cluster_descriptions.get(cluster, "🧩 ما عرفنا شخصيتك، بس أكيد فريدة من نوعها!")

    # حساب الأبعاد الخمسة من القيم الأصلية (لعرضها فقط)
    ext = ['EXT2', 'EXT3', 'EXT4', 'EXT5', 'EXT7', 'EXT9', 'EXT10']
    est = ['EST6', 'EST8']
    agr = ['AGR7']
    opn = ['OPN9']
    csn = ['CSN4']

    trait_scores = {
        'extroversion': round(input_df[ext].sum(axis=1).iloc[0] / len(ext), 2),
        'neurotic': round(input_df[est].sum(axis=1).iloc[0] / len(est), 2),
        'agreeable': round(input_df[agr].sum(axis=1).iloc[0] / len(agr), 2),
        'conscientious': round(input_df[csn].sum(axis=1).iloc[0] / len(csn), 2),
        'open': round(input_df[opn].sum(axis=1).iloc[0] / len(opn), 2)
    }

    return {
        "cluster": cluster,
        "description": description,
        "scores": trait_scores
    }