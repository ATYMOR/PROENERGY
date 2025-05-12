import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
from io import BytesIO

st.title("📄 Calcolatore Fattura - con IVA, Totali, PDF ed Excel")

# Inserimento importo originale
importo_lordo = st.number_input("💰 Inserisci l'importo in bolletta (con IVA):", min_value=0.0, format="%.2f")

# Selezione dell'aliquota IVA
iva_opzione = st.radio("🧾 Seleziona l'aliquota IVA:", ["10%", "22%"])
aliquota_iva = 0.10 if iva_opzione == "10%" else 0.22

if importo_lordo > 0:
    # Calcolo imponibile e netto base
    imponibile = importo_lordo / (1 + aliquota_iva)
    netto_base = imponibile - 25.5

    # Opzioni
    aggiunte = [16.5, 18.5, 21.5, 35]
    nomi_colonne = ["PRO 16.5", "PRO 18.5", "PRO 21.5", "PRO 35"]
    totali = []

    for aggiunta in aggiunte:
        netto = netto_base + aggiunta
        iva = netto * aliquota_iva
        totale = netto + iva
        totali.append(round(totale, 2))

    # Creazione DataFrame
    df = pd.DataFrame([totali], columns=nomi_colonne)
    st.subheader("📊 Totali a Pagare con IVA inclusa")
    st.dataframe(df, use_container_width=True)

    # ========= GENERAZIONE PDF =========
    if st.button("📥 Scarica PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Calcolo Totali con IVA", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Importo in bolletta (con IVA): €{importo_lordo}", ln=True)
        pdf.cell(200, 10, txt=f"Aliquota IVA: {iva_opzione}", ln=True)
        pdf.cell(200, 10, txt=f"Imponibile (senza IVA): €{imponibile:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Netto dopo -25.5: €{netto_base:.2f}", ln=True)
        pdf.ln(5)

        for i, nome in enumerate(nomi_colonne):
            pdf.cell(200, 10, txt=f"{nome}: €{totali[i]}", ln=True)

        # Salva PDF in memoria
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        b64_pdf = base64.b64encode(pdf_buffer.read()).decode()
        href_pdf = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="fattura_risultato.pdf">📄 Clicca per scaricare il PDF</a>'
        st.markdown(href_pdf, unsafe_allow_html=True)

    # ========= GENERAZIONE EXCEL =========
    if st.button("📊 Scarica Excel"):
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        b64_excel = base64.b64encode(excel_buffer.read()).decode()
        href_excel = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="fattura_risultato.xlsx">📊 Clicca per scaricare il file Excel</a>'
        st.markdown(href_excel, unsafe_allow_html=True)
