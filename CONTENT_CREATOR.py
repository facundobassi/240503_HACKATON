import streamlit as st
import time

st.set_page_config(layout="wide")
st.title("VibeZAI")
st.sidebar.title("VibeZAI")

st.subheader("CONTENT CREATOR")

col1, col2 = st.columns([5, 5])

# Define parameters and options
platforms_list = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'Pinterest', 'email marketing', 'Reddit']
tones_list = ['Engaging', 'Informative', 'Funny', 'Argumentative', 'Sarcastic']
target_audiences_list = ['General Public', 'Specific Demographics', 'Niche Communities']
lengths_list = ['Short (50-70 words)','Medium (100-120 words)', 'Long (200-250 words)', 'X/Tweet Max (280 characters)']
hashtags_options_list = ['Include', 'Exclude', 'Specific Hashtags']
emotions_list = ['Exciting','Happiness', 'Sadness', 'Anger', 'Fear', 'Surprise']
call_to_actions_list = ['Share', 'Like', 'Comment', 'Debate', 'Donate']

with col1:
    with st.expander("PREFERENCES", expanded=True):
        subject = st.text_area("Subject")
        
        #Creates the context for the content
        col11, col12 = st.columns([1, 1])
        with col11:
            target_audience = st.selectbox("Target Audience", target_audiences_list)
            tone = st.selectbox("Tone", tones_list)
            call_to_action = st.selectbox("Call to Action", call_to_actions_list)           
        
        with col12:
            length = st.selectbox("Length", lengths_list)
            emotion = st.selectbox("Emotion", emotions_list)
            custom_hashtags = st.text_input("Custom Hashtags (comma separated)")

        with col11:
            generate_hashtags = st.checkbox("Generate Hashtags", False)

        with col12:
            create_image = st.checkbox("Create Image", False)
            if create_image:
                user_image_prompt = st.text_input("Tell us more about the image...", label_visibility= "visible")

        colb11, colb12 = st.columns([1, 1])
        # Create a progress bar
        progress_bar = st.progress(0)
        with colb11:
            if st.button("Create Post"):
                # Display the progress bar as indeterminate
                for i in range(100):
                    progress_bar.progress(i + 1)
                    time.sleep(0.01)

                if create_image:
                    # Display the progress bar as indeterminate
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(0.01)

with col2:
    col21, col22, col23 = st.columns([1, 20, 1])
    with col22:
        st.info("Generated post will appear here.")
        
        if create_image:
            with col22:
                st.image('./placeholder.png', use_column_width="always")
            with col22:
                if st.button("Regenerate image"):
                    st.image('./placeholder.png', use_column_width="always")

