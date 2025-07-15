import streamlit as st
import pandas as pd

# Udvidet initial ingrediensliste med kategorier (makrodata = estimeret standardværdier)
initial_ingredienser = [
    # Kød og animalske proteiner
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

    # Mejeriprodukter
    ("Ægte Parmigiano Reggiano fra Italien", "Mejeri", 390, 35, 28, 0),
    ("Ægte bøffelmozzarella fra Italien", "Mejeri", 280, 18, 23, 2),
    ("Ægte Græsk Yoghurt fra Grækenland øko 10%", "Mejeri", 120, 6, 10, 4),
    ("Halloumi", "Mejeri", 320, 20, 26, 2),
    ("Feta block", "Mejeri", 270, 14, 22, 1),
    ("Smør", "Mejeri", 720, 0, 80, 0),
    ("Skyr", "Mejeri", 60, 11, 0, 4),

    # Grøntsager
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
    ("Knoldselleri", "Grøntsag", 42, 1, 0, 9),
    ("Agurk", "Grøntsag", 15, 0, 0, 3),
    ("Bladselleri", "Grøntsag", 16, 1, 0, 3),
    ("Courgette", "Grøntsag", 17, 1, 0, 3),
    ("Squash", "Grøntsag", 17, 1, 0, 3),
    ("Grønne bønner", "Grøntsag", 31, 2, 0, 6),
    ("Ærter", "Grøntsag", 81, 5, 0, 14),
    ("Asparges", "Grøntsag", 20, 2, 0, 2),
    ("Svampe Shiitake", "Grøntsag", 34, 2, 0, 6),
    ("Svampe Portobello", "Grøntsag", 22, 2, 0, 3),
    ("Champignon", "Grøntsag", 22, 3, 0, 3),
    ("Løg", "Grøntsag", 40, 1, 0, 9),
    ("Rødløg", "Grøntsag", 42, 1, 0, 9),
    ("Tomater", "Grøntsag", 18, 1, 0, 3),
    ("Kartofler", "Grøntsag", 85, 2, 0, 17),
    ("Aubergine", "Grøntsag", 25, 1, 0, 5),

    # Frugter
    ("Blåbær", "Frugt", 57, 1, 0, 14),
    ("Jordbær", "Frugt", 32, 1, 0, 7),
    ("Hindbær", "Frugt", 52, 1, 0, 12),
    ("Brombær", "Frugt", 43, 1, 0, 10),
    ("Appelsiner", "Frugt", 47, 1, 0, 9),
    ("Citroner", "Frugt", 29, 1, 0, 3),
    ("Lime", "Frugt", 30, 0, 0, 3),
    ("Æbler", "Frugt", 52, 0, 0, 12),
    ("Pærer", "Frugt", 57, 0, 0, 15),
    ("Kiwi", "Frugt", 61, 1, 0, 15),
    ("Granatæble", "Frugt", 83, 1, 1, 19),
    ("Avocado", "Frugt", 160, 2, 15, 3),
    ("Druer", "Frugt", 69, 0, 0, 17),
    ("Mango", "Frugt", 60, 0, 0, 15),

    # Fuldkorn og kornprodukter
    ("Havregryn", "Korn", 370, 13, 7, 60),
    ("Quinoa", "Korn", 120, 4, 2, 21),
    ("Fuldkornshvede", "Korn", 340, 13, 2, 70),
    ("Speltmel", "Korn", 360, 12, 2, 72),
    ("Hvedemel", "Korn", 350, 11, 1, 74),
    ("Boghvedemel", "Korn", 340, 12, 2, 71),
    ("Rug", "Korn", 330, 11, 2, 66),
    ("Spaghetti", "Korn", 350, 12, 1, 72),
    ("Pasta", "Korn", 350, 12, 1, 72),
    ("Hvidt brød", "Korn", 265, 8, 3, 49),
    ("Bulgur", "Korn", 350, 12, 1, 72),

    # Bælgfrugter, nødder og frø
    ("Røde splitlinser", "Bælgfrugt", 340, 25, 1, 55),
    ("Grønne linser", "Bælgfrugt", 330, 24, 1, 53),
    ("Kikærter", "Bælgfrugt", 160, 9, 3, 27),
    ("Sorte bønner", "Bælgfrugt", 130, 9, 1, 23),
    ("Kidneybønner", "Bælgfrugt", 127, 9, 0, 22),
    ("Edamame", "Bælgfrugt", 121, 11, 5, 9),
    ("Mandler", "Nød", 580, 21, 50, 10),
    ("Hasselnødder", "Nød", 630, 15, 60, 10),
    ("Cashewnødder", "Nød", 550, 18, 44, 30),
    ("Pistacienødder", "Nød", 560, 20, 45, 28),
    ("Chiafrø", "Frø", 490, 16, 31, 8),
    ("Hørfrø", "Frø", 530, 18, 42, 10),
    ("Græskarkerner", "Frø", 570, 30, 45, 10),
    ("Sesamfrø", "Frø", 570, 20, 50, 12),
    ("Peanuts", "Nød", 560, 25, 48, 10),
    ("Peanutbutter", "Smør", 590, 25, 50, 10),
    ("Mandelsmør", "Smør", 620, 20, 55, 15),
    ("Cashewsmør", "Smør", 600, 20, 50, 20),

    # Fisk og skaldyr
    ("Laks", "Fisk", 210, 22, 15, 0),
    ("Makrel", "Fisk", 250, 20, 20, 0),
    ("Sild", "Fisk", 250, 18, 20, 0),
    ("Torsk", "Fisk", 85, 18, 1, 0),
    ("Fiskefilet", "Fisk", 180, 15, 10, 10),
    ("Mørksej", "Fisk", 95, 19, 1, 0),
    ("Rejer", "Fisk", 80, 18, 1, 0),
    ("Vannameirejer", "Fisk", 85, 17, 1, 0),
    ("Blåmuslinger", "Fisk", 120, 20, 3, 4),
    ("Krabber", "Fisk", 90, 19, 1, 0),

    # Sundt fedt
    ("Ekstra jomfru olivenolie", "Fedt", 900, 0, 100, 0),
    ("Avocadoolie", "Fedt", 900, 0, 100, 0),
    ("Kokosolie", "Fedt", 900, 0, 100, 0),
    ("Hørfrøolie", "Fedt", 900, 0, 100, 0),
    ("Nødder", "Fedt", 600, 20, 50, 15),
    ("Nøddeolier", "Fedt", 900, 0, 100, 0),
    ("Frø", "Fedt", 550, 20, 50, 15),
    ("MCT-olie", "Fedt", 900, 0, 100, 0),
    ("Kokosmælk", "Fedt", 180, 1, 18, 3),

    # Fermenterede og sylt
    ("Sauerkraut", "Fermenteret", 20, 1, 0, 3),
    ("Miso", "Fermenteret", 200, 12, 6, 25),
    ("Syltede rødløg", "Fermenteret", 60, 0, 0, 12),
    ("Syltede agurker", "Fermenteret", 20, 1, 0, 4),
    ("Syltede rødbeder", "Fermenteret", 50, 1, 0, 10),

    # Krydderier og urter
    ("Hvidløg", "Krydderi", 130, 6, 0, 28),
    ("Kanel", "Krydderi", 247, 4, 1, 81),
    ("Rosmarin", "Krydderi", 130, 3, 5, 20),
    ("Timian", "Krydderi", 101, 5, 2, 25),
    ("Oregano", "Krydderi", 265, 9, 4, 69),
    ("Basilikum", "Krydderi", 23, 3, 0, 2),
    ("Persille", "Krydderi", 36, 3, 1, 6),
    ("Mynte", "Krydderi", 44, 4, 1, 8),
    ("Salvie", "Krydderi", 315, 11, 13, 61),

    # Drikkevarer og diverse
    ("Vand", "Drik", 0, 0, 0, 0),
    ("Kaffe", "Drik", 2, 0, 0, 0),
    ("Rødvin", "Drik", 85, 0, 0, 2),
    ("Kamille-te", "Drik", 1, 0, 0, 0),
    ("Grøn te", "Drik", 1, 0, 0, 0),
    ("Urte-teer", "Drik", 1, 0, 0, 0),
    ("Honning", "Sødemiddel", 304, 0, 0, 82),
    ("Ahornsirup", "Sødemiddel", 260, 0, 0, 67),
    ("Tofu", "Diverse", 110, 12, 7, 1),
    ("Sojasauce", "Diverse", 50, 5, 0, 4),
    ("Dadler", "Diverse", 280, 2, 0, 75),
    ("Stevia", "Sødemiddel", 0, 0, 0, 0),
    ("Grov Hummus (Rema 1000)", "Diverse", 190, 6, 14, 12),
    ("Klar lagereddike", "Diverse", 15, 0, 0, 0),
    ("Gær", "Diverse", 300, 45, 7, 15),
    ("Proteinpulver", "Diverse", 370, 80, 5, 5),
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
    ingrediens_data = st.session_state.ingredienser[st.session_state.ingredienser["Navn"] == selected_ingredient
