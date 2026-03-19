import streamlit as st
import pandas as pd
import json

# Import your modules (make sure folder names are correct)
from extraction_logic.parser import extract_text, extract_info
from cleaning_helpers.utils import clean_text

# App Title
st.set_page_config(page_title="Smart Resume Parser", page_icon="📄")
st.title("📄 AI Smart Resume Parser")

# File Upload
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    try:
        # Step 1: Extract text
        text = extract_text(uploaded_file)

        # Step 2: Clean text
        clean = clean_text(text)

        # Step 3: Extract info
        data = extract_info(clean)

        # Display Output
        st.subheader("📊 Extracted Information")
        st.json(data)

        # Save outputs
        # Create outputs folder if not exists
        import os
        if not os.path.exists("outputs"):
            os.makedirs("outputs")

        # Save JSON
        with open("outputs/output.json", "w") as f:
            json.dump(data, f, indent=4)

        # Save CSV
        df = pd.DataFrame([data])
        df.to_csv("outputs/output.csv", index=False)

        # Download buttons
        st.download_button("⬇ Download JSON", json.dumps(data, indent=4), "output.json")
        st.download_button("⬇ Download CSV", df.to_csv(index=False), "output.csv")

        st.success("✅ Resume processed successfully!")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

else:
    st.info("📌 Please upload a resume file to begin.")
