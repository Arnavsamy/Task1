import streamlit as st
from groq import Groq


st.set_page_config(
    page_title="Investor Scout Pro", 
    page_icon="⚡",
    layout="wide" 
)

# CSS 
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #f55036; /* Groq Orange */
        color: white;
        font-size: 20px;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        width: 100%;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #cf3a22;
        color: white;
    }
    .reportview-container {
        background: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR 
with st.sidebar:
    st.header("⚙️ Configuration")
    
    
    api_key = st.text_input("Groq API Key", type="password", help="Paste your gsk_... key here")
    
    st.divider()
    
    
    num_investors = st.slider("Number of Investors", min_value=1, max_value=10, value=3)
    
    
    stage = st.selectbox(
        "Investment Stage", 
        ["Any Stage", "Pre-Seed", "Seed", "Series A", "Series B+", "Private Equity"]
    )
    
    st.info("💡 **Tip:** Use specific sectors like 'Generative AI' for better results.")

# MAIN 
st.title("⚡ Investor Scout Pro")
st.markdown(f"### Find the perfect capital partners for your **{stage}** startup.")


with st.expander("ℹ️ How this tool works"):
    st.write("""
    1. Enter your **Sector** (what you do) and **Country** (where you are).
    2. Select your **Stage** and **Count** in the sidebar.
    3. The AI scans its database to find relevant active investors.
    """)

st.divider()


col1, col2 = st.columns(2)

with col1:
    sector = st.text_input("Industry / Sector", placeholder="e.g. SaaS, BioTech, Crypto")

with col2:
    country = st.text_input("Target Country", placeholder="e.g. United Kingdom, India, USA")

# APP 
if st.button("🔍 Find Investors"):
    if not api_key:
        st.error("🔒 Please enter your Groq API Key in the sidebar to proceed.")
    elif not sector or not country:
        st.warning("⚠️ Please fill in both Sector and Country fields.")
    else:
        try:
            
            with st.spinner("Analyzing market data..."):
                
                
                client = Groq(api_key=api_key)
                
                
                prompt = (
                    f"List {num_investors} venture capital firms or angel investors in {country} "
                    f"that specifically invest in the {sector} sector at the {stage} stage. "
                    f"For each investor, provide:\n"
                    f"1. Name\n"
                    f"2. A one-sentence focus area\n"
                    f"3. Why they are a good fit.\n"
                    f"Format the output as clean Markdown."
                )

                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert venture capital analyst."
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama-3.1-8b-instant",
                    temperature=0.7 
                )

                
                result_text = chat_completion.choices[0].message.content
                
                st.markdown("---")
                st.subheader("🎯 Search Results")
                
                
                with st.container(border=True):
                    st.markdown(result_text)
                    
                st.success("Analysis Complete!")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")