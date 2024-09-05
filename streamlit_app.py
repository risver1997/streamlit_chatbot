import streamlit as st
from openai import OpenAI

st.title("ChatGPT clone")

enable_chat_input = True

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if openai_api_key.startswith("sk-"):
    enable_chat_input = False

client = OpenAI(api_key = openai_api_key)

if "openai_model" not in st.session_state:
	st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
	st.session_state.messages = []

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])

if prompt := st.chat_input("Wassup?", disabled = enable_chat_input):
	st.session_state.messages.append({"role": "user", "content": prompt})
	with st.chat_message("user"):
		st.markdown(prompt)
	
	with st.chat_message("assistant"):
		stream = client.chat.completions.create(
			model = st.session_state["openai_model"],
			messages = [
				{"role": m["role"], "content": m["content"]}
				for m in st.session_state.messages
			],
			stream = True
		)
		response = st.write_stream(stream)
	st.session_state.messages.append({"role": "assistant", "content": response})