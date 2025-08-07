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
import asyncio
import streamlit.components.v1 as components
from openai import OpenAI
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM with streaming enabled
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    streaming=True
)

# Define the system prompt for a kid-friendly Python tutor
system_template = """
You are a friendly Python tutor for kids aged 6-12. Explain Python in a very simple and clear way, like telling a fun story. Let’s learn data structures first! Follow these instructions exactly:

- Start by teaching basic data structures (Module 1: variables, lists) with lots of practice, using examples like variables as superhero boxes or lists as toy collections.
- After data structures, move to Module 2 (basic operations: addition, subtraction), then Module 3 (loops), then Module 4 (conditionals), and so on.
- Use examples with things kids like, such as games, animals, or superheroes.
- Keep answers to one or two short sentences.
- Only answer questions about Python; if the question is not about Python, say, "Let’s learn some Python!"
- Include a small, simple code example when it helps, like `hero = "Spider-Man"` for variables.
- Remember what the child has learned and suggest the next topic, like "You know variables! Want to try lists?"
- End with a fun question like "Want to make a list of superhero powers?"
- Avoid any inappropriate content, like violence or complex ideas.
- Do not include formatting characters like ** or * in responses.
"""

# Set up the prompt template with history and input variables
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{history}\n{input}")
])

# Initialize session state for conversation memory and cache
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "response_cache" not in st.session_state:
    st.session_state.response_cache = {}

# Create the conversation chain
conversation = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=st.session_state.memory,
    input_key="input"
)

# Asynchronous function to convert text to speech
async def async_text_to_speech(text):
    loop = asyncio.get_event_loop()
    def generate_audio():
        tts = gTTS(text=text, lang='en')
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return base64.b64encode(audio_bytes.read()).decode('utf-8')
    return await loop.run_in_executor(None, generate_audio)

# Synchronous function for Whisper transcription
def transcribe_audio(audio_file_path, api_key):
    try:
        client = OpenAI(api_key=api_key)
        with open(audio_file_path, "rb") as audio_file:
            logger.info(f"Transcribing audio file: {audio_file_path}")
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
        logger.info(f"Transcription successful: {transcript.text}")
        return transcript.text
    except Exception as e:
        logger.error(f"Whisper transcription failed: {str(e)}")
        raise Exception(f"Whisper transcription failed: {str(e)}")

# Custom HTML for auto-playing audio with fallback
def play_audio(audio_base64):
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    components.html(audio_html, height=0)

# Streamlit app
st.title("Python Tutor Bot for Kids")
st.write("Hello! I'm your Python teacher. Let’s learn data structures first! Click 'Ready' to start, or ask about Python by typing or using your microphone.")
st.write("Note: If voice doesn't work, please check your browser's microphone permissions or type your question.")

# Ready button to start learning
if st.button("Ready"):
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Great! A variable is like a box for Spider-Man's web! Try this: `hero = \"Spider-Man\"`. Want to practice variables?",
        "audio": asyncio.run(async_text_to_speech("Great! A variable is like a box for Spider-Man's web! Try this: hero equals Spider-Man. Want to practice variables?"))
    })

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "audio" in message:
            play_audio(message["audio"])

# Voice input
st.write("Record your question:")
try:
    audio_bytes = audio_recorder(
        text="Click to record",
        energy_threshold=(100, 3000),
        pause_threshold=2.0,
        sample_rate=44100
    )
    if audio_bytes:
        logger.info("Audio recorded successfully")
    else:
        logger.warning("No audio bytes recorded")
except Exception as e:
    logger.error(f"Audio recorder failed: {str(e)}")
    st.error(f"Sorry, I couldn't record your voice: {str(e)}. Please check microphone permissions or type your question.")

# Text input
user_input = st.chat_input("Or type your question here")

# Process input (voice or text)
input_text = None
if audio_bytes:
    with st.spinner("Listening to your question"):
        # Save audio to temporary file
        temp_file = "temp_audio.wav"
        try:
            with open(temp_file, "wb") as f:
                f.write(audio_bytes)
            # Use OpenAI Whisper for transcription
            input_text = transcribe_audio(temp_file, os.getenv("OPENAI_API_KEY"))
            st.session_state.messages.append({"role": "user", "content": input_text})
            with st.chat_message("user"):
                st.markdown(input_text)
        except Exception as e:
            logger.error(f"Audio processing error: {str(e)}")
            st.error(f"Sorry, I couldn't understand: {str(e)}. Please try speaking again or type your question.")
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
elif user_input:
    input_text = user_input
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"):
        st.markdown(input_text)

# Process bot response
if input_text:
    try:
        # Check cache for response
        cache_key = input_text.lower().strip()
        if cache_key in st.session_state.response_cache:
            response, audio_base64 = st.session_state.response_cache[cache_key]
            with st.chat_message("assistant"):
                st.markdown(response)
                play_audio(audio_base64)
        else:
            # Stream response
            response_container = st.chat_message("assistant")
            response_text = ""
            with response_container:
                response_placeholder = st.empty()
                for chunk in conversation.stream(input_text):
                    response_text += chunk.get("response", "")
                    response_placeholder.markdown(response_text)
            # Generate audio asynchronously
            with st.spinner("Making audio"):
                audio_base64 = asyncio.run(async_text_to_speech(response_text))
            # Cache response
            st.session_state.response_cache[cache_key] = (response_text, audio_base64)
            # Auto-play audio
            play_audio(audio_base64)
            # Store in session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "audio": audio_base64
            })
    except Exception as e:
        logger.error(f"Response processing error: {str(e)}")
        st.error(f"Sorry, something went wrong: {str(e)}")