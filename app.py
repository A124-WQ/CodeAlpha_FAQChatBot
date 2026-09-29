import streamlit as st

from chatbot import FAQChatbot

st.set_page_config(page_title="ShopEase FAQ Chatbot", page_icon="🤖")


@st.cache_resource
def get_bot():
    return FAQChatbot()


bot = get_bot()

st.title("🤖 ShopEase FAQ Chatbot")
st.caption("Ask about orders, shipping, returns, payments and your account.")

with st.sidebar:
    st.header("Try asking")
    for sample in bot.questions[:8]:
        st.write("•", sample)
    if st.button("Clear chat"):
        st.session_state.pop("messages", None)
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How can I help you today?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Type your question here")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    answer, score = bot.reply(prompt)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
