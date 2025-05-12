import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calcolo Importi con IVA", layout="centered")

st.title("💶 Calcolatore Totali con IVA Personalizzata")

# Input: importo e IVA
importo_lordo = st.number_input("💰 Inserisci l'importo in bolletta (IVA inclusa)", min_value=0.0, format="%.2f")
aliquota_iva_label = st.radio("📌 Seleziona l'aliquota IVA:", ["10%", "22%"])
aliquota_iva = 0.10 if aliquota_iva_label == "10%" else 0.22

if importo_lordo > 0:
    # 1. Rimuove IVA
    imponibile = importo_lordo / (1 + aliquota_iva)
    # 2. Togliamo il fisso di 25.5
    netto = imponibile - 25.5

    st.markdown(f"**Importo senza IVA:** €{imponibile:.2f}")
    st.markdown(f"**Importo netto dopo -25.5:** €{netto:.2f}")
    
    # 3. Tariffe aggiuntive
    aggiunte = [16.5, 18.5, 21.5, 35]
    etichette = ["PRO 16.5", "PRO 18.5", "PRO 21.5", "PRO 35"]

    # 4. Calcoli finali
    risultati = []
    for aggiunta in aggiunte:
        base = netto + aggiunta
        iva = base * aliquota_iva
        totale = base + iva
        risultati.append(round(totale, 2))

    # 5. Visualizzazione tabella
    df = pd.DataFrame([risultati], columns=etichette)
    st.subheader("📊 Totali a Pagare con IVA")
    st.dataframe(df, use_container_width=True)

    st.markdown("✅ Puoi copiare e incollare direttamente questa tabella.")
