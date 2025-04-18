import streamlit as st
from fpdf import FPDF
import base64
import io

st.set_page_config(page_title="Questionario Dieta Mediterranea - MDSS", layout="centered")
st.title("\U0001F35D Questionario di Aderenza alla Dieta Mediterranea (MDSS)")

st.write("""
Questo questionario valuta la tua aderenza alla Dieta Mediterranea secondo il punteggio **MDSS (Mediterranean Diet Serving Score)**.
""")

DOMANDE = [
    ("Frutta", "Quante porzioni di frutta consumi per pasto principale (colazione, pranzo e cena)", ["0", "1-2", "maggiore di 2"], "1-2", 3),
    ("Verdura", "Quante porzioni di verdura consumi per pasto principale (colazione, pranzo e cena)", ["2 o più", "meno di 2"], "2 o più", 3),
    ("Cereali", "Quante porzioni di cereali (pane, cereali per la colazione, riso e pasta) consumi per pasto principale", ["0", "1-2", "più di 2"], "1-2", 3),
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

if "calcolato" not in st.session_state:
    st.session_state.calcolato = False
if "salvataggio" not in st.session_state:
    st.session_state.salvataggio = None
if "codice" not in st.session_state:
    st.session_state.codice = ""

if not st.session_state.calcolato:
    sesso = st.radio("Seleziona il tuo sesso", ["Femmina", "Maschio"], horizontal=True, index=None, key="sesso")
    risposte = {}
    errori = []

    with st.form("questionario"):
        for idx, (key, testo, opzioni, _, _) in enumerate(DOMANDE, 1):
            st.markdown(f"**{idx}. {testo}**")
            risposte[key] = st.radio("", options=opzioni, key=key, index=None)
            st.markdown("---")

        st.markdown("**14. Quanti bicchieri di vino/birra bevi al giorno**")
        risposta_alcol = st.radio("", ["0", "1", "2", "più di 2"], key="Bevande alcoliche", index=None)
        st.markdown("---")
        invia = st.form_submit_button("Calcola Punteggio")

    if invia:
        punteggio = 0
        errori = []

        for idx, (key, _, _, corretto, punti) in enumerate(DOMANDE, 1):
            risposta = st.session_state.get(key)
            if risposta is None:
                errori.append((idx, key))
            elif risposta == corretto:
                punteggio += punti

        if st.session_state.get("Bevande alcoliche") is None:
            errori.append((14, "Bevande alcoliche"))
        else:
            if st.session_state["sesso"] == "Femmina" and st.session_state["Bevande alcoliche"] == "1":
                punteggio += 1
            elif st.session_state["sesso"] == "Maschio" and st.session_state["Bevande alcoliche"] == "2":
                punteggio += 1

        if errori:
            for idx, _ in errori:
                st.warning(f"Manca la risposta alla domanda n. {idx}")
        else:
            st.session_state.calcolato = True
            st.session_state.punteggio = punteggio

if st.session_state.calcolato:
    st.subheader("\U0001F4C8 Risultato")
    st.markdown(f"**Punteggio MDSS:** {st.session_state.punteggio} / 24")

    if st.session_state.punteggio <= 5:
        st.info("Bassa aderenza alla dieta mediterranea")
    elif st.session_state.punteggio <= 10:
        st.info("Media aderenza alla dieta mediterranea")
    else:
        st.info("Alta aderenza alla dieta mediterranea")

    st.caption("*Fonte: Mediterranean Diet Serving Score (Monteagudo et al., 2015)*")

    st.session_state.salvataggio = st.radio("Vuoi salvare il questionario?", ["Sì", "No"], index=None)

    if st.session_state.salvataggio == "No":
        st.session_state.clear()
        st.experimental_rerun()

    elif st.session_state.salvataggio == "Sì":
        st.session_state.codice = st.text_input("Assegna un codice a questa intervista")

        if st.session_state.codice and st.button("Salva"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Questionario di Aderenza alla Dieta Mediterranea (ADM)", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.ln(10)
            pdf.cell(0, 10, f"Codice intervista: {st.session_state['codice']}", ln=True)
            pdf.cell(0, 10, f"Sesso: {st.session_state['sesso']}", ln=True)
            pdf.ln(5)

            for idx, (key, testo, _, _, _) in enumerate(DOMANDE, 1):
                risposta = st.session_state.get(key, "Nessuna risposta")
                pdf.multi_cell(0, 10, f"{idx}. {testo}\nRisposta: {risposta}", align="L")
                pdf.ln(1)

            pdf.multi_cell(0, 10, f"14. Quanti bicchieri di vino/birra bevi al giorno\nRisposta: {st.session_state.get('Bevande alcoliche', 'Nessuna risposta')}", align="L")
            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"Punteggio MDSS: {st.session_state.punteggio} / 24", ln=True)
            pdf.ln(10)
            pdf.set_font("Arial", "I", 10)
            pdf.multi_cell(0, 10, "punteggio di aderenza alla dieta mediterranea (MDSS: Mediterranean Diet Serving Score) calcolato secondo Monteagudo et al (https://doi.org/10.1371/journal.pone.0128594) ed ottenuto tramite web app del dott. Giovanni Buonsanti - Matera")

            buffer = io.BytesIO()
            pdf.output(buffer)
            b64 = base64.b64encode(buffer.getvalue()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="MDSS_{st.session_state.codice}.pdf">📄 Scarica il PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
