# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from PIL import Image

# Load your trained model
k_fit = joblib.load('models/kmeans_model.pkl')

# Define question groups
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

# Combine all questions
all_questions = {**ext_questions, **est_questions, **agr_questions, **csn_questions, **opn_questions}

# Sort keys to maintain order
ordered_keys = sorted(all_questions.keys(), key=lambda x: (x[:3], int(x[3:])))
questions_ordered = {k: all_questions[k] for k in ordered_keys}

st.set_page_config(page_title="Personality Cluster Test", layout="wide")
st.title("🧠 Personality Cluster Predictor")
st.write("Please answer the following questions on a scale from 0 (Strongly Disagree) to 5 (Strongly Agree).")

responses = {}

# Input form
with st.form("personality_form"):
    for key, question in questions_ordered.items():
        responses[key] = st.slider(f"{key}: {question}", 0, 5, 3)
    submitted = st.form_submit_button("Submit")

if submitted:
    df = pd.DataFrame([responses])

    correct_columns = [
        'EXT1', 'EXT2', 'EXT3', 'EXT4', 'EXT5', 'EXT6', 'EXT7', 'EXT8', 'EXT9', 'EXT10',
        'EST1', 'EST2', 'EST3', 'EST4', 'EST5', 'EST6', 'EST7', 'EST8', 'EST9', 'EST10',
        'AGR1', 'AGR2', 'AGR3', 'AGR4', 'AGR5', 'AGR6', 'AGR7', 'AGR8', 'AGR9', 'AGR10',
        'CSN1', 'CSN2', 'CSN3', 'CSN4', 'CSN5', 'CSN6', 'CSN7', 'CSN8', 'CSN9', 'CSN10',
        'OPN1', 'OPN2', 'OPN3', 'OPN4', 'OPN5', 'OPN6', 'OPN7', 'OPN8', 'OPN9', 'OPN10'
    ]

    df = df[correct_columns]  # Ensure exact order before predicting

    # Predict cluster
    cluster = k_fit.predict(df)[0]

    # Define groups
    col_list = list(df.columns)
    ext = col_list[0:10]
    est = col_list[10:20]
    agr = col_list[20:30]
    csn = col_list[30:40]
    opn = col_list[40:50]

    # Compute trait scores
    trait_scores = {
        'extroversion': df[ext].sum(axis=1).iloc[0] / 10,
        'neurotic': df[est].sum(axis=1).iloc[0] / 10,
        'agreeable': df[agr].sum(axis=1).iloc[0] / 10,
        'conscientious': df[csn].sum(axis=1).iloc[0] / 10,
        'open': df[opn].sum(axis=1).iloc[0] / 10
    }

    # Show predicted cluster
    st.subheader(f"🎯 You belong to **Cluster {cluster}**")

    # Show summary table
    trait_scores["cluster"] = cluster
    summary_df = pd.DataFrame([trait_scores])
    st.write("### Sum of Your Question Groups")
    st.dataframe(summary_df.style.format(precision=1), use_container_width=True)

    # Chart
    st.write("### Visual Summary of Your Traits")
    fig, ax = plt.subplots()
    traits = list(trait_scores.keys())[:-1]  # Exclude cluster
    values = [trait_scores[t] * 10 for t in traits]

    ax.bar(traits, values, color='green', alpha=0.2)
    ax.plot(traits, values, color='red', marker='o')
    ax.set_ylim(0, 40)
    ax.set_title(f"Cluster {cluster}")
    plt.xticks(rotation=45)

    st.pyplot(fig)