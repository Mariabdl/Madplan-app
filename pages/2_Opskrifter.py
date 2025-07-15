import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Opskrifter", layout="wide")

st.title("Opskriftsdatabase")

# --- FORM TIL AT TILFØJE NY OPSKRIFT ---
st.markdown("### ➕ Tilføj ny opskrift")
with st.form("ny_opskrift_form"):
    navn = st.text_input("Navn på opskrift")
    kategori = st.selectbox("Vælg kategori", [
        "Fisk & Skaldyr", "Kødretter", "Vegetar / Vegansk",
        "Supper", "Brød & Rugbrød", "Morgenmad", "Mellemmåltid/snack"
    ])
    billede = st.file_uploader("Upload billede", type=["jpg", "jpeg", "png"])
    ingredienser_input = st.text_area("Ingredienser og mængder (fx Laks:200, Broccoli:100)")
    gem_opskrift = st.form_submit_button("Gem opskrift")

    if gem_opskrift and navn and kategori and ingredienser_input:
        opskrift_ingredienser = []
        for linje in ingredienser_input.split(","):
            try:
                navn_m, gram = linje.strip().split(":")
                opskrift_ingredienser.append((navn_m.strip(), int(gram.strip())))
            except:
                st.warning(f"Kunne ikke forstå linje: '{linje}'")

        billede_path = "images/default.jpg"
        if billede is not None:
            os.makedirs("images", exist_ok=True)
            billede_path = f"images/{navn.replace(' ', '_').lower()}.jpg"
            with open(billede_path, "wb") as f:
                f.write(billede.getbuffer())

        ny_opskrift = {
            "navn": navn,
            "kategori": kategori,
            "billede": billede_path,
            "ingredienser": opskrift_ingredienser
        }
        st.session_state.opskrifter.append(ny_opskrift)
        st.success("Opskrift tilføjet!")

st.markdown("---")

# --- OPSKRIFTSOVERSIGT ---
st.subheader("📚 Gennemse opskrifter")
selected_kategori = st.selectbox("Vælg kategori", ["Alle"] + sorted(list(set([o["kategori"] for o in st.session_state.opskrifter]))))

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

viste = 0
for idx, opskrift in enumerate(st.session_state.opskrifter):
    if selected_kategori != "Alle" and opskrift["kategori"] != selected_kategori:
        continue

    with cols[viste % 3]:
        st.image(opskrift["billede"], caption=opskrift["navn"], use_column_width=True)
        if st.button(f"Se detaljer – {opskrift['navn']}"):
            st.session_state.valgt_opskrift = opskrift
    viste += 1

# --- DETALJEVISNING AF OPSKRIFT ---
if "valgt_opskrift" in st.session_state:
    st.markdown("---")
    st.subheader(st.session_state.valgt_opskrift["navn"])
    st.image(st.session_state.valgt_opskrift["billede"], use_column_width=True)
    st.write(f"**Kategori:** {st.session_state.valgt_opskrift['kategori']}")

    st.subheader("Ingredienser")
    df_ingredienser = pd.DataFrame(st.session_state.valgt_opskrift["ingredienser"], columns=["Ingrediens", "Mængde (g)"])
    st.table(df_ingredienser)

    ingredienser_df = st.session_state.get("ingredienser", pd.DataFrame())
    if not ingredienser_df.empty:
        total_kcal = total_prot = total_fedt = total_kulh = 0
        for navn, mængde in st.session_state.valgt_opskrift["ingredienser"]:
            match = ingredienser_df[ingredienser_df["Navn"] == navn]
            if not match.empty:
                row = match.iloc[0]
                faktor = mængde / 100
                total_kcal += row["Kalorier pr. 100g"] * faktor
                total_prot += row["Protein pr. 100g"] * faktor
                total_fedt += row["Fedt pr. 100g"] * faktor
                total_kulh += row["Kulhydrat pr. 100g"] * faktor

        st.markdown("---")
        st.subheader("Makroer for hele retten")
        st.metric("Kalorier", f"{round(total_kcal)} kcal")
        st.metric("Protein", f"{round(total_prot, 1)} g")
        st.metric("Fedt", f"{round(total_fedt, 1)} g")
        st.metric("Kulhydrat", f"{round(total_kulh, 1)} g")

        total_gram = sum([m for _, m in st.session_state.valgt_opskrift["ingredienser"]])
        if total_gram > 0:
            st.subheader("Makroer pr. 100g")
            st.write(f"{round(total_kcal/total_gram*100)} kcal / {round(total_prot/total_gram*100,1)} g protein / {round(total_fedt/total_gram*100,1)} g fedt / {round(total_kulh/total_gram*100,1)} g kulhydrat")
