from groq import Groq
import streamlit as st 

# Inject Bootstrap for a stylish UI
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* Cool gradient background */
        .main {
            background: linear-gradient(135deg, #ff9a9e, #fad0c4, #ffdde1);
        }

        /* Chat container */
        .chat-container {
            max-width: 800px;
            margin: auto;
            padding: 10px;
        }

        /* User messages - White BG, Black Text */
        .user-msg {
            background: #ffffff;
            color: black;
            padding: 12px;
            border-radius: 20px;
            margin: 5px;
            text-align: left;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            width: fit-content;
        }

        /* AI messages - Cyan BG, White Text */
        .assistant-msg {
            background: #0dcaf0;
            color: white;
            padding: 12px;
            border-radius: 20px;
            margin: 5px;
            text-align: left;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            width: fit-content;
        }

        /* Title Styling */
        .title {
            font-size: 28px;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 15px 0;
            background: #212529;
            border-radius: 10px;
            margin-bottom: 5px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        }

        /* Quote Styling */
        .quote {
            font-size: 18px;
            font-style: italic;
            color: #ffffff;
            text-align: center;
            padding: 10px;
            background: #343a40;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        }

        /* Footer Styling */
        .footer {
            text-align: center;
            padding: 15px;
            font-size: 16px;
            color: white;
            background: #212529;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0px -4px 10px rgba(0, 0, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">💬Career Advisor Chatbot</div>', unsafe_allow_html=True)

# Quote for inspiration
st.markdown('<div class="quote">"The future belongs to those who believe in the beauty of their dreams." – Eleanor Roosevelt</div>', unsafe_allow_html=True)

# Function to generate AI response
def generate(prompt, history):
    client = Groq(api_key="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")
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful career advisor for students. You will go step by step..."
            },
            {
                "role": "user",
                "content": f"Conversation history: {history}. Prompt: {prompt}",
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        top_p=1,
        stop=None,
        stream=True,
    )
    output = "" 
    for chunk in stream:
        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
            output += chunk.choices[0].delta.content
    return output

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi, what is your highest education qualification and interests?"}]
if "history" not in st.session_state:
    st.session_state["history"] = ""

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f'<div class="{"user-msg" if msg["role"] == "user" else "assistant-msg"}">{msg["content"]}</div>', unsafe_allow_html=True)

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    # Display user's message
    with st.chat_message("user"):
        st.markdown(f'<div class="user-msg">{prompt}</div>', unsafe_allow_html=True)

    # Store message in session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI response
    response = generate(prompt, st.session_state.history)
    msg = response

    # Update history
    st.session_state.history += f"User: {prompt}\nAssistant: {msg}\n"

    # Store AI response and display it
    st.session_state.messages.append({"role": "assistant", "content": msg})
    with st.chat_message("assistant"):
        st.markdown(f'<div class="assistant-msg">{msg}</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">🔥 Powered by AI | Created with ❤️ for Shaping Brilliant Minds</div>', unsafe_allow_html=True)
