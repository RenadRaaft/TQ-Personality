from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI()


model = joblib.load("../models/kmeans_model.pkl")  #استنى وريف ترسله

# أوصاف الكلسترات
cluster_descriptions = {
    0: "😌",
    1: "🎭",
    2: "📚",
    3: "🔕",
    4: "🎢"
}


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

  
    extroversion = sum([raw[q] for q in ['EXT2', 'EXT3', 'EXT4', 'EXT5', 'EXT7', 'EXT9', 'EXT10']]) / 7
    neurotic = sum([raw[q] for q in ['EST6', 'EST8']]) / 2
    agreeable = raw['AGR7'] / 1
    conscientious = raw['CSN4'] / 1
    openness = raw['OPN9'] / 1

    input_df = pd.DataFrame([{
        'extroversion': extroversion,
        'neurotic': neurotic,
        'agreeable': agreeable,
        'conscientious': conscientious,
        'open': openness
    }])


    cluster = int(model.predict(input_df)[0])
    description = cluster_descriptions.get(cluster, "🧩 ما عرفنا شخصيتك، بس أكيد فريدة من نوعها!")

    return {
        "cluster": cluster,
        "description": description,
        "scores": {
            "extroversion": round(extroversion, 2),
            "neurotic": round(neurotic, 2),
            "agreeable": round(agreeable, 2),
            "conscientious": round(conscientious, 2),
            "open": round(openness, 2)
        }
    }
