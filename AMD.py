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

st.header("\U0001F4CB Domande")

sesso = st.radio("Seleziona il tuo sesso", ["Femmina", "Maschio"], horizontal=True, index=None)

risposte = {}
errori = []

with st.form("questionario"):
    for idx, (key, testo, opzioni, corretto, punteggio) in enumerate(DOMANDE, 1):
        is_missing = key in [e[1] for e in errori]
        suffix = "<span style='color:red'> (risposta mancante)</span>" if is_missing else ""
        st.markdown(f"<div style='font-weight:bold; color:{'red' if is_missing else 'black'}'>{idx}. {testo}{suffix}</div>", unsafe_allow_html=True)
        risposta = st.radio("", options=opzioni, key=key, index=None)
        risposte[key] = risposta
        st.markdown("---")

    is_missing_alcol = "Bevande alcoliche" in [e[1] for e in errori]
    suffix_alcol = "<span style='color:red'> (risposta mancante)</span>" if is_missing_alcol else ""
    st.markdown(f"<div style='font-weight:bold; color:{'red' if is_missing_alcol else 'black'}'>14. Quanti bicchieri di vino/birra bevi al giorno{suffix_alcol}</div>", unsafe_allow_html=True)
    risposta_alcol = st.radio("", ["0", "1", "2", "più di 2"], key="Bevande alcoliche", index=None)
    st.markdown("---")
    invia = st.form_submit_button("Calcola Punteggio")

if invia:
    punteggio_totale = 0
    errori.clear()

    for idx, (key, _, _, corretto, punteggio) in enumerate(DOMANDE, 1):
        risposta = risposte.get(key)
        if risposta is None:
            errori.append((idx, key))
        elif isinstance(corretto, list):
            if risposta in corretto:
                punteggio_totale += punteggio
        else:
            if risposta == corretto:
                punteggio_totale += punteggio

    if risposta_alcol is None:
        errori.append((14, "Bevande alcoliche"))
    else:
        if (sesso == "Femmina" and risposta_alcol == "1"):
            punteggio_totale += 1
        elif (sesso == "Maschio" and risposta_alcol == "2"):
            punteggio_totale += 1

    st.subheader("\U0001F4C8 Risultato")

    if errori:
        for numero, _ in errori:
            st.warning(f"Manca la risposta alla domanda n. {numero}")
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

        salva = st.radio("Vuoi salvare il questionario?", ["Sì", "No"], index=None)

        if salva == "No":
            st.experimental_rerun()
        elif salva == "Sì":
            codice = st.text_input("Assegna un codice a questa intervista")
            if codice:
                if st.button("Salva"):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 14)
                    pdf.cell(0, 10, "Questionario di Aderenza alla Dieta Mediterranea (ADM)", ln=True, align="C")

                    pdf.set_font("Arial", "", 12)
                    pdf.ln(10)
                    pdf.cell(0, 10, f"Codice intervista: {codice}", ln=True)
                    pdf.cell(0, 10, f"Sesso: {sesso}", ln=True)
                    pdf.ln(5)

                    for idx, (key, testo, _, _, _) in enumerate(DOMANDE, 1):
                        risposta = risposte.get(key, "Nessuna risposta")
                        pdf.multi_cell(0, 10, f"{idx}. {testo}\nRisposta: {risposta}", align="L")
                        pdf.ln(1)

                    pdf.multi_cell(0, 10, f"14. Quanti bicchieri di vino/birra bevi al giorno\nRisposta: {risposta_alcol}", align="L")
                    pdf.ln(5)

                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, f"Punteggio MDSS: {punteggio_totale} / 24", ln=True)
                    pdf.ln(10)

                    pdf.set_font("Arial", "I", 10)
                    pdf.multi_cell(0, 10, "punteggio di aderenza alla dieta mediterranea (MDSS: Mediterranean Diet Serving Score) calcolato secondo Monteagudo et al (https://doi.org/10.1371/journal.pone.0128594) ed ottenuto tramite web app del dott. Giovanni Buonsanti - Matera")

                    buffer = io.BytesIO()
                    pdf.output(buffer)
                    b64 = base64.b64encode(buffer.getvalue()).decode()
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="MDSS_{codice}.pdf">📄 Scarica il PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
