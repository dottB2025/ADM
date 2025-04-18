import streamlit as st import base64 import io import csv

st.set_page_config(page_title="Questionario Dieta Mediterranea - MDSS", layout="centered") st.title("\U0001F35D Questionario di Aderenza alla Dieta Mediterranea (MDSS)")

st.write(""" Questo questionario valuta la tua aderenza alla Dieta Mediterranea secondo il punteggio MDSS (Mediterranean Diet Serving Score). """)

DOMANDE = [ ("Frutta", "Quante porzioni di frutta consumi per pasto principale (colazione, pranzo e cena)", ["0", "1-2", "maggiore di 2"], "1-2", 3), ("Verdura", "Quante porzioni di verdura consumi per pasto principale (colazione, pranzo e cena)", ["2 o più", "meno di 2"], "2 o più", 3), ("Cereali", "Quante porzioni di cereali (pane, cereali per la colazione, riso e pasta) consumi per pasto principale", ["0", "1-2", "più di 2"], "1-2", 3), ("Patate", "Quante porzioni di patate consumi a settimana", ["3 o meno", "più di 3"], "3 o meno", 1), ("Olio d’oliva", "Usi olio d’oliva (su insalate, pane o per friggere) ad ogni pasto principale", ["Sì", "No"], "Sì", 3), ("Frutta secca", "Quante porzioni di frutta secca consumi al giorno", ["0", "1-2", "più di 2"], "1-2", 2), ("Latticini", "Quante porzioni di latticini (latte, yogurt, formaggio, gelato) consumi al giorno", ["1", "2", "più di 2"], "2", 2), ("Legumi", "Quante porzioni di legumi consumi a settimana", ["meno di 2", "2 o più"], "2 o più", 1), ("Uova", "Quante porzioni di uova consumi a settimana", ["meno di 2", "2-4", "4 o più"], "2-4", 1), ("Pesce", "Quante porzioni di pesce consumi a settimana", ["meno di due", "2 o più"], "2 o più", 1), ("Carne bianca", "Quante porzioni di carne bianca (pollame) consumi a settimana", ["meno di 2", "2", "più di 2"], "2", 1), ("Carne rossa", "Quante porzioni di carne rossa (maiale, manzo o agnello) consumi a settimana", ["meno di 2", "2 o più"], "meno di 2", 1), ("Dolci", "Quante porzioni di dolci (zucchero, caramelle, pasticcini, succhi zuccherati, bevande analcoliche) consumi a settimana", ["2 o meno", "più di 2"], "2 o meno", 1), ]

if "calcolato" not in st.session_state: st.session_state.calcolato = False if "codice" not in st.session_state: st.session_state.codice = ""

if not st.session_state.calcolato: genere = st.radio("Seleziona il tuo genere", ["Femmina", "Maschio"], horizontal=True, index=None) errori = []

with st.form("questionario"):
    risposte = {}
    for idx, (key, testo, opzioni, _, _) in enumerate(DOMANDE, 1):
        st.markdown(f"**{idx}. {testo}**")
        valore = st.radio("", options=opzioni, key=f"form_{key}", index=None)
        risposte[key] = valore
        st.markdown("---")

    st.markdown("**14. Quanti bicchieri di vino/birra bevi al giorno**")
    valore_alcol = st.radio("", ["0", "1", "2", "più di 2"], key="form_Bevande", index=None)
    st.markdown("---")
    invia = st.form_submit_button("Calcola Punteggio")

if invia:
    if genere is None:
        st.warning("È obbligatorio selezionare il genere")
    else:
        st.session_state["genere"] = genere
        punteggio = 0
        errori = []

        for idx, (key, _, _, corretto, punti) in enumerate(DOMANDE, 1):
            risposta = risposte.get(key)
            if risposta is None:
                errori.append((idx, key))
            else:
                st.session_state[key] = risposta
                if risposta == corretto:
                    punteggio += punti

        if valore_alcol is None:
            errori.append((14, "Bevande alcoliche"))
        else:
            st.session_state["Bevande alcoliche"] = valore_alcol
            if st.session_state["genere"] == "Femmina" and valore_alcol == "1":
                punteggio += 1
            elif st.session_state["genere"] == "Maschio" and valore_alcol == "2":
                punteggio += 1

        if errori:
            for idx, _ in errori:
                st.warning(f"Manca la risposta alla domanda n. {idx}")
        else:
            st.session_state.calcolato = True
            st.session_state.punteggio = punteggio

