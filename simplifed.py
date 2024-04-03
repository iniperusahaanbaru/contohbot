#Importing required packages
import streamlit as st
from anthropic import  HUMAN_PROMPT, AI_PROMPT
import anthropic
import uuid
import math

INIT_PROMPT = """ 

1.Fokus pada Digital Marketing: Utamakan jawaban yang berkaitan dengan digital marketing, menggunakan contoh relevan untuk menjelaskan konsep-konsep. Ketika Topik Tidak Berkaitan:

2.ika pertanyaan tidak terkait digital marketing informasikan bahwa Anda tidak dapat menjawabnya secara langsung.

3.Berikan Contoh yang Menarik dan Gunakan Analogi: Sertakan contoh yang menarik dan gunakan analogi dengan hal-hal familiar untuk memudahkan pemahaman konsep digital marketing.

4. Interaktivitas: interaktivitas untuk memperjelas penjelasan dan meningkatkan keterlibatan user. Penggunaan Bahasa yang Positif dan Kesederhanaan:

5.Gunakan bahasa yang positif dan jaga kesederhanaan dalam penyampaian untuk memudahkan pemahaman dan menjaga fokus. Mengajak Berpikir Kritis:

6.Meskipun menggunakan pendekatan sederhana, ajak user untuk berpikir kritis tentang topik yang dibahas untuk mengembangkan pemahaman mereka pada level yang lebih dalam.
"""

TRAINING_PROMPT = """



"""

INTRO_PROMPT = """

"""

# Anthropic Claude pricing: https://cdn2.assets-servd.host/anthropic-website/production/images/model_pricing_may2023.pdf
PRICE_PROMPT = 1.102E-5
PRICE_COMPLETION = 3.268E-5

#MODEL = "claude-1"
#MODEL = "claude-2.1"
MODEL = "claude-3-haiku-20240307"
#MODEL = "claude-v1-100k"

st.title("Chat dengan mentor Darun")

new_prompt = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    



if "claude_model" not in st.session_state:
    st.session_state["claude_model"] = MODEL

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "all_prompts" not in st.session_state:
    st.session_state["all_prompts"] = INIT_PROMPT + TRAINING_PROMPT

def count_used_tokens(prompt, completion):
    prompt_token_count = client.count_tokens(prompt)
    completion_token_count = client.count_tokens(completion)
    prompt_cost = prompt_token_count * PRICE_PROMPT
    completion_cost = completion_token_count * PRICE_COMPLETION
    total_cost = prompt_cost + completion_cost
    total_cost = math.ceil(total_cost * 100) / 100
    return (
        prompt_token_count,
        completion_token_count,
        total_cost
    )
    

    # If the user has provided an API key, use it

client=anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=st.secrets['ANTHROPIC_API_KEY']
)

with st.chat_message("assistant"):
    st.write("Hello ini adalah Bot Darun , ini BUKAN Darun asli 👋")


for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            new_prompt.append(message["content"])
            st.markdown(message["content"])
            

if user_input := st.chat_input("Ayo tanya tanya tentang beriklan"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    print(st.session_state.messages)
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
    full_response = ""
    message =  client.messages.create(
        messages=st.session_state.messages ,
        system = st.session_state["all_prompts"],
        model=MODEL,
        max_tokens=150,  # Adjust the max_tokens value as needed
    )
    response=message.content[0].text
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
    
    # Display token usage and cos