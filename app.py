import streamlit as st
import os

API_KEY = os.environ.get("AI_API_KEY", "")

st.set_page_config(page_title="聊天机器人")
st.title("🤖 简易聊天机器人 (DeepSeek)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("请输入你的问题..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})

    if API_KEY:
        try:
            import openai
            client = openai.OpenAI(
                api_key=API_KEY,
                base_url="https://api.deepseek.com"
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"AI 调用失败：{str(e)}"
    else:
        reply = f"你说的是：{prompt}（未配置 AI_API_KEY 环境变量）"

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role":"assistant","content":reply})