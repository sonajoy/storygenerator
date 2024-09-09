import streamlit as st
import requests

# Define your API key and endpoint
api_key = 'AIzaSyAhAEsUOgZxiR4b77fFkX2tdNbzQmywdlU'
endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

# Function to generate a story
def generate_story(prompt):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'contents': [
            {
                'parts': [
                    {'text': prompt}
                ]
            }
        ]
    }
    response = requests.post(f"{endpoint}?key={api_key}", headers=headers, json=data)
    response.raise_for_status()
    
    response_data = response.json()
    
    if response_data.get('candidates', [{}])[0].get('finishReason') == 'SAFETY':
        return 'Content was blocked due to safety concerns. Please try a different prompt.'
    
    try:
        content_parts = response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])
        return ' '.join(part.get('text', '') for part in content_parts)
    except (IndexError, KeyError):
        return 'No story generated'

# Streamlit interface
def main():
    # Custom CSS for styling
    st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    .header {background-color: #3498db; color: white; padding: 20px; text-align: center; border-radius: 10px;}
    .text {color: #333;}
    .container {background-color: white; border-radius: 15px; padding: 30px; margin: 20px auto; width: 80%; box-shadow: 0px 6px 12px rgba(0,0,0,0.1);}
    .input-container {margin-top: 20px; margin-bottom: 20px;}
    .button {background-color: #3498db; color: white; border: none; border-radius: 5px; padding: 12px 24px; cursor: pointer; font-size: 16px;}
    .button:hover {background-color: #2980b9;}
    .textarea {margin-top: 20px; border-radius: 5px; border: 1px solid #ddd; padding: 10px;}
    .image {display: block; margin: 0 auto;}
    </style>
    """, unsafe_allow_html=True)

    # Displaying a logo image (replace 'logo.png' with your image file)
    # st.image('logo.png', width=200, caption="Story Generator")

    # Title and introduction
    st.markdown('<div class="header"><h1>🌟 Story Generator with Google Gemini API 🌟</h1></div>', unsafe_allow_html=True)
    st.write("Generate unique stories with a touch of magic! ✨")

    # Main layout for generating and displaying the story
    st.markdown('<div class="container">', unsafe_allow_html=True)
    prompt = st.text_area("Story Prompt", "Write a story about a group of friends who discover a hidden treasure map and embark on an exciting adventure to find it.", height=200, key="prompt", help="Enter your story prompt here. Be creative!")

    if st.button("Generate Story", key="generate_button"):
        with st.spinner("Generating your story..."):
            try:
                story = generate_story(prompt)
                st.write("### Generated Story:")
                st.write(story)
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

if _name_ == "_main_":
    main()
