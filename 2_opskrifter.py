import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Opskrifter", layout="wide")

st.title("Opskriftsdatabase")

# Dummy-opskrifter (kan udvides med upload og database senere)
if "opskrifter" not in st.session_state:
    st.session_state.opskrifter = [
        {
            "navn": "Laks med blomkål og avocadosalsa",
            "billede": "images/laks_ret1.jpg",
            "ingredienser": [
                ("Laks", 200),
                ("Blomkål", 150),
                ("Avocado", 50)
            ]
        },
        {
            "navn": "Kyllingefrikadeller med grøntsager",
            "billede": "images/kylling_ret2.jpg",
            "ingredienser": [
                ("Hakket kyllingekød", 200),
                ("Broccoli", 100),
                ("Gulerødder", 80)
            ]
        }
    ]

# Hent ingrediensdata fra session_state
ingredienser_df = st.session_state.get("ingredienser", pd.DataFrame())

# Opskriftsvisning
selected = st.selectbox("Vælg en opskrift for detaljer:", [r["navn"] for r in st.session_state.opskrifter])

recipe = next((r for r in st.session_state.opskrifter if r["navn"] == selected), None)

if recipe:
    col1, col2 = st.columns([1, 2])

    with col1:
        if os.path.exists(recipe["billede"]):
            st.image(recipe["billede"], caption=recipe["navn"], use_column_width=True)
        else:
            st.warning("Billedet kunne ikke findes.")

    with col2:
        st.subheader("Ingredienser og mængder")
        total_kcal = total_prot = total_fedt = total_kulh = 0
        opskriftsdata = []

        for navn, mængde in recipe["ingredienser"]:
            match = ingredienser_df[ingredienser_df["Navn"] == navn]
            if not match.empty:
                data = match.iloc[0]
                faktor = mængde / 100
                kcal = data["Kalorier pr. 100g"] * faktor
                prot = data["Protein pr. 100g"] * faktor
                fedt = data["Fedt pr. 100g"] * faktor
                kulh = data["Kulhydrat pr. 100g"] * faktor

                total_kcal += kcal
                total_prot += prot
                total_fedt += fedt
                total_kulh += kulh

                opskriftsdata.append({
                    "Ingrediens": navn,
                    "Mængde (g)": mængde,
                    "Kcal": round(kcal),
                    "Protein": round(prot, 1),
                    "Fedt": round(fedt, 1),
                    "Kulhydrat": round(kulh, 1)
                })

        df = pd.DataFrame(opskriftsdata)
        st.dataframe(df)

        st.markdown("---")
        st.subheader("Opskriftens samlede makroer")
        st.metric("Kalorier", f"{round(total_kcal)} kcal")
        st.metric("Protein", f"{round(total_prot, 1)} g")
        st.metric("Fedt", f"{round(total_fedt, 1)} g")
        st.metric("Kulhydrat", f"{round(total_kulh, 1)} g")

        samlet_gram = sum([m for _, m in recipe["ingredienser"]])
        if samlet_gram > 0:
            st.markdown("---")
            st.subheader("Pr. 100 g")
            st.write(f"{round(total_kcal/samlet_gram*100)} kcal / {round(total_prot/samlet_gram*100, 1)} g protein / {round(total_fedt/samlet_gram*100, 1)} g fedt / {round(total_kulh/samlet_gram*100, 1)} g kulhydrat")
