# Big Five Personality Test Clustring Prediction!

This project implements a personality test based on the Big Five personality traits. It uses machine learning to cluster users into personality groups and provides an interactive interface for users to analyze their personality traits.

## :clipboard: Table of Contents
1. [Team Members](#team-members)
2. [About the Project](#about-the-project)
3. [Features](#features)
4. [Technologies Used](#technologies-used)
5. [Data Source](#data-source)
6. [Installation](#installation)
7. [Usage](#usage)

## Team Members:
- Marwan Alhindi
- Abdulaziz Alfrayan
- Renad Raaft Yassin
- Waref Alyousef
- Mohammad Alhusini

## :book: About the Project

The Big Five Personality Test is a psychological assessment tool that evaluates individuals based on five key traits: Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism. This project provides:
- A *Streamlit-based frontend* for users to take personality tests.
- A *FastAPI backend* for processing responses and clustering users into personality groups using machine learning models.

## :sparkles: Features

- *Quick Personality Test*: A short test for users to get a quick overview of their personality.
- *Full Personality Test*: A comprehensive test with 50 questions for detailed analysis.
- *Peer Evaluation*: Allows users to evaluate others and see how they are perceived.
- *Interactive Visualizations*: Displays personality trait scores and clustering results using Plotly.
- *Machine Learning Integration*: Uses KMeans clustering to group users based on their responses.


## :tools: Technologies Used

- *Frontend*: Streamlit
- *Backend*: FastAPI
- *Machine Learning*: Scikit-learn
- *Visualization*: Plotly
- *Data Handling*: Pandas
- *Deployment*: Render

## :bar_chart: Data Source
- The dataset used in this project is sourced from [Kaggle](https://www.kaggle.com/datasets/tunguz/big-five-personality-test). It was collected between 2016 and 2018 through an interactive online personality test. The test was constructed using the "Big-Five Factor Markers" from the [IPIP](https://ipip.ori.org/newBigFive5broadKey.htm).


### Key Details:
- *Scale*: Each question was rated on a five-point scale:
  - 1 = Disagree
  - 3 = Neutral
  - 5 = Agree
- *Questions*: The dataset includes 50 questions, 10 for each personality trait:
  - *Extraversion (EXT)*: e.g., "I am the life of the party."
  - *Agreeableness (AGR)*: e.g., "I feel little concern for others."
  - *Conscientiousness (CSN)*: e.g., "I am always prepared."
  - *Neuroticism (EST)*: e.g., "I get stressed out easily."
  - *Openness (OPN)*: e.g., "I have a rich vocabulary."
- *Additional Features*:
  - Time spent on each question (in milliseconds).
  - User's screen dimensions (screenw, screenh).
  - Timestamps for survey start and completion.
  - User's country and approximate latitude/longitude.

## :rocket: Installation

1. Clone the repository:
   bash
   git clone [repository_url]
   cd TQ-Personality

2. Install dependencies for both client and server:
    bash
    pip install -r personalitytest.client/requirements.txt
    pip install -r personalitytest.server/api/requirements.txt

3. Run the backend server:
    bash
    cd personalitytest.server/api
    python main.py

4. Ru the frontend application:
    bash
    cd personalitytest.client
    streamlit run !مرحبا.py

## :book: Usage
1. Open the frontend application in your browser.
2. Choose between:
    - Quick Personality Test
    - Full Personality Test
    - Peer Evaluation
4. Answer the questions and submit your responses.
5. View your personality cluster and trait analysis.
