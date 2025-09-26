import streamlit as st
import requests
import spacy

# -----------------------------
# 1. Setup
# -----------------------------
API_KEY = "244fbebdb4ab45aab252b694ccfdf045"
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# 2. Functions
# -----------------------------
def fetch_ingredients(query, number=10):
    url = f"https://api.spoonacular.com/food/ingredients/autocomplete?query={query}&number={number}&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return [item["name"] for item in response.json()]
    else:
        return []

def rank_ingredients(user_input, candidates):
    user_vec = nlp(user_input)
    ranked = []
    for ing in candidates:
        ing_vec = nlp(ing)
        similarity = user_vec.similarity(ing_vec)
        ranked.append((ing, similarity))
    ranked.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in ranked]

def predict_related_ingredients(user_input):
    candidates = fetch_ingredients(user_input, number=20)
    if not candidates:
        return ["No related ingredients found"]
    ranked_ingredients = rank_ingredients(user_input, candidates)
    return ranked_ingredients[:5]  # return top 5

# -----------------------------
# 3. Streamlit Frontend
# -----------------------------
st.set_page_config(page_title="Ingredient Predictor", page_icon="🍴")

st.title("🍴 Ingredient Predictor")
st.write("Type an ingredient or dish and get related ingredients using NLP & Spoonacular API.")

# Input
user_input = st.text_input("Enter an ingredient or dish:", "")

if st.button("🔍 Predict Related Ingredients"):
    if user_input.strip():
        with st.spinner("Fetching related ingredients..."):
            predictions = predict_related_ingredients(user_input)
        st.success("Here are your top related ingredients:")
        for i, p in enumerate(predictions, 1):
            st.write(f"**{i}. {p}**")
    else:
        st.warning("Please enter an ingredient or dish.")
