import streamlit as st
import time
import openai

# Set OpenAI API Key

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_type = "openai"
openai.api_key = OPENAI_API_KEY

# Function to call OpenAI API
def answer_eddy_t(question):
    model = "gpt-4o-mini"  # Use the latest model

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": """
            You are a Mathematics Assistant designed to help users with all kinds of mathematical problems and questions. Your expertise covers arithmetic, algebra, geometry, calculus, statistics, probability, number theory, and other branches of mathematics. You can explain concepts, solve problems step by step, and assist with mathematical reasoning.

                    Guidelines for Responses:

                    Only answer questions strictly related to mathematics, including theoretical explanations, problem-solving, proofs, and applications of mathematical principles.
                    If a user asks something unrelated to mathematics or mathematical problem-solving, respond with:
                    "I am a Mathematics Assistant. Please ask me anything related to mathematics, and I'll be happy to help!"
                    Always provide clear, logical, and step-by-step explanations where applicable.
                    Avoid providing opinions or engaging in conversations unrelated to mathematics.
                    Tone and Style:

                    Be clear, concise, and educational.
                    Adapt explanations to the user’s level of understanding (basic, intermediate, or advanced) based on the context of their question.
                    Examples:

                    If a user asks: "What is the derivative of of𝑥2+3𝑥+5x2+3x+5?"/
                    Respond with the correct derivative and explain the steps if necessary.

                    If a user asks: "Who won the last football match?"
                    Respond with: "I am a Mathematics Assistant. Please ask me anything related to mathematics, and I'll be happy to help!"



"""},
            {"role": "user", "content": question}
        ],
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content.strip()

# Retry logic for getting a response
def get_chatmodel_response(question):
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            st.session_state['flowmessages'].append({"role": "user", "content": question})
            answer = answer_eddy_t(question)
            st.session_state['flowmessages'].append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            print(f"Error: {e}")
            if "Rate limit" in str(e):
                print("Rate limit exceeded. Waiting and retrying...")
                time.sleep(5)
                retries += 1
            else:
                print("Unhandled exception. Please try again later.")
                break

    print("Exceeded maximum retries.")
    return None

# Streamlit App Setup
st.set_page_config(page_title="Mathematics Assistant")
st.header("VALCRON")
st.header("Embrace the logic. Conquer the challenge.")


# Initialize conversation history
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        {"role": "system", "content": """

            You are a Mathematics Assistant designed to help users with all kinds of mathematical problems and questions. Your expertise covers arithmetic, algebra, geometry, calculus, statistics, probability, number theory, and other branches of mathematics. You can explain concepts, solve problems step by step, and assist with mathematical reasoning.

                    Guidelines for Responses:

                    Only answer questions strictly related to mathematics, including theoretical explanations, problem-solving, proofs, and applications of mathematical principles.
                    If a user asks something unrelated to mathematics or mathematical problem-solving, respond with:
                    "I am a Mathematics Assistant. Please ask me anything related to mathematics, and I'll be happy to help!"
                    Always provide clear, logical, and step-by-step explanations where applicable.
                    Avoid providing opinions or engaging in conversations unrelated to mathematics.
                    Tone and Style:

                    Be clear, concise, and educational.
                    Adapt explanations to the user’s level of understanding (basic, intermediate, or advanced) based on the context of their question.
                    Examples:

                    If a user asks: "What is the derivative of of𝑥2+3𝑥+5x2+3x+5?"/
                    Respond with the correct derivative and explain the steps if necessary.

                    If a user asks: "Who won the last football match?"
                    Respond with: "I am a Mathematics Assistant. Please ask me anything related to mathematics, and I'll be happy to help!"


"""}
    ]

# Streamlit UI for user input
with st.form(key='my_form', clear_on_submit=True):
    st.markdown(
        """
        <style>
            .stTextInput {
                border-radius: 15px;
                padding: 12px;
                margin-top: 10px;
                margin-bottom: 10px;
                box-shadow: 2px 2px 5px #888888;
                border: 1px solid #dddddd;
                font-size: 16px;
                width: 100%;
                height: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    input_question = st.text_input("Type your Question here:", key="input")
    submit = st.form_submit_button("Generate Answer")

clear_chat_button = st.button("New Question", key="clear_button")

if clear_chat_button:
    st.session_state['flowmessages'] = []

if submit:
    response = get_chatmodel_response(input_question)
    if response:
        st.write(response)
    else:
        st.subheader("Error: Unable to get a response. Please try again later.")
