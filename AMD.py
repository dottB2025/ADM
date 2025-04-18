import streamlit as st

st.set_page_config(page_title="Questionario Dieta Mediterranea - MDSS", layout="centered")
st.title("\U0001F35D Questionario di Aderenza alla Dieta Mediterranea (MDSS)")

st.write("""
Questo questionario valuta la tua aderenza alla Dieta Mediterranea secondo il punteggio **MDSS (Mediterranean Diet Serving Score)**.
""")

DOMANDE = [
    ("Frutta", "1. Quante porzioni di frutta consumi per pasto principale (colazione, pranzo e cena)", ["0", "1-2", "maggiore di 2"], "1-2", 3),
    ("Verdura", "2. Quante porzioni di verdura consumi per pasto principale (colazione, pranzo e cena)", ["2 o più", "meno di 2"], "2 o più", 3),
    ("Cereali", "3. Quante porzioni di cereali (pane, cereali per la colazione, riso e pasta) consumi per pasto principale", ["0", "1-2", "più di 2"], "1-2", 3),
    ("Patate", "Quante porzioni di patate consumi a settimana", ["3 o meno", "più di 3"], "3 o meno", 1),
    ("Olio d’oliva", "Usi olio d’oliva (su insalate, pane o per friggere) ad ogni pasto principale", ["Sì", "No"], "Sì", 3),
    ("Frutta secca", "Quante porzioni di frutta secca consumi al giorno", ["0", "1-2", "più di 2"], "1-2", 2),
    ("Latticini", "Quante porzioni di latticini (latte, yogurt, formaggio, gelato) consumi al giorno", ["1", "2", "più di 2"], "2", 2),
    ("Legumi", "Quante porzioni di legumi consumi a settimana", ["meno di 2", "2 o più"], "2 o più", 1),
    ("Uova", "Quante porzioni di uova consumi a settimana", ["meno di 2", "2-4", "4 o più"], "2-4", 1),
    ("Pesce", "Quante porzioni di pesce consumi a settimana", ["meno di due", "2 o più"], "2 o più", 1),
    ("Carne bianca", "Quante porzioni di carne bianca (pollame) consumi a settimana", ["meno di 2", "2", "più di 2"], "2", 1),
    ("Carne rossa", "Quante porzioni di carne rossa (maiale, manzo o agnello) consumi a settimana", ["meno di 2", "2 o più"], "meno di 2", 1),
    ("Dolci", "Quante porzioni di dolci (zucchero, caramelle, pasticcini, succhi zuccherati, bevande analcoliche) consumi a settimana", ["2 o meno", "più di 2"], "2 o meno", 1),
]

st.header("\U0001F4CB Domande")

sesso = st.radio("Seleziona il tuo sesso", ["Femmina", "Maschio"], horizontal=True, index=None)

risposte = {}
errori = []

with st.form("questionario"):
    for idx, (key, testo, opzioni, corretto, punteggio) in enumerate(DOMANDE, 1):
        is_missing = key in errori
        domanda = f"{idx}. {testo}{' (risposta mancante)' if is_missing else ''}"
        style_id = f"style_{key}"
        if is_missing:
            st.markdown(f"<style>#{style_id} > label {{ color: red !important; }}</style>", unsafe_allow_html=True)
        with st.container():
            risposta = st.radio(domanda, options=opzioni, key=key, index=None)
        risposte[key] = risposta

    is_missing_alcol = "Bevande alcoliche" in errori
    domanda_alcol = f"14. Quanti bicchieri di vino/birra bevi al giorno{' (risposta mancante)' if is_missing_alcol else ''}"
    if is_missing_alcol:
        st.markdown("<style>#style_Bevande > label { color: red !important; }</style>", unsafe_allow_html=True)
    risposta_alcol = st.radio(domanda_alcol, ["0", "1", "2", "più di 2"], key="Bevande alcoliche", index=None)

    invia = st.form_submit_button("Calcola Punteggio")

if invia:
    punteggio_totale = 0
    errori.clear()

    for idx, (key, _, _, corretto, punteggio) in enumerate(DOMANDE, 1):
        risposta = risposte.get(key)
        if risposta is None:
            errori.append(key)
        elif isinstance(corretto, list):
            if risposta in corretto:
                punteggio_totale += punteggio
        else:
            if risposta == corretto:
                punteggio_totale += punteggio

    if risposta_alcol is None:
        errori.append("Bevande alcoliche")
    else:
        if (sesso == "Femmina" and risposta_alcol == "1"):
            punteggio_totale += 1
        elif (sesso == "Maschio" and risposta_alcol == "2"):
            punteggio_totale += 1

    st.subheader("\U0001F4C8 Risultato")

    if errori:
        for idx, (key, _, _, _, _) in enumerate(DOMANDE, 1):
            if key in errori:
                st.warning(f"Manca la risposta alla domanda n. {idx}")
        if "Bevande alcoliche" in errori:
            st.warning("Manca la risposta alla domanda n. 14")
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
