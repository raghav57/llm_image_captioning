# Session 12 – Multimodal AI Engineering

## Practical Project: AI Image Captioning Assistant

This project builds a browser-based application that accepts an image, inspects its numerical and visual properties, and uses a multimodal AI model to generate a natural-language description.

The application combines image processing with vision-language inference. Users upload an image through Streamlit, inspect its dimensions and RGB channels, and ask Gemini to describe the image.

---

# Project overview

## What the application does

The application follows this workflow:

1. The user uploads an image through a Streamlit interface.
2. Pillow opens the image and exposes its properties.
3. The application displays the image, dimensions, file format and colour mode.
4. The image is converted to RGB so its colour channels and pixel values can be inspected.
5. The application separates and displays the red, green and blue channels.
6. The centre pixel is inspected to show its RGB intensity values.
7. When the user requests a description, the application sends the image and a text prompt to Google's Gemini API.
8. Gemini analyses the visual content and returns a natural-language description, which Streamlit displays.

## Technology stack

| Component | Technology | Role |
|---|---|---|
| Programming language | Python 3.13 | Application logic |
| Editor | Visual Studio Code | Development environment |
| User interface | Streamlit | Browser-based application |
| Image processing | Pillow | Opening, converting and inspecting images |
| Multimodal model | Gemini 3.5 Flash-Lite | Image understanding and description generation |
| Model API | Google Gemini API | Sends image and prompt to Gemini |
| Python SDK | `google-genai` | Connects Python to the Gemini API |
| Configuration | `python-dotenv` | Loads the API key from `.env` |

## Python environment

This project uses the system installation of **Python 3.13**. A virtual environment is not used for this workshop project.

Use the Python Launcher to select Python 3.13 consistently:

```powershell
py -3.13
```

Install packages with:

```powershell
py -3.13 -m pip
```

Run the Streamlit application with:

```powershell
py -3.13 -m streamlit
```

---

# Project setup

## Create the project directory

Create the following folder:

```text
D:\genai-course\session_12_image_captioning
```

Open Visual Studio Code and select **File → Open Folder**, then open this directory.

Alternatively, open it from PowerShell:

```powershell
code D:\genai-course\session_12_image_captioning
```

## Verify Python 3.13

Open the integrated terminal in VS Code using **Terminal → New Terminal** and run:

```powershell
py -3.13 --version
```

The output should show Python 3.13.x. The patch version may differ.

## Project files

The project directory should contain the following files:

```text
session_12_image_captioning/
│
├── app.py
├── image_captioner.py
├── test_gemini_connection.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── sample.jpg
```

File responsibilities:

| File | Purpose |
|---|---|
| `app.py` | Streamlit interface, image inspection and Gemini description generation |
| `image_captioner.py` | Reserved for separating model-calling logic as the application evolves; it may remain unused at this stage |
| `test_gemini_connection.py` | Standalone test of the Gemini API using a sample image |
| `requirements.txt` | Python package dependencies |
| `.env` | Private configuration, including the Gemini API key |
| `.gitignore` | Excludes secrets and generated files from version control |
| `README.md` | Project documentation |
| `sample.jpg` | Sample image used to test image understanding |

---

# Install the Python dependencies

Add the following packages to `requirements.txt`:

```text
streamlit
pillow
python-dotenv
google-genai
```

What each package provides:

- **Streamlit:** Creates the browser-based user interface.
- **Pillow:** Opens, converts and inspects image files.
- **python-dotenv:** Loads configuration values from the local `.env` file.
- **google-genai:** Google's official Python SDK for accessing the Gemini API.

Install or update the dependencies:

```powershell
py -3.13 -m pip install --upgrade pip
py -3.13 -m pip install -r requirements.txt
```

To verify the packages:

```powershell
py -3.13 -m pip show streamlit pillow python-dotenv google-genai
```

If `google-genai` was installed separately during development, listing it in `requirements.txt` ensures that the dependency is documented and can be installed again on another machine.

---

# Configure the Google Gemini API key

