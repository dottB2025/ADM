import streamlit as st

st.set_page_config(page_title="Questionario Dieta Mediterranea - MDSS", layout="centered")
st.title("\U0001F35D Questionario di Aderenza alla Dieta Mediterranea (MDSS)")

st.write("""
Questo questionario valuta la tua aderenza alla Dieta Mediterranea secondo il punteggio **MDSS (Mediterranean Diet Serving Score)**.
""")

# Lista delle domande con le opzioni e la logica di punteggio
DOMANDE = [
    ("Frutta", "Quante porzioni di frutta consumi per pasto principale (colazione, pranzo e cena)?", ["0", "1", "2 o più"], "2 o più", 3),
    ("Verdura", "Quante porzioni di verdura consumi per pasto principale (colazione, pranzo e cena)?", ["0", "1", "2 o più"], "2 o più", 3),
    ("Cereali", "Quante porzioni di cereali (pane, cereali per la colazione, riso e pasta) consumi per pasto principale?", ["0", "1", "2 o più"], "2 o più", 3),
    ("Patate", "Quante porzioni di patate consumi a settimana?", [">3", "3 o meno"], "3 o meno", 1),
    ("Olio d’oliva", "Usi olio d’oliva (su insalate, pane o per friggere) ad ogni pasto principale?", ["Sì", "No"], "Sì", 3),
    ("Frutta secca", "Quante porzioni di frutta secca consumi al giorno?", ["0", "1", "2 o più"], ["1", "2 o più"], 2),
    ("Latticini", "Quante porzioni di latticini (latte, yogurt, formaggio, gelato) consumi al giorno?", ["0", "1", "2 o più"], "2 o più", 2),
    ("Legumi", "Quante porzioni di legumi consumi a settimana?", ["<2", "2 o più"], "2 o più", 1),
    ("Uova", "Quante porzioni di uova consumi a settimana?", ["<2", "2-4", ">4"], "2-4", 1),
    ("Pesce", "Quante porzioni di pesce consumi a settimana?", ["<2", "2 o più"], "2 o più", 1),
    ("Carne bianca", "Quante porzioni di carne bianca (pollame) consumi a settimana?", ["<2", "2 o più"], "2 o più", 1),
    ("Carne rossa", "Quante porzioni di carne rossa (maiale, manzo o agnello) consumi a settimana?", [">=2", "<2"], "<2", 1),
    ("Dolci", "Quante porzioni di dolci (zucchero, caramelle, pasticcini, succhi zuccherati, bevande analcoliche) consumi a settimana?", [">2", "≤2"], "≤2", 1),
    ("Bevande alcoliche", "Quante unità di bevande fermentate (vino o birra) consumi al giorno?", ["0", "1-2", ">2"], "1-2", 1),
]

risposte = {}

st.header("\U0001F4CB Domande")

# Form
with st.form("questionario"):
    for key, testo, opzioni, corretto, punteggio in DOMANDE:
        risposta = st.radio(testo, opzioni, key=key)
        risposte[key] = risposta
    invia = st.form_submit_button("Calcola Punteggio")

if invia:
    punteggio_totale = 0

    for key, testo, opzioni, corretto, punteggio in DOMANDE:
        risposta = risposte[key]
        if isinstance(corretto, list):
            if risposta in corretto:
                punteggio_totale += punteggio
        else:
            if risposta == corretto:
                punteggio_totale += punteggio

    st.subheader("\U0001F4C8 Risultato")
    st.markdown(f"**Punteggio MDSS:** {punteggio_totale} / 24")

    if punteggio_totale <= 5:
        livello = "Bassa aderenza alla dieta mediterranea"
    elif punteggio_totale <= 10:
        livello = "Media aderenza alla dieta mediterranea"
    else:
        livello = "Alta aderenza alla dieta mediterranea"

    st.info(f"**{livello}**")

    st.caption("*Fonte: Mediterranean Diet Serving Score (Monteagudo et al., 2015)*")
