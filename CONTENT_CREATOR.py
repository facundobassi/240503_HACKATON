import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession
import streamlit as st

from vertexai.preview.vision_models import Image, ImageGenerationModel
from IPython.display import Image
import streamlit as st
import time
import json
import os
from google.oauth2.service_account import Credentials

from google.cloud import aiplatform

st.set_page_config(layout="wide")
# Add the app name in the header

st.image("VibezAl-horizontal with text.svg", width=200)

# Add the app name in the sidebar
st.sidebar.image("VibezAl-horizontal with text.svg", width=100)


# #Authentication on server
# if st.toggle("Deployed app", False):

# Get the JSON string from environment variable
service_account_key_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

# Replace \\n and \" back to newlines and double quotes
service_account_key_json = service_account_key_json.replace('\\n', '\n').replace('\\"', '"')

# Parse the JSON string back to a dictionary
service_account_key = json.loads(service_account_key_json, strict=False)

# Create credentials from the service account key
credentials = Credentials.from_service_account_info(service_account_key)

# Use the credentials
client = aiplatform.gapic.PredictionServiceClient(credentials=credentials)
# st.write(client)



project_id = "lognos-agent"
location = "us-central1"

vertexai.init(project=project_id, location=location, credentials=credentials)

model = GenerativeModel("gemini-1.0-pro")
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()

model2 = ImageGenerationModel.from_pretrained("imagegeneration@005")

def get_chat_response(chat: ChatSession, prompt: str):
    response = chat.send_message(prompt)
    return response.text

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("##### CONTENT CREATOR")

col1, col2 = st.columns([5, 5])

# Define parameters and options
st.session_state.platforms_list = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'Pinterest', 'email marketing', 'Reddit']
st.session_state.tones_list = ['Engaging', 'Informative', 'Funny', 'Argumentative', 'Sarcastic']
st.session_state.target_audiences_list = ['General Public', 'Specific Demographics', 'Niche Communities']
st.session_state.age_groups_list = ['All','Children', 'Teenagers', 'Young Adults', 'Adults', 'Seniors']
st.session_state.gender_list = ['All', 'Male', 'Female', 'Non-binary']
st.session_state.niche_communities_list = ['All', 'Tech', 'Fashion', 'Food', 'Travel', 'Fitness', 'Health', 'Finance', 'Education', 'Entertainment', 'Sports', 'Politics', 'Religion', 'Science', 'Environment', 'Lifestyle', 'Parenting', 'Pets', 'Art', 'Music', 'Movies', 'Books', 'Gaming', 'Beauty', 'DIY', 'Crafts', 'Photography', 'Cars', 'Real Estate', 'Home Decor', 'Gardening', 'Mental Health', 'Dating', 'Career', 'Business', 'Marketing', 'Social Media', 'News', 'History', 'Culture', 'Language', 'Fashion', 'Shopping', 'Design', 'Architecture', 'Engineering', 'Agriculture', 'Legal', 'Medicine', 'Psychology', 'Sociology', 'Philosophy', 'Literature', 'Writing', 'Journalism', 'Public Relations', 'Advertising', 'Sales', 'Customer Service', 'Human Resources', 'Management', 'Leadership', 'Productivity', 'Motivation', 'Inspiration', 'Self-improvement', 'Self-care', 'Self-love', 'Self-esteem', 'Self-confidence', 'Self-discipline', 'Self-awareness', 'Self-regulation', 'Self-control', 'Self-compassion', 'Self-acceptance', 'Self-forgiveness', 'Self-empowerment', 'Self-realization', 'Self-actual']
st.session_state.lengths_list = ['Short (50-70 words)','Medium (100-120 words)', 'Long (200-250 words)', 'X/Tweet Max (280 characters)']
st.session_state.hashtags_options_list = ['Include', 'Exclude', 'Specific Hashtags']
st.session_state.emotions_list = ['Exciting','Happiness', 'Sadness', 'Anger', 'Fear', 'Surprise']
st.session_state.call_to_actions_list = ['Share', 'Like', 'Comment', 'Debate', 'Donate']

st.session_state.age_group = 'All'
st.session_state.gender = 'All'
st.session_state.niche_community = 'All'

