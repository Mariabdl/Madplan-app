import streamlit as st
import pandas as pd

# Udvidet initial ingrediensliste med kategorier (makrodata = estimeret standardværdier)
initial_ingredienser = [
    ("Økologiske frie æg", "Kød/Æg", 143, 13, 10, 1),
    ("Bacon Fedtreduceret", "Kød/Æg", 250, 20, 20, 1),
    ("Hamburgerryg", "Kød/Æg", 110, 22, 2, 0),
    ("Hakket oksekød 4-7%", "Kød/Æg", 140, 20, 5, 0),
    ("Hakket kyllingekød", "Kød/Æg", 120, 22, 4, 0),
    ("Kyllingebryst", "Kød/Æg", 105, 23, 1, 0),
    ("Kylling inderfilet", "Kød/Æg", 105, 23, 1, 0),
    ("Flæskesteg", "Kød/Æg", 250, 18, 20, 0),
    ("Serranoskinke", "Kød/Æg", 180, 25, 8, 0),
    ("Mortadella", "Kød/Æg", 300, 15, 28, 1),
    ("Pepperoni", "Kød/Æg", 450, 20, 40, 1),
    ("Ægte Parmigiano Reggiano fra Italien", "Mejeri", 390, 35, 28, 0),
    ("Ægte bøffelmozzarella fra Italien", "Mejeri", 280, 18, 23, 2),
    ("Ægte Græsk Yoghurt fra Grækenland øko 10%", "Mejeri", 120, 6, 10, 4),
    ("Halloumi", "Mejeri", 320, 20, 26, 2),
    ("Feta block", "Mejeri", 270, 14, 22, 1),
    ("Smør", "Mejeri", 720, 0, 80, 0),
    ("Skyr", "Mejeri", 60, 11, 0, 4),
    ("Spinat", "Grøntsag", 25, 3, 0, 1),
    ("Grønkål", "Grøntsag", 35, 3, 1, 4),
    ("Rucola", "Grøntsag", 30, 3, 1, 3),
    ("Broccoli", "Grøntsag", 34, 3, 0, 5),
    ("Blomkål", "Grøntsag", 30, 3, 0, 5),
    ("Rødkål", "Grøntsag", 28, 1, 0, 6),
    ("Gulerødder", "Grøntsag", 40, 1, 0, 8),
    ("Rødbeder", "Grøntsag", 43, 1, 0, 9),
    ("Pastinakker", "Grøntsag", 75, 1, 0, 17),
    ("Sød kartoffel", "Grøntsag", 86, 2, 0, 20),
    ("Jordskokker", "Grøntsag", 73, 2, 0, 17),
    ("Pastinak", "Grøntsag", 75, 1, 0, 17),
    ("Knoldselleri", "Grøntsag", 42, 1, 0, 9),
    ("Agurk", "Grøntsag", 15, 0, 0, 3),
    ("Bladselleri", "Grøntsag", 16, 1, 0, 3),
    ("Courgette", "Grøntsag", 17, 1, 0, 3),
    ("Squash", "Grøntsag", 17, 1, 0, 3),
    ("Grønne bønner", "Grøntsag", 31, 2, 0, 6),
    ("Ærter", "Grøntsag", 81, 5, 0, 14),
    ("Asparges", "Grøntsag", 20, 2, 0, 2),
    ("Champignon", "Grøntsag", 22, 3, 0, 3),
    ("Løg", "Grøntsag", 40, 1, 0, 9),
    ("Rødløg", "Grøntsag", 42, 1, 0, 9),
    ("Tomater", "Grøntsag", 18, 1, 0, 3),
    ("Kartofler", "Grøntsag", 85, 2, 0, 17),
    ("Aubergine", "Grøntsag", 25, 1, 0, 5),
    ("Blåbær", "Frugt", 57, 1, 0, 14),
    ("Jordbær", "Frugt", 32, 1, 0, 7),
    ("Hindbær", "Frugt", 52, 1, 0, 12),
    ("Avocado", "Frugt", 160, 2, 15, 3),
    ("Havregryn", "Korn", 370, 13, 7, 60),
    ("Quinoa", "Korn", 120, 4, 2, 21),
    ("Spaghetti", "Korn", 350, 12, 1, 72),
    ("Pasta", "Korn", 350, 12, 1, 72),
    ("Bulgur", "Korn", 350, 12, 1, 72),
    ("Røde splitlinser", "Bælgfrugt", 340, 25, 1, 55),
    ("Grønne linser", "Bælgfrugt", 330, 24, 1, 53),
    ("Kikærter", "Bælgfrugt", 160, 9, 3, 27),
    ("Sorte bønner", "Bælgfrugt", 130, 9, 1, 23),
    ("Kidneybønner", "Bælgfrugt", 127, 9, 0, 22),
    ("Edamame", "Bælgfrugt", 121, 11, 5, 9),
    ("Mandler", "Nød", 580, 21, 50, 10),
    ("Cashewnødder", "Nød", 550, 18, 44, 30),
    ("Peanutbutter", "Smør", 590, 25, 50, 10),
    ("Laks", "Fisk", 210, 22, 15, 0),
    ("Torsk", "Fisk", 85, 18, 1, 0),
    ("Rejer", "Fisk", 80, 18, 1, 0),
    ("Vannameirejer", "Fisk", 85, 17, 1, 0),
    ("Olivenolie", "Fedt", 900, 0, 100, 0),
    ("Avocadoolie", "Fedt", 900, 0, 100, 0),
    ("Kokosolie", "Fedt", 900, 0, 100, 0),
    ("Kokosmælk", "Fedt", 180, 1, 18, 3),
    ("Sauerkraut", "Fermenteret", 20, 1, 0, 3),
    ("Miso", "Fermenteret", 200, 12, 6, 25),
    ("Syltede rødløg", "Fermenteret", 60, 0, 0, 12),
    ("Syltede agurker", "Fermenteret", 20, 1, 0, 4),
    ("Syltede rødbeder", "Fermenteret", 50, 1, 0, 10),
    ("Hvidløg", "Krydderi", 130, 6, 0, 28),
    ("Honning", "Sødemiddel", 304, 0, 0, 82),
    ("Ahornsirup", "Sødemiddel", 260, 0, 0, 67),
    ("Tofu", "Diverse", 110, 12, 7, 1),
    ("Sojasauce", "Diverse", 50, 5, 0, 4),
    ("Dadler", "Diverse", 280, 2, 0, 75),
    ("Stevia", "Sødemiddel", 0, 0, 0, 0),
    ("Grov Hummus (Rema 1000)", "Diverse", 190, 6, 14, 12),
    ("Klar lagereddike", "Diverse", 15, 0, 0, 0),
    ("Gær", "Diverse", 300, 45, 7, 15),
    ("Proteinpulver", "Diverse", 370, 80, 5, 5)
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