The application uses the Gemini API to send an image and a prompt to Gemini 3.5 Flash-Lite. The API key authenticates the application.

## Create an API key in Google AI Studio

1. Open Google AI Studio: https://aistudio.google.com/
2. Sign in with your Google account.
3. Open the API keys page: https://aistudio.google.com/api-keys
4. Review the available Google AI Studio projects.
5. Select an existing project or create a project if prompted.
6. Select **Create API key**.
7. Choose the relevant Google Cloud project if asked.
8. Copy the generated API key and store it securely.

If you already have multiple API keys, you only need one for this project. Choose an active key associated with the intended project. There is no need to create additional keys just for this application.

Google may change the labels or layout in AI Studio over time, so follow the current on-screen instructions if they differ slightly.

## Store the key in `.env`

In the project root, open `.env` and add:

```text
GEMINI_API_KEY=your_actual_api_key_here
```

Replace the placeholder with the key you generated. Do not include the placeholder text itself.

Keep the key private:

- Do not paste it into source code.
- Do not share it in screenshots, notebooks, chat messages or public repositories.
- Do not commit `.env` to Git.
- If the key is exposed, revoke it in Google AI Studio and create a replacement.
- Do not delete or rotate a key that another application depends on without checking first.

The `.env` file should be in the project directory from which you run the Python script.

## Configure `.gitignore`

Ensure `.gitignore` contains:

```text
__pycache__/
.env
*.pyc
```

This prevents the local API key file and Python-generated cache files from being committed accidentally.

---

# Connect Python to Gemini

## Initialise the Gemini client

The Google Gen AI SDK is imported using:

```python
from google import genai
```

Load the environment variable and create the client:

```python
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)
```

Key concepts:

- `load_dotenv()` reads values from the local `.env` file.
- `os.getenv("GEMINI_API_KEY")` retrieves the key without hardcoding it in the Python source.
- The check prevents the application from continuing when the key is missing.
- `genai.Client()` creates the client used to make Gemini API requests.

## Select the model

The application uses:

```python
MODEL_ID = "gemini-3.5-flash-lite"
```

The model identifier is passed to the SDK when generating content. Model availability, quotas and pricing can depend on Google's current API offering and the Google Cloud project configuration.

Official model documentation: https://ai.google.dev/gemini-api/docs/models

## Test the API using a sample image

Create `test_gemini_connection.py`:

```python
import os
from dotenv import load_dotenv
from PIL import Image
from google import genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Initialise Gemini client
client = genai.Client(api_key=API_KEY)

print("Gemini client initialised successfully!")

# Load the sample image
image = Image.open("sample.jpg").convert("RGB")

print("Image loaded successfully:", image.size)

# Define the image description prompt
prompt = """
Describe this image.

Identify:
1. The main subject
2. The surroundings
3. Important visual details

Write a clear and concise description.
"""

# Send the prompt and image to Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=[prompt, image]
)

# Display the generated description
print("\nGemini Image Description:")
print(response.text)
```

Run the test from the project directory:

```powershell
py -3.13 test_gemini_connection.py
```

A successful run should:

1. Initialise the Gemini client.
2. Load `sample.jpg`.
3. Send the prompt and image to Gemini.
4. Print the generated image description.

The exact description will vary depending on the sample image and model response.

### Understand the multimodal request

The central API call is:

```python
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=[prompt, image]
)
```

The `contents` argument contains both text and image input. The SDK accepts the Pillow image object directly in this example. We do not manually convert the image into Base64.

`response.text` provides the generated text from the model response.

---

# Build the Streamlit image inspection interface

The application accepts images in JPEG, PNG and WEBP formats and uses Pillow to inspect their properties.

## Configure the Streamlit page

The application imports the required libraries:

```python
import os
import streamlit as st

from dotenv import load_dotenv
from google import genai
from PIL import Image
```

The page is configured using:

```python
st.set_page_config(
    page_title="AI Image Captioning Assistant",
    page_icon="🖼️",
    layout="wide"
)
```

The page title, browser tab icon and wide layout are set here. This configuration should appear before other Streamlit elements are rendered.

