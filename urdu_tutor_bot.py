import streamlit as st
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from gtts import gTTS
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Define the system prompt for a kid-friendly Urdu letter tutor
system_template = """
You are a friendly Urdu letter tutor for 5-year-old kids. Teach Urdu letters (حروف تہجی) in a very simple and fun way, like telling a story. Use examples with things kids like, such as animals, fruits, or toys. Avoid hard words and keep answers very short. Remember which letters the child has learned and suggest the next letter when it fits, like "You learned ا, want to try ب next?" If they ask something not about Urdu letters, kindly bring them back to learning letters. Include a simple example, like "ا is for آم (mango)." End with a fun question like "Want to learn a letter for a bird?"
"""

# Set up the prompt template with history and input variables
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{history}\n{input}")
])

# Initialize session state for conversation memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create the conversation chain
conversation = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=st.session_state.memory,
    input_key="input",
    memory_key="history"
)

# Function to convert text to speech using gTTS with Urdu support
def text_to_speech(text):
    tts = gTTS(text=text, lang='ur')  # Set language to Urdu
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    audio_base64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
    return audio_base64

# Streamlit app
st.title("Urdu Letter Tutor Bot for Kids")
st.write("Hello! I'm your Urdu letter teacher. Ask me about Urdu letters by typing or using your microphone. Try asking 'What is ا?' or 'Tell me about ب.' Let's learn together.")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "audio" in message:
            st.audio(f"data:audio/mp3;base64,{message['audio']}", format="audio/mp3")

# Voice input
st.write("Record your question:")
audio_bytes = audio_recorder(
    text="Click to record",
    energy_threshold=(100, 3000),
    pause_threshold=2.0,
    sample_rate=44100
)

# Text input
user_input = st.chat_input("Or type your question here")

# Process input (voice or text)
input_text = None
if audio_bytes:
    with st.spinner("Listening to your question"):
        # Save audio to temporary file
        temp_file = "temp_audio.wav"
        with open(temp_file, "wb") as f:
            f.write(audio_bytes)
        # Use OpenAI Whisper for transcription
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            with open(temp_file, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="ur"  # Set transcription language to Urdu
                )
            input_text = transcript.text
            st.session_state.messages.append({"role": "user", "content": input_text})
            with st.chat_message("user"):
                st.markdown(input_text)
            os.remove(temp_file)
        except Exception as e:
            st.error(f"Sorry, I couldn't understand: {str(e)}")
elif user_input:
    input_text = user_input
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"):
        st.markdown(input_text)

# Process bot response
if input_text:
    try:
        with st.spinner("Thinking"):
            response = conversation.run(input_text)
        with st.spinner("Making audio"):
            audio_base64 = text_to_speech(response)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "audio": audio_base64
        })
        with st.chat_message("assistant"):
            st.markdown(response)
            st.audio(f"data:audio/mp3;base64,{audio_base64}", format="audio/mp3")
    except Exception as e:
        st.error(f"Sorry, something went wrong: {str(e)}")
