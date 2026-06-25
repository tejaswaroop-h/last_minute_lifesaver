import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="The Last-Minute Life Saver", page_icon="⏰", layout="centered")

st.title("⏰ The Last-Minute Life Saver")
st.subheader("Your AI-Powered Anti-Procrastination Companion")
st.write("Stop panicking. Let AI break down your tasks and force you into action.")

# 2. Backend API Key Fetch
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    backend_ready = True
except Exception:
    st.error("🔒 Backend Configuration Error: API Key missing or invalid in secrets.toml.")
    backend_ready = False

# 3. Application Features
if backend_ready:
    
    # GLOBAL INPUTS (Placed outside forms so both buttons can see them)
    st.header("🎯 Step 1: Enter Your Deadline Details")
    task_input = st.text_area("What project or assignment are you stressing about?", 
                              placeholder="e.g., Study for Java OOP quiz and complete lab exercises")
    time_left = st.text_input("How much time do you have left?", placeholder="e.g., 24 hours, 3 days")
    
    st.markdown("---")
    
    # FEATURE 1 ACTION
    st.header("📋 Option 1: Break Down Your Schedule")
    if st.button("Generate Action Plan", type="primary"):
        if task_input and time_left:
            with st.spinner("AI is calculating your rescue plan..."):
                prompt = f"""
                You are an aggressive, highly efficient productivity coach. 
                The user has this task: '{task_input}' and only '{time_left}' left.
                Break this task down into a strict, hour-by-hour or day-by-day action plan. 
                Keep steps tiny, hyper-actionable, and clear so a beginner cannot fail.
                """
                response = model.generate_content(prompt)
                st.success("### Your Step-by-Step Schedule:")
                st.write(response.text)
        else:
            st.warning("Please fill out both fields above first!")

    st.markdown("---")

    # FEATURE 2 ACTION
    st.header("🛑 Option 2: Need a Reality Check?")
    st.write("Get an aggressive notification text designed to make you start working immediately.")
    if st.button("Generate Emergency Nudge"):
        if task_input:
            with st.spinner("Drafting your wakeup call..."):
                nudge_prompt = f"Write a short, highly urgent, witty, and motivating push-notification style message for someone avoiding: '{task_input}'."
                nudge_response = model.generate_content(nudge_prompt)
                st.error(nudge_response.text)
        else:
            st.warning("Please enter a task in the input box at the top first!")