if st.session_state.calcolato: st.subheader("\U0001F4C8 Risultato") st.markdown(f"Punteggio MDSS: {st.session_state.punteggio} / 24")

if st.session_state.punteggio <= 5:
    st.info("Bassa aderenza alla dieta mediterranea")
elif st.session_state.punteggio <= 10:
    st.info("Media aderenza alla dieta mediterranea")
else:
    st.info("Alta aderenza alla dieta mediterranea")

st.caption("*Fonte: Mediterranean Diet Serving Score (Monteagudo et al., 2015)*")

codice = st.text_input("Assegna un codice a questa intervista")
salva = st.button("Salva")

if codice:
    st.session_state.codice = codice

if salva and st.session_state.codice:
    txt_buffer = io.StringIO()
    txt_buffer.write("Questionario di Aderenza alla Dieta Mediterranea (ADM)\n\n")
    txt_buffer.write(f"Codice intervista: {st.session_state.codice}\n")
    txt_buffer.write(f"Genere: {st.session_state.get('genere', 'Non specificato')}\n\n")
    for idx, (key, testo, _, _, _) in enumerate(DOMANDE, 1):
        risposta = st.session_state.get(key, "Nessuna risposta")
        txt_buffer.write(f"{idx}. {testo}\nRisposta: {risposta}\n\n")
    txt_buffer.write(f"14. Quanti bicchieri di vino/birra bevi al giorno\nRisposta: {st.session_state.get('Bevande alcoliche', 'Nessuna risposta')}\n\n")
    txt_buffer.write(f"Punteggio MDSS: {st.session_state.punteggio} / 24\n\n")
    txt_buffer.write("punteggio di aderenza alla dieta mediterranea (MDSS: Mediterranean Diet Serving Score) calcolato secondo Monteagudo et al (https://doi.org/10.1371/journal.pone.0128594) ed ottenuto tramite web app del dott. Giovanni Buonsanti - Matera\n")
    txt_bytes = txt_buffer.getvalue().encode("utf-8")
    txt_b64 = base64.b64encode(txt_bytes).decode()
    txt_href = f'<a href="data:application/octet-stream;base64,{txt_b64}" download="MDSS_{st.session_state.codice}.txt">📄 Scarica il file TXT</a>'

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Codice intervista", st.session_state.codice])
    writer.writerow(["Genere", st.session_state.get("genere", "")])
    writer.writerow(["Punteggio MDSS", st.session_state.punteggio])
    writer.writerow([])
    for idx, (key, testo, _, _, _) in enumerate(DOMANDE, 1):
        risposta = st.session_state.get(key, "")
        writer.writerow([f"{idx}. {testo}", risposta])
    writer.writerow(["14. Quanti bicchieri di vino/birra bevi al giorno", st.session_state.get("Bevande alcoliche", "")])
    writer.writerow([])
    writer.writerow(["Nota", "punteggio di aderenza alla dieta mediterranea (MDSS: Mediterranean Diet Serving Score) calcolato secondo Monteagudo et al (https://doi.org/10.1371/journal.pone.0128594) ed ottenuto tramite web app del dott. Giovanni Buonsanti - Matera"])
    csv_bytes = csv_buffer.getvalue().encode("utf-8")
    csv_b64 = base64.b64encode(csv_bytes).decode()
    csv_href = f'<a href="data:application/octet-stream;base64,{csv_b64}" download="MDSS_{st.session_state.codice}.csv">📊 Scarica il file CSV</a>'

    st.markdown(txt_href, unsafe_allow_html=True)
    st.markdown(csv_href, unsafe_allow_html=True)
