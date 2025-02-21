
import streamlit as st
import pandas as pd
import os
from io import BytesIO
from streamlit_lottie import st_lottie
import requests

# Set Page Configurations
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom Tailwind-Inspired Styling with Purple-Gray Theme
st.markdown(
    """
    <style>
    /* Global Styles */
    body { 
        background: linear-gradient(to right, #6B5B95, #B0A8B9);
        font-family: 'Inter', sans-serif;
    }

    /* Container Card */
    .stApp {
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin: 20px;
    }

    /* Buttons */
    .stButton>button, .stDownloadButton>button {
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 16px;
        font-weight: 600;
        transition: 0.3s;
    }

    .stButton>button {
        background: #6B5B95;
        color: white;
        border: none;
    }

    .stButton>button:hover {
        background: #564F8C;
        transform: scale(1.05);
    }

    .stDownloadButton>button {
        background: #9178C8;
        color: white;
        border: none;
    }

    .stDownloadButton>button:hover {
        background: #7A5DBF;
        transform: scale(1.05);
    }

    /* File Upload Box */
    .stFileUploader {
        background: #E1D9E5;
        border-radius: 10px;
        padding: 10px;
        border: 2px dashed #6B5B95;
    }

    /* Headings */
    .stTitle, .stHeader {
        color: #3D2C8D;
        font-weight: 700;
        text-align: center;
        justify-content: center;
    }


    /* Centering the Lottie animation */
    .lottie-animation {
        display: flex;
        justify-content: center;
    }

    /* Data Table */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Spacing */
    .stMarkdown {
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧹 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# Function to Load Lottie Animations
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie Animations
lottie_upload = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_w51pcehl.json")
lottie_processing = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_j4u6gfux.json")
lottie_success = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_rpbt5kpk.json")
lottie_visual = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_2ibxqx3y.json")

# Display Upload Animation with Slower Speed
if lottie_upload:
    st.markdown('<div class="lottie-animation">', unsafe_allow_html=True)
    st_lottie(lottie_upload, speed=0.6, width=500, height=300, key="upload_anim")
    st.markdown('</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader("📂 Upload a CSV or Excel file", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📦 File Size:** {file.size / 1024:.2f} KB")

        # Processing Animation with Slower Speed
        if lottie_processing:
            st.markdown('<div class="lottie-animation">', unsafe_allow_html=True)
            st_lottie(lottie_processing, speed=0.6, width=300, height=200, key="processing_anim")
            st.markdown('</div>', unsafe_allow_html=True)

        st.write("### 🔍 Data Preview")
        st.dataframe(df.head())

        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"✨ Clean Data for {file.name}"):
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(f"🗑 Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            with col2:
                if st.button(f"📊 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if not numeric_cols.empty:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✅ Missing values filled!")
                    else:
                        st.warning("⚠ No numeric columns found!")

            with col3:
                if st.button(f"🧹 Remove Empty Rows from {file.name}"):
                    df.dropna(how='all', inplace=True)
                    st.success("✅ Empty rows removed!")

            if st.button(f"📏 Normalize Numeric Data for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                if not numeric_cols.empty:
                    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())
                    st.success("✅ Numeric data normalized!")
                else:
                    st.warning("⚠ No numeric columns found!")

        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Visualization for {file.name}"):
            numeric_cols = df.select_dtypes(include=['number']).columns
            if not numeric_cols.empty:
                st.bar_chart(df[numeric_cols])
                # Visualization Animation with Slower Speed
                if lottie_visual:
                    st.markdown('<div class="lottie-animation">', unsafe_allow_html=True)
                    st_lottie(lottie_visual, speed=0.6, width=300, height=200, key="visual_anim")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠ No numeric columns found for visualization!")

        st.subheader("📤 Conversion Options")
        conversion_options = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"🔄 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_options == "CSV":
                df.to_csv(buffer, index=False)
                file_name = f"{os.path.splitext(file.name)[0]}_converted.csv"
                mime_type = "text/csv"
            elif conversion_options == "Excel":
                df.to_excel(buffer, index=False)
                file_name = f"{os.path.splitext(file.name)[0]}_converted.xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_options}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

        # Success Animation with Slower Speed
        if lottie_success:
            st.markdown('<div class="lottie-animation">', unsafe_allow_html=True)
            st_lottie(lottie_success, speed=0.1, width=300, height=200, key="success_anim")
            st.markdown('</div>', unsafe_allow_html=True)

    st.success("🎉 All files processed successfully!")