## Add the image uploader

```python
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"]
)
```

`st.file_uploader()` displays a file upload control in the browser. The `type` argument restricts the file types accepted by this interface.

The returned object is file-like and can be passed to Pillow.

## Open and display the uploaded image

```python
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Your uploaded image",
        width=500
    )
```

The `if` condition ensures that the image is opened only after a file has been uploaded.

`Image.open()` returns a Pillow Image object. This object exposes properties such as width, height, format and colour mode.

## Inspect image properties

```python
st.metric("Width", f"{image.width} px")
st.metric("Height", f"{image.height} px")
st.metric("Format", image.format or "Unknown")

st.write("Colour Mode:", image.mode)
```

Important properties:

- `image.width`: number of pixels horizontally.
- `image.height`: number of pixels vertically.
- `image.format`: file encoding format, such as JPEG, PNG or WEBP.
- `image.mode`: representation of the image's colour information.

Common Pillow colour modes include:

| Mode | Meaning |
|---|---|
| `RGB` | Red, Green and Blue channels |
| `RGBA` | Red, Green, Blue and Alpha (transparency) |
| `L` | Grayscale intensity |
| `P` | Palette-based image |

File format and colour mode are different concepts. For example, a PNG file may use RGB, RGBA or a palette-based mode.

## Convert the image to RGB

```python
rgb_image = image.convert("RGB")
```

This creates an RGB representation of the image. It ensures that subsequent pixel inspection returns three colour values.

For an RGBA image, the alpha channel is not retained in this RGB conversion.

This operation does not resize the image or normalize its pixel values.

## Separate the RGB channels

```python
red, green, blue = rgb_image.split()
```

This produces three single-channel images. Each channel represents the intensity of one colour component at every pixel location.

For a typical 8-bit channel:

- `0` represents no intensity for that channel.
- `255` represents maximum intensity for that channel.

The channel images are displayed in grayscale. Their brightness represents the intensity of the corresponding colour channel.

## Inspect a pixel

```python
x = rgb_image.width // 2
y = rgb_image.height // 2

pixel_value = rgb_image.getpixel((x, y))
```

This selects the centre pixel of the image.

For an RGB image, the returned value is a tuple such as:

```python
(125, 180, 95)
```

This represents:

- Red intensity: 125
- Green intensity: 180
- Blue intensity: 95

The coordinate order for `getpixel()` is `(x, y)`, meaning horizontal position followed by vertical position.

---

# Generate an image description with Gemini

Once an image is uploaded and inspected, the user can request a natural-language description.

## Load the API key and initialise the client

At the beginning of `app.py`, load the key and initialise Gemini:

```python
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found in .env")
    st.stop()

client = genai.Client(api_key=API_KEY)

MODEL_ID = "gemini-3.5-flash-lite"
```

The client is initialised once when the Streamlit script runs. Streamlit reruns the script after user interactions, so the client setup is part of the application initialisation.

## Add the description button

The following code belongs inside the uploaded-image block, after the image inspection section:

```python
st.subheader("AI Image Description")

if st.button("Generate Image Description"):

    prompt = """
    Analyse the uploaded image and provide:

    1. Main subject: What is the image primarily about?
    2. Surroundings: Describe the environment and background.
    3. Visual details: Identify important objects, colours,
       people, activities, and other relevant details.
    4. Overall description: Provide a concise natural-language
       description of the image.

    Be accurate. Do not invent details that are not visible.
    """

    try:
        with st.spinner("Gemini is analysing your image..."):

            response = client.models.generate_content(
                model=MODEL_ID,
                contents=[prompt, rgb_image]
            )

        st.markdown("### Generated Description")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error generating image description: {e}")
```

## Understand the inference flow

- `st.button()` creates a button and runs the enclosed code when clicked.
- The prompt gives Gemini instructions about the content and structure of the description.
- `st.spinner()` provides visual feedback while the API request is running.
- `client.models.generate_content()` sends the prompt and RGB image to the selected Gemini model.
- `response.text` extracts the generated text for display.
- `try/except` catches request or processing errors and displays a message rather than leaving the user with an unhandled traceback.

