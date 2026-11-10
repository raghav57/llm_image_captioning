# Step 1 Setup
# import streamlit as st

# st.set_page_config(
#     page_title="AI Image Captioning Assistant",
#     page_icon="🖼️",
#     layout="centered"
# )

# st.title("AI Image Captioning Assistant")

# st.write(
#     "Upload an image and let AI generate "
#     "a meaningful description."
# )

# st.success("Environment setup completed!")


import os
from dotenv import load_dotenv
from google import genai
import streamlit as st
from PIL import Image
import time

# Load environment variables
load_dotenv()

# Initialise Gemini
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found in .env")
    st.stop()

client = genai.Client(api_key=API_KEY)

MODEL_ID = "gemini-3.5-flash-lite"

# Step 2 Image Testing


# Configure Streamlit
st.set_page_config(
    page_title="AI Image Captioning Assistant",
    page_icon="🖼️",
    layout="wide"
)

# Application heading
st.title("AI Image Captioning Assistant")

st.write(
    "Upload an image to inspect its properties "
    "and understand its numerical representation."
)

# Image uploader
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"]
)

# Process uploaded image
if uploaded_file is not None:

    # Load image using Pillow
    image = Image.open(uploaded_file)

    st.subheader("Uploaded Image")

    # Display image
    st.image(
        image,
        caption="Your uploaded image",
        width=500
    )

    # Inspect image properties
    st.subheader("Image Properties")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Width", f"{image.width} px")

    with col2:
        st.metric("Height", f"{image.height} px")

    with col3:
        st.metric("Format", image.format)

    st.write("Colour Mode:", image.mode)

    # Convert image into RGB
    rgb_image = image.convert("RGB")

    # Extract RGB channels
    red, green, blue = rgb_image.split()

    st.subheader("RGB Channel Inspection")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(red, caption="Red Channel")

    with col2:
        st.image(green, caption="Green Channel")

    with col3:
        st.image(blue, caption="Blue Channel")

    # Inspect one pixel
    x = image.width // 2
    y = image.height // 2

    pixel_value = rgb_image.getpixel((x, y))

    st.subheader("Pixel Inspection")

    st.write(f"Pixel Coordinates: ({x}, {y})")
    st.write(f"RGB Values: {pixel_value}")
    
    # Gemini Image Description
    st.subheader("AI Image Description")
    
        # Prompt engineering experiments

    PROMPTS = {
            "Concise": """
            Describe this image in no more than two sentences.
            Focus on the main subject and the most important details.
            """,

            "Detailed": """
            Analyse this image in detail.
            Describe the main subjects, their appearance,
            objects, background, environment, colours,
            spatial relationships and visible activities.
            Organise your response into clear sections.
            """,

            "Descriptive": """
            Write a vivid and natural-language description
            of this image as if you were helping someone
            who cannot see it visualise the scene.
            Describe the atmosphere, setting, subjects
            and notable visual details.
            """,

            "Task-specific": """
            Analyse this image for a professional business report.
            Identify the people, objects, setting and any
            visible business-related context.
            Separate directly observable details from
            interpretations. Do not infer identities.
            """
        }

    selected_style = st.selectbox(
                "Choose a Prompting Strategy",
                list(PROMPTS.keys())
            )

    # Custom user instructions
    custom_prompt = st.text_area(
        "Add Your Own Instructions (Optional)",
        placeholder="Example: Focus on the person's clothing, posture and surroundings.",
        height=100
    )

    # Display the selected prompt
    # Combine predefined prompt and custom instructions
    final_prompt = PROMPTS[selected_style]

    if custom_prompt.strip():
        final_prompt += "\n\nAdditional User Instructions:\n" + custom_prompt

    # Display the exact prompt sent to Gemini
    st.markdown("**Final Prompt Sent to Gemini:**")

    st.code(
        final_prompt,
        language="text"
    )

    if st.button("Generate Image Description"):

        prompt = PROMPTS[selected_style]


        try:
            with st.spinner("Gemini is analysing your image..."):

                response = None

                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model=MODEL_ID,
                            contents=[final_prompt, rgb_image]
                        )
                        break

                    except Exception as e:
                        if "503" in str(e) and attempt < 2:
                            time.sleep(2 ** attempt)
                        else:
                            raise

            if response and response.text:
                st.markdown("### Generated Description")
                st.write(response.text)
            else:
                st.warning("Gemini returned an empty response.")

        except Exception as e:
            st.error(f"Error generating image description: {e}")


else:
    st.info("Please upload an image to begin.")


