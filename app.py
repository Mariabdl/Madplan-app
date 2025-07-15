import streamlit as st
import pandas as pd

# Udvidet initial ingrediensliste med kategorier (makrodata = estimeret standardværdier)
initial_ingredienser = [
    # ... (samme som før - beholdt intakt)
]

# Initialiser session state
if "ingredienser" not in st.session_state or st.session_state.ingredienser.empty:
    st.session_state.ingredienser = pd.DataFrame(initial_ingredienser, columns=[
        "Navn", "Kategori", "Kalorier pr. 100g", "Protein pr. 100g",
        "Fedt pr. 100g", "Kulhydrat pr. 100g"
    ])

st.title("Ingrediensdatabase - Madplan App")

st.subheader("Tilføj eller redigér ingrediens")
med_navne = st.session_state.ingredienser["Navn"].tolist()
selected_ingredient = st.selectbox("Vælg ingrediens for redigering eller ny", [""] + med_navne)

if selected_ingredient and selected_ingredient in med_navne:
    ingrediens_data = st.session_state.ingredienser[st.session_state.ingredienser["Navn"] == selected_ingredient].iloc[0]

    navn = st.text_input("Navn", ingrediens_data["Navn"])
    kategori = st.text_input("Kategori", ingrediens_data["Kategori"])
    kalorier = st.number_input("Kalorier pr. 100g", value=ingrediens_data["Kalorier pr. 100g"])
    protein = st.number_input("Protein pr. 100g", value=ingrediens_data["Protein pr. 100g"])
    fedt = st.number_input("Fedt pr. 100g", value=ingrediens_data["Fedt pr. 100g"])
    kulhydrat = st.number_input("Kulhydrat pr. 100g", value=ingrediens_data["Kulhydrat pr. 100g"])

    if st.button("Opdater ingrediens"):
        st.session_state.ingredienser.loc[st.session_state.ingredienser["Navn"] == selected_ingredient] = [
            navn, kategori, kalorier, protein, fedt, kulhydrat
        ]
        st.success("Ingrediens opdateret!")

else:
    navn = st.text_input("Navn")
    kategori = st.text_input("Kategori")
    kalorier = st.number_input("Kalorier pr. 100g", value=0)
    protein = st.number_input("Protein pr. 100g", value=0)
    fedt = st.number_input("Fedt pr. 100g", value=0)
    kulhydrat = st.number_input("Kulhydrat pr. 100g", value=0)

    if st.button("Tilføj ny ingrediens") and navn:
        ny = pd.DataFrame([[navn, kategori, kalorier, protein, fedt, kulhydrat]], columns=st.session_state.ingredienser.columns)
        st.session_state.ingredienser = pd.concat([st.session_state.ingredienser, ny], ignore_index=True)
        st.success("Ingrediens tilføjet!")

st.subheader("Ingrediensoversigt")
st.dataframe(st.session_state.ingredienser.sort_values("Navn").reset_index(drop=True))
