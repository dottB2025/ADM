import streamlit as st

st.set_page_config(page_title="Questionario Dieta Mediterranea - MDSS", layout="centered")
st.title("\U0001F35D Questionario di Aderenza alla Dieta Mediterranea (MDSS)")

st.write("""
Questo questionario valuta la tua aderenza alla Dieta Mediterranea secondo il punteggio **MDSS (Mediterranean Diet Serving Score)**.
""")

DOMANDE = [
    ("Frutta", "Quante porzioni di frutta consumi per pasto principale (colazione, pranzo e cena)?", ["0", "1-2", "maggiore di 2"], "1-2", 3),
    ("Verdura", "Quante porzioni di verdura consumi per pasto principale (colazione, pranzo e cena)?", ["2 o più", "meno di 2"], "2 o più", 3),
    ("Cereali", "Quante porzioni di cereali (pane, cereali per la colazione, riso e pasta) consumi per pasto principale?", ["0", "1-2", "più di 2"], "1-2", 3),
    ("Patate", "Quante porzioni di patate consumi a settimana?", ["3 o meno", "più di 3"], "3 o meno", 1),
    ("Olio d’oliva", "Usi olio d’oliva (su insalate, pane o per friggere) ad ogni pasto principale?", ["Sì", "No"], "Sì", 3),
    ("Frutta secca", "Quante porzioni di frutta secca consumi al giorno?", ["0", "1-2", "più di 2"], "1-2", 2),
    ("Latticini", "Quante porzioni di latticini (latte, yogurt, formaggio, gelato) consumi al giorno?", ["1", "2", "più di 2"], "2", 2),
    ("Legumi", "Quante porzioni di legumi consumi a settimana?", ["meno di 2", "2 o più"], "2 o più", 1),
    ("Uova", "Quante porzioni di uova consumi a settimana?", ["meno di 2", "2-4", "4 o più"], "2-4", 1),
    ("Pesce", "Quante porzioni di pesce consumi a settimana?", ["meno di due", "2 o più"], "2 o più", 1),
    ("Carne bianca", "Quante porzioni di carne bianca (pollame) consumi a settimana?", ["meno di 2", "2", "più di 2"], "2", 1),
    ("Carne rossa", "Quante porzioni di carne rossa (maiale, manzo o agnello) consumi a settimana?", ["meno di 2", "2 o più"], "meno di 2", 1),
    ("Dolci", "Quante porzioni di dolci (zucchero, caramelle, pasticcini, succhi zuccherati, bevande analcoliche) consumi a settimana?", ["2 o meno", "più di 2"], "2 o meno", 1),
]

st.header("\U0001F4CB Domande")

sesso = st.radio("Seleziona il tuo sesso:", ["Femmina", "Maschio"], horizontal=True)

risposte = {}
errori = []

with st.form("questionario"):
    for idx, (key, testo, opzioni, corretto, punteggio) in enumerate(DOMANDE, 1):
        risposta = st.radio(
            f"{idx}. {testo}",
            options=opzioni,
            key=key,
            index=None,
            help="Seleziona una risposta"
        )
        risposte[key] = risposta
    risposta_alcol = st.radio("Quanti bicchieri di vino/birra bevi al giorno?", ["0", "1", "2", "più di 2"], key="Bevande alcoliche", index=None)
    invia = st.form_submit_button("Calcola Punteggio")

if invia:
    punteggio_totale = 0
    errori.clear()

    for idx, (key, _, _, corretto, punteggio) in enumerate(DOMANDE, 1):
        risposta = risposte.get(key)
        if risposta is None:
            errori.append(idx)
        elif isinstance(corretto, list):
            if risposta in corretto:
                punteggio_totale += punteggio
        else:
            if risposta == corretto:
                punteggio_totale += punteggio

    if risposta_alcol is None:
        errori.append("bevande fermentate")
    else:
        if (sesso == "Femmina" and risposta_alcol == "1"):
            punteggio_totale += 1
        elif (sesso == "Maschio" and risposta_alcol == "2"):
            punteggio_totale += 1

    st.subheader("\U0001F4C8 Risultato")

    if errori:
        for idx in errori:
            if isinstance(idx, int):
                st.warning(f"Manca la risposta alla domanda n. {idx}")
            else:
                st.warning("Manca la risposta alla domanda su vino/birra")
    else:
        st.markdown(f"**Punteggio MDSS:** {punteggio_totale} / 24")

        if punteggio_totale <= 5:
            livello = "Bassa aderenza alla dieta mediterranea"
        elif punteggio_totale <= 10:
            livello = "Media aderenza alla dieta mediterranea"
        else:
            livello = "Alta aderenza alla dieta mediterranea"

        st.info(f"**{livello}**")

    st.caption("*Fonte: Mediterranean Diet Serving Score (Monteagudo et al., 2015)*")

    if errori:
        st.markdown("""
        <style>
        div[data-testid="stRadio"] > label {
            color: red !important;
        }
        </style>
        """, unsafe_allow_html=True)
