import streamlit as st
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Kasun's AI Smart Assistant", page_icon="🧠", layout="wide")

# 2. Initialize Counters (මේක තමයි අමතක වුණේ!)
if 'total_count' not in st.session_state:
    st.session_state.total_count = 0
if 'urgent_count' not in st.session_state:
    st.session_state.urgent_count = 0

# UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button { border-radius: 20px; background: linear-gradient(45deg, #00dbde, #fc00ff); color: white; border: none; width: 100%; font-weight: bold; }
    .dev-tag { background: #1E1E1E; padding: 10px; border-radius: 10px; text-align: center; color: #fc00ff; font-weight: bold; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Dashboard (ඔන්න දැන් ආයෙත් Counters ටික තියෙනවා)
with st.sidebar:
    st.title("📊 Performance Dashboard")
    st.metric("Total Emails Processed", st.session_state.total_count)
    st.metric("Urgent Emails Found", st.session_state.urgent_count)
    st.markdown("---")
    st.markdown('<div class="dev-tag">Developed with ❤️ by Kasun</div>', unsafe_allow_html=True)

# 4. Main Interface
st.title("🚀 Smart AI Email Pro (Multi-Language)")
st.write("Automatically identify language, priority, and generate replies.")

# API Setup
client = Groq(api_key="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")

email_content = st.text_area("Paste Email Content (English or Sinhala):", height=200, placeholder="Type or paste here...")

if st.button("Smart Analyze ✨"):
    if email_content:
        # Counter එක වැඩි කරනවා
        st.session_state.total_count += 1
        
        with st.spinner('AI is analyzing...'):
            try:
                prompt = f"""
                Identify the language. If Sinhala, reply in Sinhala. If English, reply in English.
                Provide:
                1. PRIORITY: (Urgent/Normal)
                2. LANGUAGE: (Sinhala/English)
                3. SUMMARY: (Short summary)
                4. SUGGESTED REPLY: (Professional response)

                Email: {email_content}
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                response_text = completion.choices[0].message.content
                
                # Urgent ද කියලා චෙක් කරලා Counter එක වැඩි කරනවා
                if "Urgent" in response_text or "හදිසි" in response_text:
                    st.session_state.urgent_count += 1
                
                st.markdown("### 🔍 Smart Analysis Result")
                st.info(response_text)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please paste an email first!")