import os
from PIL import Image
import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.pipelines.linear_sync_pipeline  import  LinearSyncPipeline
from lyzr_automata import Logger
from dotenv import load_dotenv; load_dotenv()

# Setup your config
st.set_page_config(
    page_title="Caption Studio",
    layout="centered",   
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Caption Studio by Lyzr")
st.markdown("### Welcome to the Caption Studio!")
st.markdown("Caption Studio by Lyzr will generates creative captions for users, and it will generates a corresponding unique image!!!")

# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Caption Studio Application

# replace this with your openai api key or create an environment variable for storing the key.
API_KEY = os.getenv('OPENAI_API_KEY')

 
open_ai_model_image = OpenAIModel(
    api_key=API_KEY,
    parameters={
        "n": 1,
        "model": "dall-e-3",
    },
)


open_ai_model_text = OpenAIModel(
    api_key= API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.5,
        "max_tokens": 1500,
    },
)

def ig_caption_studio(input_content):
    # Social Media Manager Agent
    social_media_manager_agent = Agent(
        prompt_persona="You are an expert social media manager good at writing a short and catchy instagram captions, as well creating the intagram images",
        role="social media manager",
    )


    instagram_caption_task = Task(
        name="Instagram Caption Creator",
        agent=social_media_manager_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Use the description provided and write some set of catchy 5-7 Instagram captions in 20-30 words. Use your creativity. [IMPORTANT!] Setup the events in a detailed manner",
        log_output=True,
        enhance_prompt=False,
        default_input=input_content
    )

    # Generate Intagram Image
    instagram_image_task = Task(
        name="Instagram Image Creation",
        output_type=OutputType.IMAGE,
        input_type=InputType.TEXT,
        model=open_ai_model_image,
        log_output=True,
        instructions="Generate an Instagram image for the given description. Capture every detail. Minimalistic style. [IMPORTANT!] Avoid any text or numbers in the image.",
    )

    logger = Logger()
    

    main_output = LinearSyncPipeline(
        logger=logger,
        name="Caption Generator",
        completion_message="IG Caption and Image Generated!",
        tasks=[
            instagram_caption_task,
            instagram_image_task,
        ],
    ).run()

    return main_output


if __name__ == "__main__":
    style_app() 
    caption_brief = st.text_area("Enter about caption")
    button=st.button('Submit')
    if (button==True):
        # CALL FUNCTION TO GENERATE OUTPUT
        generated_output = ig_caption_studio(caption_brief)

        # DISPLAY OUTPUT
        text_output = generated_output[0]['task_output']
        st.write(text_output)
        image_file_name = generated_output[1]['task_output'].local_file_path
        st.image(image_file_name, caption='Caption Studio') 
        
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr Automata Agent to create the Instagram captions and images. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)