with col1:
    with st.expander("PREFERENCES", expanded=True):
        if "response2" in st.session_state:
            st.session_state.prompt2 = st.text_input("Subject", st.session_state.prompt2)
            # "Previous"
            # st.markdown(st.session_state.response2)
        else:
            st.session_state.prompt2 = st.text_area("Subject",)
        
        #Creates the context for the content
        col11, col12 = st.columns([1, 1])
        with col11:
            st.session_state.target_audience = st.selectbox("Target Audience", st.session_state.target_audiences_list)
            if st.session_state.target_audience == "Specific Demographics":
                    st.session_state.age_group = st.selectbox("Age Group", st.session_state.age_groups_list, index=0)
                    st.session_state.gender = st.selectbox("Gender", st.session_state.gender_list, index=0)
            elif st.session_state.target_audience == "Niche Communities":
                    st.session_state.niche_community = st.selectbox("Niche Community", st.session_state.niche_communities_list, index=0 )
            st.session_state.tone = st.selectbox("Tone", st.session_state.tones_list)
            st.session_state.call_to_action = st.selectbox("Call to Action", st.session_state.call_to_actions_list)           
        
        with col12:
            st.session_state.length = st.selectbox("Length", st.session_state.lengths_list)
            st.session_state.emotion = st.selectbox("Emotion", st.session_state.emotions_list)
            st.session_state.custom_hashtags = st.text_input("Custom Hashtags (comma separated)")


        with col11:
            if st.toggle("Generate Hashtags", False):
                st.session_state.hashtags_option = "Generate hashtags"
            else:
                st.session_state.hashtags_option = "Do not generate hashtags"

        with col12:
            st.session_state.create_image = st.toggle("Create Image", False)
            if st.session_state.create_image:
                st.session_state.user_image_prompt = st.text_input("Tell us more about the image...", label_visibility= "visible")

            st.session_state.context = f"Create a post considering the following parameters: Tone: {st.session_state.tone}\nTarget Audience: {st.session_state.target_audience} (Gender:{st.session_state.gender}; age group: {st.session_state.age_group}; niche community: {st.session_state.niche_community} )\nLength: {st.session_state.length}\nEmotion: {st.session_state.emotion}\nCall to Action: {st.session_state.call_to_action}\nHashtags: {st.session_state.hashtags_option} and use {st.session_state.custom_hashtags}\n. Start the response with the post title and do not mention it is a post. Subject and additional context: "

        colb11, colb12 = st.columns([1, 1])
        # Create a progress bar
        bar_text_variable = ""
        progress_bar = st.progress(0,bar_text_variable)
        with colb11:
            if st.button("Create Post"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": st.session_state.prompt2})
                # Display the progress bar as indeterminate
                bar_text_variable = st.text("Generating post prompt...")
                for i in range(100):
                    progress_bar.progress(i + 1)
                    time.sleep(0.01)

                st.session_state.response2 = get_chat_response(st.session_state.chat, st.session_state.context+st.session_state.prompt2)

                if st.session_state.create_image:
                    st.session_state.pre_prompt_image = f"I'm promoting {st.session_state.prompt2} online, and I need to generate an image of it. I need the image to be compelling and interesting to convince people to buy. Can you create a prompt I can use with Vertex? It's to generate an image for {st.session_state.context+st.session_state.prompt2}. Also consider the following for the image prompt: {st.session_state.user_image_prompt}. Respond with only the prompt, no other text. Be as verbose as possible."
                    # Display the progress bar as indeterminate
                    bar_text_variable = st.text("Generating image prompt...")
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(0.01)

                    # Execute the line of code
                    st.session_state.prompt_image = get_chat_response(st.session_state.chat, st.session_state.pre_prompt_image)
                    progress_bar.empty()

    if "response2" in st.session_state:
        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.response2})
    
with col2:
    col21, col22, col23 = st.columns([1, 20, 1])
    if "response2" in st.session_state: 
        with col22:
            st.info(st.session_state.response2)
        
        if st.session_state.create_image:
            with col22:
                try:
                    bar_text_variable = st.text("Working on the image...")
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(0.01)

                    st.session_state.images = model2.generate_images(prompt=st.session_state.prompt_image)
                    st.session_state.images[0].save(location="./gen-img1.png", include_generation_parameters=True)
                    progress_bar.empty()

                    st.image('./gen-img1.png', use_column_width="always")
                except:
                    st.warning("The generated content may violate Gemini models policies. Please try regenerating the image.")

            with col22:
                if st.button("Regenerate image"):
                    try:
                        bar_text_variable = st.text("Reworking the image...")
                        for i in range(100):
                            progress_bar.progress(i + 1)
                            time.sleep(0.01)
                        
                        st.session_state.images = model2.generate_images(prompt=st.session_state.prompt_image)
                        progress_bar.empty()
                        st.session_state.images[0].save(location="./gen-img1.png", include_generation_parameters=True)
                    except:
                        st.warning("Sorry. The generated content may violate Gemini models policies. Please refresh and review your prompts.")
        #                 st.image('./gen-img1.png', use_column_width="always")
        # st.image('./gen-img1.png', use_column_width="always")    