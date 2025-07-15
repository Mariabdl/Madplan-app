import streamlit as st
import pandas as pd
import os
import re
from PIL import Image
from difflib import get_close_matches

st.set_page_config(page_title="Opskrifter", layout="wide")

if "opskrifter" not in st.session_state:
    st.session_state.opskrifter = []
if "ingrediens_rækker" not in st.session_state:
    st.session_state.ingrediens_rækker = 1

# Hent ingrediensdatabase hvis tilgængelig
if "ingredienser" in st.session_state:
    ingrediens_df = st.session_state.ingredienser.copy()
    ingrediens_df["Navn_clean"] = ingrediens_df["Navn"].str.lower().str.strip()
    ingrediens_db = ingrediens_df["Navn"].tolist()
else:
    ingrediens_df = pd.DataFrame()
    ingrediens_db = []

# --- ØVERSTE LINJE MED SØG OG TILFØJ ---
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
                input_txt = st.text_input(f"Ingrediens {i+1}", key=f"ingrediens_input_{i}")
                forslag = get_close_matches(input_txt.strip().lower(), [n.lower() for n in ingrediens_db], n=5, cutoff=0.3)
                valgt_ingred = st.selectbox("Vælg fra forslag", forslag if forslag else [input_txt], key=f"forslag_{i}")
            with col2:
                mængde = st.number_input(f"Gram", key=f"g_{i}", min_value=0, step=10)
            if valgt_ingred:
                ingrediens_liste.append((valgt_ingred, mængde))

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
        if os.path.exists(opskrift["billede"]):
            st.image(opskrift["billede"], caption=opskrift["navn"], use_column_width=True)
        else:
            st.warning("Billedet kunne ikke vises.")
        if st.button(f"Se detaljer – {opskrift['navn']}", key=f"vis_{idx}"):
            st.session_state.valgt_opskrift = opskrift

# --- DETALJEVISNING ---
if "valgt_opskrift" in st.session_state:
    st.markdown("---")
    o = st.session_state.valgt_opskrift
    st.subheader(o["navn"])
    try:
        if os.path.exists(o["billede"]):
            st.image(o["billede"], use_column_width=True)
        else:
            st.warning("Billedet kunne ikke vises.")
    except:
        st.warning("Billedet kunne ikke vises.")

    st.write(f"**Kategori:** {o['kategori']}")
    df_ingredienser = pd.DataFrame(o["ingredienser"], columns=["Ingrediens", "Mængde (g)"])
    st.table(df_ingredienser)

    # --- Beregn makroer ---
    if not ingrediens_df.empty:
        df_ingredienser["Ingrediens_clean"] = df_ingredienser["Ingrediens"].str.lower().str.strip()
        merged = df_ingredienser.merge(
            ingrediens_df,
            how="left",
            left_on="Ingrediens_clean",
            right_on="Navn_clean"
        )
        missing = merged[merged["Navn"].isna()]
        if not missing.empty:
            st.warning("Følgende ingredienser findes ikke i databasen og er ikke med i beregningen:")
            st.write(missing["Ingrediens"].tolist())

        merged["Kalorier"] = merged["Mængde (g)"] * merged["Kalorier pr. 100g"] / 100
        merged["Protein"] = merged["Mængde (g)"] * merged["Protein pr. 100g"] / 100
        merged["Fedt"] = merged["Mængde (g)"] * merged["Fedt pr. 100g"] / 100
        merged["Kulhydrat"] = merged["Mængde (g)"] * merged["Kulhydrat pr. 100g"] / 100

        total = merged[["Kalorier", "Protein", "Fedt", "Kulhydrat"]].sum()
        samlet_vaegt = df_ingredienser["Mængde (g)"].sum()

        st.write("**Makroer (samlet):**")
        st.write(f"Kalorier: {total['Kalorier']:.0f} kcal")
        st.write(f"Protein: {total['Protein']:.1f} g")
        st.write(f"Fedt: {total['Fedt']:.1f} g")
        st.write(f"Kulhydrat: {total['Kulhydrat']:.1f} g")

        if samlet_vaegt > 0:
            st.write("**Makroer pr. 100g:**")
            st.write(f"Kalorier: {100 * total['Kalorier'] / samlet_vaegt:.0f} kcal")
            st.write(f"Protein: {100 * total['Protein'] / samlet_vaegt:.1f} g")
            st.write(f"Fedt: {100 * total['Fedt'] / samlet_vaegt:.1f} g")
            st.write(f"Kulhydrat: {100 * total['Kulhydrat'] / samlet_vaegt:.1f} g")

    if st.button("🔙 Tilbage"):
        del st.session_state.valgt_opskrift
