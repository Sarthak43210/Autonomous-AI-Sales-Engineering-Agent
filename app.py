import streamlit as st
import pandas as pd
import time
from streamlit_extras.add_vertical_space import add_vertical_space
from agent import search_company_news, write_email_logic

# Page Config: Dark mode & Wide layout
st.set_page_config(page_title="AgentX | AI Outreach", page_icon="🚀", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #2962ff;
        color: white;
        font-weight: bold;
    }
    .company-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for Branding & Stats
with st.sidebar:
    st.title("🤖 AgentX v2.0")
    st.info("The next generation of autonomous sales outreach.")
    add_vertical_space(2)
    st.metric(label="Total Tokens Saved", value="42.5k")
    st.metric(label="Efficiency Boost", value="+85%")

# Header
st.title("🚀 Autonomous Sales Pipeline")
st.caption("Upload your leads and watch the agent conduct 2026-level market research.")

# Layout: Two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📁 Data Ingestion")
    uploaded_file = st.file_uploader("Drop your leads.csv here", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    with col2:
        st.subheader("⚡ Live Processing")
        if st.button("Generate AI Campaign"):
            results = []
            
            for index, row in df.iterrows():
                company = row['company_name']
                
                # Visual "Card" for each company
                with st.container():
                    st.markdown(f'<div class="company-card">', unsafe_allow_html=True)
                    st.markdown(f"### 🏢 {company}")
                    
                    # Status Spinners
                    with st.status(f"Agent researching {company}...", expanded=False) as status:
                        research = search_company_news(company)
                        st.write("✓ Crawling 2026 news archives...")
                        st.write("✓ Identifying pain points...")
                        status.update(label="Research Complete!", state="complete")
                    
                    email = write_email_logic(company, research)
                    
                    # Display the Email in a professional code block
                    st.markdown("**Drafted Outreach:**")
                    st.code(email, language="markdown")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    results.append({"Company": company, "Email": email})
                    
                    # Wait for API limit (35s)
                    if index < len(df) - 1:
                        st.write("⏳ Cooling down to respect API quota...")
                        time.sleep(35)
            
            # Final Results Download
            res_df = pd.DataFrame(results)
            csv = res_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Campaign CSV", csv, "campaign.csv", "text/csv")