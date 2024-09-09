import streamlit as st
from transformers import pipeline, TFAutoModelForCausalLM, AutoTokenizer

# Cache the model and tokenizer loading to avoid reloading every time the app is rerun
@st.cache_resource
def load_model():
    model_name = "gpt2-medium"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

# Load the model and tokenizer
model, tokenizer = load_model()

# Initialize the text generation pipeline
generator = pipeline(
    'text-generation', 
    model=model, 
    tokenizer=tokenizer,
    max_length=300,
    temperature=0.7, 
    top_p=0.95,
    top_k=50,
    repetition_penalty=1.2
)

# Streamlit UI
st.set_page_config(page_title="Story Generator", page_icon=":book:", layout="wide")

# Custom CSS to enhance the UI
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .title {
        font-size: 2.5em;
        color: #2d3436;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        padding: 10px;
        background: linear-gradient(90deg, #74b9ff, #a29bfe);
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .description {
        font-size: 1.2em;
        color: #636e72;
        text-align: center;
        margin-bottom: 30px;
        padding: 0 20px;
    }
    .stTextInput {
        background-color: #e0f7fa;
        border: 2px solid #00796b;
        border-radius: 5px;
        padding: 10px;
    }
    .stButton {
        background-color: #009688;
        color:#00796 ;
        font-weight: bold;
        border-radius: 5px;
        padding: 8px 16px;
        border: none;
        cursor: pointer;
        font-size: 0.9em;
    }
    .stButton:hover {
        background-color: #00796b;
    }
    .story-output {
        border: 2px solid #dfe6e9;
        border-radius: 15px;
        padding: 20px;
        background-color: #ffffff;
        font-family: 'Georgia', serif;
        font-size: 1.2em;
        line-height: 1.8;
        white-space: pre-wrap;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 800px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Story Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Generate a creative and engaging story using an LLM model!</div>', unsafe_allow_html=True)

# User input for story prompt
prompt = st.text_input("Enter a prompt for your story:", "")

# User input for story length
max_length = st.slider("Select the maximum length of the story:", min_value=100, max_value=1000, value=300)

# Generate story when the button is clicked
if st.button("Generate Story"):
    if prompt:
        # Show spinner while generating the story
        with st.spinner("Generating your story..."):
            refined_prompt = f"Once upon a time, {prompt}"
            stories = generator(refined_prompt, max_length=max_length, num_return_sequences=1)
            
        # Display the story in a styled format
        st.markdown(f'<div class="story-output">{stories[0]["generated_text"]}</div>', unsafe_allow_html=True)
    else:
        st.write("Please enter a prompt to generate a story.")
