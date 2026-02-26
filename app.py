import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="AI Email Pro", page_icon="🚀", layout="wide")

# ලස්සනට පෙනෙන්න CSS ටිකක් දාමු
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #ff4b4b; color: white; }
    .result-box { padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; background-color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - උඹේ විස්තර මෙතනට දාපන්
with st.sidebar:
    st.title("👨‍💻 Developer Info")
    st.info("මෙම App එක මගින් ඊමේල් වර්ගීකරණය සහ පිළිතුරු ලිවීම ස්වයංක්‍රීයව සිදු කරයි.")
    st.markdown("---")
    st.write("Done by: **Kasun**")
    st.success("Status: AI Engine Active")

# 3. Main Interface
st.title("📩 Smart AI Email Assistant")
st.write("ඔයාගේ ඊමේල් එක පහළින් පේස්ට් කරන්න. AI එක ඒක කියවලා හොඳම පිළිතුර ලියයි.")

# Groq Setup
api_key = "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"
client = Groq(api_key=api_key)

# Input Area
email_content = st.text_area("Email Content:", placeholder="මෙතන පේස්ට් කරන්න...", height=250)

if st.button("Analyze & Write Reply ✨"):
    if email_content:
        with st.spinner('AI එක හිතනවා... 🧠'):
            try:
                # Prompt එක තවත් දියුණු කරමු
                prompt = f"""
                Analyze this email: {email_content}
                1. Decide if it's 'Urgent' or 'Normal'.
                2. Write a professional and friendly reply.
                Format: 
                CATEGORY: [Type]
                REPLY: [Text]
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                full_res = completion.choices[0].message.content
                
                # පෙනුම ලස්සනට කොටස් වලට බෙදමු
                st.markdown("---")
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if "Urgent" in full_res:
                        st.error("🚨 Priority: URGENT")
                    else:
                        st.success("✅ Priority: NORMAL")
                
                with col2:
                    st.markdown("### ✍️ Suggested Reply:")
                    st.info(full_res.split("REPLY:")[1] if "REPLY:" in full_res else full_res)
                    
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("කරුණාකර ඊමේල් එකක් ඇතුළත් කරන්න.")