The image is sent to Gemini only when the user clicks the button.

---

# Run and test the application

Start Streamlit from the project directory:

```powershell
py -3.13 -m streamlit run app.py
```

Streamlit normally opens the application in your browser. If it does not, use the local URL printed in the terminal, usually:

```text
http://localhost:8501
```

Test the application:

1. Upload a JPEG, PNG or WEBP image.
2. Confirm that the uploaded image is displayed.
3. Review the width, height, file format and original colour mode.
4. Inspect the three RGB channel images.
5. Review the centre pixel coordinates and RGB values.
6. Click **Generate Image Description**.
7. Wait for Gemini to analyse the image.
8. Review the generated description.

To stop the Streamlit server, return to the terminal and press `Ctrl + C`.

---

# Important technical boundaries

- Pillow is used to open and inspect the uploaded image.
- Converting an image to RGB is a colour-mode conversion; it is not the same as resizing or normalizing pixel values.
- The RGB channel inspection is an educational view of image data. It is not a custom vision-model feature extractor.
- The application sends a Pillow image object and a text prompt to Gemini through the Google Gen AI SDK.
- The model performs the multimodal interpretation. The application does not implement its own vision encoder.
- The generated description is a model output and may contain errors. It should not be treated as a guaranteed factual account of every detail in the image.

---

# Troubleshooting

| Problem | Suggested action |
|---|---|
| `py -3.13` is not recognised | Verify Python 3.13 installation and Windows Python Launcher configuration. |
| `No module named streamlit` | Run `py -3.13 -m pip install -r requirements.txt`. |
| `No module named PIL` | Install Pillow using `py -3.13 -m pip install pillow`. |
| `No module named dotenv` | Install `python-dotenv` using `py -3.13 -m pip install python-dotenv`. |
| `No module named google` | Install the SDK using `py -3.13 -m pip install google-genai`. |
| `GEMINI_API_KEY not found in .env` | Check the `.env` filename, its location, the variable spelling and the current working directory. |
| Gemini returns an authentication error | Check that the API key is valid, active and associated with the intended Google AI Studio project. Do not share the key. |
| Gemini returns a model-not-found error | Check the model identifier and Google's current model documentation. |
| Gemini returns a quota or rate-limit error | Review the project's current API quota and usage in Google AI Studio or Google Cloud. |
| Image cannot be opened | Confirm that the file is a valid supported image. Try another JPEG or PNG. |
| Streamlit command is not found | Use `py -3.13 -m streamlit run app.py`. |
| Browser does not open | Use the local URL printed in the Streamlit terminal. |
| Port 8501 is occupied | Stop the other Streamlit process or run `py -3.13 -m streamlit run app.py --server.port 8502`. |

---

# Learning outcomes

After building and testing this application, students should be able to:

1. Set up a Python application project and manage dependencies.
2. Build and run a browser-based interface using Streamlit.
3. Store API credentials securely using environment variables.
4. Generate an API key using Google AI Studio.
5. Initialise the Google Gen AI Python client.
6. Load images using Pillow.
7. Inspect image dimensions, formats and colour modes.
8. Convert images to RGB and separate colour channels.
9. Retrieve individual pixel values.
10. Send an image and a text prompt to a multimodal model.
11. Generate and display a natural-language image description.
12. Handle loading states and API errors in an AI application.

## Official references

- Google AI Studio: https://aistudio.google.com/
- Google AI Studio API keys: https://aistudio.google.com/api-keys
- Gemini API documentation: https://ai.google.dev/gemini-api/docs
- Gemini model documentation: https://ai.google.dev/gemini-api/docs/models
- Google Gen AI Python SDK: https://github.com/googleapis/python-genai
- Streamlit documentation: https://docs.streamlit.io/
- Pillow documentation: https://pillow.readthedocs.io/

---

**Project status:** The image upload, image inspection and Gemini-powered image description workflow are implemented and working.
