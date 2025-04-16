import streamlit as st
import pandas as pd

# Set up the Streamlit app layout
st.set_page_config(layout="wide")
st.title("📦 Vehicle Tonnage Lookup")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df = df.fillna('')  # Keep blank entries visible

        st.success("✅ File uploaded successfully!")

        # Sidebar filters
        st.sidebar.header("🔍 Filter Options")
        all_regions = sorted(df["Region"].unique())
        selected_region = st.sidebar.selectbox("Select Region (optional)", [""] + all_regions)

        filtered_df = df.copy()

        if selected_region:
            filtered_df = filtered_df[filtered_df["Region"] == selected_region]

        all_plates = sorted(filtered_df["Registration Number"].unique())
        selected_reg = st.sidebar.selectbox("Select Registration Number (optional)", [""] + all_plates)

        # If a registration number is selected, filter all entries across all regions
        if selected_reg:
            reg_df = df[df["Registration Number"] == selected_reg]
            st.subheader("📋 Vehicle Details")
            st.dataframe(reg_df, use_container_width=True)
        elif selected_region:
            st.subheader(f"📍 All Vehicles in {selected_region}")
        else:
            st.subheader("📍 All Vehicles")

        # Function for hover-enabled HTML table
        def generate_tooltip_table(df):
            html = """
            <style>
            .tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
                color: #1f77b4;
                font-weight: bold;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 220px;
                background-color: black;
                color: #fff;
                text-align: left;
                border-radius: 6px;
                padding: 6px;
                position: absolute;
                z-index: 1;
                bottom: 150%;
                left: 50%;
                transform: translateX(-50%);
                opacity: 0;
                transition: opacity 0.3s;
                font-size: 14px;
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th, td {
                padding: 8px 12px;
                border: 1px solid #ddd;
                text-align: left;
                font-size: 16px;
            }
            th {
                background-color: #f4f4f4;
            }
            </style>
            <table>
                <thead>
                    <tr>
                        <th>Registration Number</th>
                        <th>Region</th>
                        <th>Tonnage</th>
                    </tr>
                </thead>
                <tbody>
            """
            for _, row in df.iterrows():
                reg = row['Registration Number']
                region = row['Region']
                tonnage = row['Tonnage']

                tooltip = f"""
                <div class='tooltip'>{reg}
                    <span class='tooltiptext'>
                        Region: {region if region else '—'}<br>
                        Tonnage: {tonnage if tonnage else '—'}
                    </span>
                </div>
                """
                html += f"<tr><td>{tooltip}</td><td>{region}</td><td>{tonnage}</td></tr>"

            html += "</tbody></table>"
            return html

        st.markdown("### 🧾 Vehicles Table (hover over plate numbers):")
        table_data = df[df["Registration Number"] == selected_reg] if selected_reg else filtered_df
        st.markdown(generate_tooltip_table(table_data), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📤 Please upload an Excel file to get started.")
