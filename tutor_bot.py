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
import time

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
You are a friendly Python tutor for kids aged 6-12. Explain Python in a very simple and clear way, like telling a fun story. Follow these instructions exactly:

- Start by teaching basic data types (Module 1: strings, integers, floats, booleans) with lots of practice, using examples like strings as superhero names, integers as counting gadgets, floats as flight speeds, or booleans as true/false for superhero powers.
- After data types, move to Module 2 (data structures: lists), then Module 3 (basic operations: addition, subtraction), then Module 4 (loops), then Module 5 (conditionals), and so on.
- Use examples with things kids like, such as games, animals, or superheroes.
- Keep answers to one or two short sentences.
- Only answer questions about Python; if the question is not about Python, say, "Let’s learn some Python!"
- Include a small, simple code example when it helps, like `name = "Spider-Man"` for strings or `is_strong = True` for booleans, and wrap code in <b> tags for bolding (e.g., <b>`code`</b>).
- Remember what the child has learned and suggest the next topic, like "You know strings! Want to try integers?"
- End with a fun question like "Want to make a boolean for your favorite superhero?"
- Avoid any inappropriate content, like violence or complex ideas.
- Do not include formatting characters like ** or * in responses.
"""

# Set up the prompt template with history and input variables
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{history}\n{input}")
])

# Initialize session state for conversation memory, cache, and playback control
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "response_cache" not in st.session_state:
    st.session_state.response_cache = {}
if "last_input" not in st.session_state:
    st.session_state.last_input = None
if "is_audio_playing" not in st.session_state:
    st.session_state.is_audio_playing = False

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

# Custom HTML for auto-playing audio with playback control
def play_audio(audio_base64):
    if st.session_state.is_audio_playing:
        logger.info("Skipping audio playback as another audio is playing")
        return
    st.session_state.is_audio_playing = True
    audio_html = f"""
    <audio id="tutor_audio" autoplay onended="resetAudioPlaying()">
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    <script>
        function resetAudioPlaying() {{
            window.parent.postMessage({{type: 'audio_ended'}}, '*');
        }}
    </script>
    """
    components.html(audio_html, height=0)
    logger.info("Audio playback started")

# JavaScript listener to reset audio playback flag
components.html("""
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'audio_ended') {
        window.parent.Streamlit.setComponentValue({audio_ended: true});
    }
});
</script>
""", height=0)

# Handle audio playback completion
if st.session_state.get("audio_ended", False):
    st.session_state.is_audio_playing = False
    st.session_state.audio_ended = False
    logger.info("Audio playback completed, resetting is_audio_playing")

# Streamlit app
st.title("Python Tutor Bot for Kids")
st.write("Hello! I'm your Python teacher. Click 'Ready' in the sidebar to start learning data types, or ask about Python by typing or using your microphone.")
st.write("Note: Type or speak one question at a time to hear a clear answer! Code examples will be <b>bold</b>.")

# Sidebar for Ready button
with st.sidebar:
    if st.button("Ready"):
        response_text = "Great! A string is like a word for Spider-Man's name! Try this: <b>`name = \"Spider-Man\"`</b>. Want to practice strings?"
        audio_base64 = asyncio.run(async_text_to_speech("Great! A string is like a word for Spider-Man's name! Try this: name equals Spider-Man. Want to practice strings?"))
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "audio": audio_base64
        })
        st.session_state.last_input = "ready_button"
        logger.info("Ready button pressed, initial response generated")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)
        if message["role"] == "assistant" and "audio" in message and not st.session_state.is_audio_playing:
            play_audio(message["audio"])

# Text input
user_input = st.chat_input("Type your question here")
if user_input:
    logger.info(f"Received text input: {user_input}")

# Voice input
st.write("Or record your question:")
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

# Process input (text or voice)
input_text = None
current_input_id = str(time.time())  # Unique ID for each input
if user_input and user_input != st.session_state.last_input:
    input_text = user_input
    st.session_state.last_input = input_text
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"):
        st.markdown(input_text)
    logger.info(f"Processing text input: {input_text} (ID: {current_input_id})")
elif audio_bytes and st.session_state.last_input != "audio_input":
    with st.spinner("Listening to your question"):
        # Save audio to temporary file
        temp_file = "temp_audio.wav"
        try:
            with open(temp_file, "wb") as f:
                f.write(audio_bytes)
            # Use OpenAI Whisper for transcription
            input_text = transcribe_audio(temp_file, os.getenv("OPENAI_API_KEY"))
            st.session_state.last_input = "audio_input"
            st.session_state.messages.append({"role": "user", "content": input_text})
            with st.chat_message("user"):
                st.markdown(input_text)
            logger.info(f"Processed audio input: {input_text} (ID: {current_input_id})")
        except Exception as e:
            logger.error(f"Audio processing error: {str(e)}")
            st.error(f"Sorry, I couldn't understand: {str(e)}. Please try speaking again or type your question.")
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
else:
    logger.info("No new input received (neither text nor audio)")

# Process bot response
if input_text:
    try:
        # Use unique cache key to avoid reusing old responses
        cache_key = f"{input_text.lower().strip()}_{current_input_id}"
        if cache_key in st.session_state.response_cache:
            response, audio_base64 = st.session_state.response_cache[cache_key]
            with st.chat_message("assistant"):
                st.markdown(response, unsafe_allow_html=True)
                if not st.session_state.is_audio_playing:
                    play_audio(audio_base64)
            logger.info(f"Retrieved cached response for: {cache_key}")
        else:
            # Stream response
            response_container = st.chat_message("assistant")
            response_text = ""
            with response_container:
                response_placeholder = st.empty()
                for chunk in conversation.stream(input_text):
                    response_text += chunk.get("response", "")
                    response_placeholder.markdown(response_text, unsafe_allow_html=True)
            # Generate audio asynchronously
            with st.spinner("Making audio"):
                audio_base64 = asyncio.run(async_text_to_speech(response_text.replace("<b>", "").replace("</b>", "")))
            # Cache response
            st.session_state.response_cache[cache_key] = (response_text, audio_base64)
            # Play audio if none is currently playing
            if not st.session_state.is_audio_playing:
                play_audio(audio_base64)
            # Store in session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "audio": audio_base64
            })
            logger.info(f"Generated new response for: {cache_key}")
    except Exception as e:
        logger.error(f"Response processing error: {str(e)}")
        st.error(f"Sorry, something went wrong: {str(e)}")
    finally:
        # Clear input to prevent reprocessing
        input_text = None