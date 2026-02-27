import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="AI Email Pro 2.0", page_icon="🚀", layout="wide")

# Dashboard Metrics Initialize (පොඩි Dashboard එකක් හදමු)
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'urgent_count' not in st.session_state:
    st.session_state.urgent_count = 0

# UI Styling
st.markdown("""
    <style>
    .metric-box { background-color: #ffffff; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Dashboard
with st.sidebar:
    st.title("📊 Usage Dashboard")
    col1, col2 = st.columns(2)
    col1.metric("Total Emails", st.session_state.count)
    col2.metric("Urgent", st.session_state.urgent_count)
    st.markdown("---")
    st.info("AI Engine: Llama 3.3-70B")

# Main Header
st.title("📩 Smart AI Email Pro v2.0")

# API Key - (මතක ඇතුව ඔයාගේ Key එක මෙතනට දාන්න)
client = Groq(api_key="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")

email_content = st.text_area("ඊමේල් එක මෙතනට පේස්ට් කරන්න:", height=200)

if st.button("Analyze & Reply ✨"):
    if email_content:
        st.session_state.count += 1 # Total count එක වැඩි කරනවා
        with st.spinner('AI එක වැඩ පටන් ගත්තා...'):
            try:
                # දියුණු කරන ලද Prompt එක
                prompt = f"""
                Analyze the following email and provide:
                1. PRIORITY: (Urgent or Normal)
                2. TONE: (Detected tone of the sender - e.g., Angry, Friendly, Professional)
                3. SUMMARY: (A 1-sentence summary of the core issue)
                4. REPLY: (A response that MATCHES the sender's tone but stays professional)

                Email: {email_content}
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                response = completion.choices[0].message.content
                
                # Urgent නම් Dashboard එක Update කරනවා
                if "Urgent" in response:
                    st.session_state.urgent_count += 1
                
                # Display Results
                st.markdown("### 🔍 Analysis Results")
                c1, c2, c3 = st.columns(3)
                
                # Results ලස්සනට කොටස් වලට බෙදා පෙන්වීම
                with c1:
                    st.success("✅ Priority Determined")
                with c2:
                    st.info("🎭 Tone Matched")
                with c3:
                    st.warning("📝 Summary Created")
                
                st.write(response) # මෙතන ඔක්කොම විස්තර පේනවා
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("කරුණාකර ඊමේල් එකක් ඇතුළත් කරන්න.")