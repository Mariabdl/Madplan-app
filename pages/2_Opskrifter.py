import streamlit as st
import pandas as pd
import os
import re
from PIL import Image

st.set_page_config(page_title="Opskrifter", layout="wide")

if "opskrifter" not in st.session_state:
    st.session_state.opskrifter = []
if "ingrediens_rækker" not in st.session_state:
    st.session_state.ingrediens_rækker = 1

# --- ØVERSTE LINJE MED SØG OG TILFØJ ---
st.markdown("""
    <style>
        .center-input .stTextInput > div > div > input {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    sog = st.text_input("", placeholder="🔍 Søg efter opskrift", label_visibility="collapsed")
with col3:
    if st.button("➕ Tilføj en opskrift"):
        st.session_state.vis_tilfoej_formular = not st.session_state.get("vis_tilfoej_formular", False)

# --- FORMULAR TIL AT TILFØJE OPSKRIFT ---
if st.session_state.get("vis_tilfoej_formular"):
    st.markdown("### Tilføj ny opskrift")

    with st.form("ny_opskrift_form"):
        navn = st.text_input("Navn på opskrift")
        kategori = st.selectbox("Vælg kategori", [
            "Fisk & Skaldyr", "Kødretter", "Vegetar/Vegansk",
            "Supper", "Brød & Rugbrød", "Morgenmad", "Mellemmåltid & Snacks"
        ])
        billede = st.file_uploader("Upload billede", type=["jpg", "jpeg", "png"])

        st.write("Ingredienser og mængder")
        ingrediens_liste = []

        for i in range(st.session_state.ingrediens_rækker):
            col1, col2 = st.columns([3, 1])
            with col1:
                ingrediens = st.text_input(f"Ingrediens {i+1}", key=f"ing_{i}")
            with col2:
                mængde = st.number_input(f"Gram", key=f"g_{i}", min_value=0, step=10)
            if ingrediens:
                ingrediens_liste.append((ingrediens, mængde))

        gem_opskrift = st.form_submit_button("Gem opskrift")

        if gem_opskrift and navn and kategori and ingrediens_liste:
            billede_path = "images/default.jpg"
            if billede is not None:
                os.makedirs("images", exist_ok=True)
                safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', navn.lower())
                billede_path = f"images/{safe_name}.jpg"
                with open(billede_path, "wb") as f:
                    f.write(billede.getbuffer())

            ny_opskrift = {
                "navn": navn,
                "kategori": kategori,
                "billede": billede_path,
                "ingredienser": ingrediens_liste
            }
            st.session_state.opskrifter.append(ny_opskrift)
            st.success("Opskrift tilføjet!")
            st.session_state.vis_tilfoej_formular = False
            st.session_state.ingrediens_rækker = 1

    if st.button("➕ Tilføj ingrediensrække"):
        st.session_state.ingrediens_rækker += 1

st.markdown("---")

# --- KATEGORIFILTER SOM BILLEDER ---
kategorier = [
    "Fisk & Skaldyr", "Kødretter", "Vegetar/Vegansk",
    "Supper", "Brød & Rugbrød", "Morgenmad", "Mellemmåltid & Snacks"
]

kat_cols = st.columns(len(kategorier))
for i, kat in enumerate(kategorier):
    with kat_cols[i]:
        if st.button(kat):
            st.session_state.kategori_filter = kat

# --- OPSKRIFTOVERSIGT ---
filtered = st.session_state.opskrifter
if "kategori_filter" in st.session_state:
    filtered = [o for o in filtered if o["kategori"] == st.session_state.kategori_filter]
if sog:
    filtered = [o for o in filtered if sog.lower() in o["navn"].lower()]

# --- GRID MED OPSKRIFTER ---
cols = st.columns(4)
for idx, opskrift in enumerate(filtered):
    with cols[idx % 4]:
        try:
            st.image(opskrift["billede"], caption=opskrift["navn"], use_column_width=True)
        except:
            st.warning("Billedet kunne ikke vises.")
        if st.button(f"Se detaljer – {opskrift['navn']}", key=f"vis_{idx}"):
            st.session_state.valgt_opskrift = opskrift

# --- DETALJEVISNING ---
if "valgt_opskrift" in st.session_state:
    st.markdown("---")
    o = st.session_state.valgt_opskrift
    st.subheader(o["navn"])
    st.image(o["billede"], use_column_width=True)
    st.write(f"**Kategori:** {o['kategori']}")

    df_ingredienser = pd.DataFrame(o["ingredienser"], columns=["Ingrediens", "Mængde (g)"])
    st.table(df_ingredienser)

    if st.button("🔙 Tilbage"):
        del st.session_state.valgt_opskrift
