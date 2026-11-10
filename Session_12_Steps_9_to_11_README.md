# Session 12 -- Multimodal AI Engineering

## Practical Project: AI Image Captioning Assistant

### Detailed Setup Guide -- Steps 9, 10 and 11

This README documents the first three implementation steps of the
Session 12 practical project. Follow the steps in order. At the end, you
will have a working Streamlit application that accepts an image,
displays it, and inspects its format, dimensions, colour mode, RGB
channels and a sample pixel.

> **Scope of this guide:** Steps 9--11 only. We prepare the Python
> project, authenticate with Hugging Face, and load/inspect images. We
> do not call Qwen2.5-VL or generate captions yet; model integration
> comes in a later step.

------------------------------------------------------------------------

# 1. Project overview

We are building an **AI Image Captioning Assistant**. The intended
end-user workflow will eventually be:

1.  Upload an image.
2.  Send the image to a vision-language model.
3.  Ask the model to describe the image.
4.  Display the generated caption in the Streamlit interface.

For the first three steps, we are preparing the application foundation.

## Technology stack

  -----------------------------------------------------------------------
  Component               Technology              Role
  ----------------------- ----------------------- -----------------------
  Language                Python 3.13             Application logic

  Editor                  Visual Studio Code      Development environment

  UI framework            Streamlit               Browser-based user
                                                  interface

  Image library           Pillow                  Opening and inspecting
                                                  images

  Model platform          Hugging Face Hub        Authentication and
                                                  hosted model access

  Configuration           python-dotenv           Loading secrets from
                                                  `.env`
  -----------------------------------------------------------------------

## Important environment decision

This workshop uses the system installation of **Python 3.13**. We are
**not creating a virtual environment** for this project.

To avoid accidentally using another installed Python version,
consistently use:

``` powershell
py -3.13
```

For package installation, use:

``` powershell
py -3.13 -m pip
```

For running the Streamlit application, use:

``` powershell
py -3.13 -m streamlit
```

------------------------------------------------------------------------

# 2. Step 9 -- Project Environment Setup

## Objective

Prepare the project folder, verify Python 3.13, install the required
packages, and launch a basic Streamlit application.

## 2.1 Create the project directory

Create the following folder:

``` text
D:\genai-course\session_12_image_captioning
```

Open Visual Studio Code, select **File → Open Folder**, and open this
directory.

You can also open the folder from PowerShell:

``` powershell
code D:\genai-course\session_12_image_captioning
```

## 2.2 Verify Python 3.13

Open the integrated terminal in VS Code:

**Terminal → New Terminal**

Run:

``` powershell
py -3.13 --version
```

Expected output will look similar to:

``` text
Python 3.13.x
```

The exact patch version may differ.

If the command fails, check that Python 3.13 is installed and available
through the Windows Python Launcher.

## 2.3 Create the project files

Create this initial structure in VS Code:

``` text
session_12_image_captioning/
│
├── app.py
├── image_captioner.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

What each file is for:

  -----------------------------------------------------------------------
  File                                Responsibility
  ----------------------------------- -----------------------------------
  `app.py`                            Streamlit user interface

  `image_captioner.py`                Model-calling and
                                      caption-generation logic in a later
                                      step

  `requirements.txt`                  List of Python package dependencies

  `.env`                              Private configuration values,
                                      including the Hugging Face token

  `.gitignore`                        Prevents secrets and generated
                                      files from being committed

  `README.md`                         Project setup and usage
                                      documentation
  -----------------------------------------------------------------------

At this point, `image_captioner.py` can remain empty. We will use it
when we begin integrating the model.

## 2.4 Add dependencies to requirements.txt

Open `requirements.txt` and add:

``` text
streamlit
huggingface_hub
pillow
python-dotenv
```

Purpose of each dependency:

-   **streamlit:** Creates the browser-based application interface.
-   **huggingface_hub:** Provides Python clients for Hugging Face Hub
    and hosted inference services.
-   **pillow:** Opens, converts and inspects image files.
-   **python-dotenv:** Loads environment variables from a local `.env`
    file.

## 2.5 Install the dependencies

Run these commands in the VS Code terminal:

``` powershell
py -3.13 -m pip install --upgrade pip
```

Then install the project dependencies:

``` powershell
py -3.13 -m pip install -r requirements.txt
```

Wait for the installation to complete. If a package is already
installed, pip may report that it is satisfied.

To verify the packages:

``` powershell
py -3.13 -m pip show streamlit huggingface_hub pillow python-dotenv
```

## 2.6 Create the initial Streamlit application

Open `app.py` and add:

``` python
import streamlit as st

st.set_page_config(
    page_title="AI Image Captioning Assistant",
    page_icon="🖼️",
    layout="centered"
)

st.title("AI Image Captioning Assistant")

st.write(
    "Upload an image and let AI generate "
    "a meaningful description."
)

st.success("Environment setup completed!")
```

### Understand the code

-   `import streamlit as st` imports Streamlit and gives it the short
    alias `st`.
-   `st.set_page_config()` configures the browser tab title, icon and
    page layout.
-   `st.title()` displays the main heading.
-   `st.write()` displays explanatory text.
-   `st.success()` displays a success-style message.

## 2.7 Run the application

From the project directory, run:

``` powershell
py -3.13 -m streamlit run app.py
```

Streamlit starts a local development server and normally opens the
application in your browser. If it does not open automatically, use the
local URL printed in the terminal, usually:

``` text
http://localhost:8501
```

You should see:

-   The title **AI Image Captioning Assistant**
-   The description text
-   The message **Environment setup completed!**

To stop the server, return to the terminal and press `Ctrl + C`.

## 2.8 Configure .gitignore

Add the following to `.gitignore`:

``` text
__pycache__/
.env
*.pyc
```

The `.env` file will contain a private access token. It must not be
committed to a public or shared Git repository.

### Step 9 completion criteria

-   [ ] Project directory created and opened in VS Code.
-   [ ] Python 3.13 verified.
-   [ ] Project files created.
-   [ ] Dependencies listed in `requirements.txt`.
-   [ ] Dependencies installed successfully.
-   [ ] Basic Streamlit application created.
-   [ ] Streamlit application launched in the browser.
-   [ ] `.gitignore` excludes `.env`.

------------------------------------------------------------------------

# 3. Step 10 -- Hugging Face Integration

## Objective

Authenticate the Python project with Hugging Face and initialise the
Python inference client. This prepares the application for hosted model
calls in a later step.

**Important:** Successful authentication and client initialisation do
not mean that a particular model has been called. We will test actual
model availability and inference when we integrate Qwen2.5-VL.

## 3.1 Open or create a Hugging Face account

Go to:

-   Create an account: https://huggingface.co/join
-   Access-token settings: https://huggingface.co/settings/tokens

If you already have an account and a suitable token, you can reuse it.
You do not need to create another account or token unnecessarily.

## 3.2 Create or verify an access token

In Hugging Face:

1.  Open **Settings → Access Tokens**.
2.  Select **Create new token** if you need a new token.
3.  Give it a descriptive name, for example
    `session-12-image-captioning`.
4.  Choose a fine-grained token.
5.  Enable the permission **Make calls to Inference Providers**.
6.  Create the token and copy its value.

If reusing an existing fine-grained token, inspect its permissions and
confirm that **Make calls to Inference Providers** is enabled.

A token's displayed name or fine-grained label alone does not prove that
the required permission is enabled.

### Security rules

-   Treat the token like a password.
-   Do not paste the complete token into a chat, screenshot, notebook,
    source file or public repository.
-   Do not commit `.env`.
-   If a token is exposed, revoke it in Hugging Face and create a
    replacement.
-   Do not revoke an existing token if another project may depend on it.

## 3.3 Store the token in .env

Open the `.env` file in the project root and add:

``` text
HF_TOKEN=hf_your_actual_token_here
```

Replace the example value with the actual token copied from Hugging
Face.

Do not add quotation marks unless your configuration specifically
requires them. Do not add spaces around the equals sign.

The `.env` file should be in the same project directory from which you
run the Python script.

## 3.4 Verify .gitignore

Confirm that `.gitignore` contains:

``` text
__pycache__/
.env
*.pyc
```

This helps prevent the token from being committed to Git.

## 3.5 Create the authentication test script

Create a new file named:

``` text
test_hf_connection.py
```

Add this code:

``` python
import os

from dotenv import load_dotenv
from huggingface_hub import HfApi, InferenceClient

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Hugging Face token
HF_TOKEN = os.getenv("HF_TOKEN")

# Stop if the token is missing
if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN not found. Check the .env file."
    )

# Create an authenticated Hugging Face Hub API client
api = HfApi(token=HF_TOKEN)

# Verify the token by retrieving the authenticated user
user_info = api.whoami()

print("Authentication successful!")
print("Username:", user_info["name"])

# Initialise the hosted inference client
client = InferenceClient(token=HF_TOKEN)

print("Inference client initialised successfully!")
```

## 3.6 Understand the code

### Load environment variables

``` python
from dotenv import load_dotenv
load_dotenv()
```

`load_dotenv()` reads the `.env` file and makes its key-value pairs
available as environment variables to the running Python process.

### Retrieve the token

``` python
HF_TOKEN = os.getenv("HF_TOKEN")
```

`os.getenv()` reads the environment variable named `HF_TOKEN`.

If the variable is absent, it returns `None`.

### Check the token

``` python
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found. Check the .env file.")
```

This prevents the script from continuing when the token has not been
loaded.

### Create the Hub API client

``` python
api = HfApi(token=HF_TOKEN)
```

This creates an authenticated client for Hugging Face Hub API
operations.

### Verify authentication

``` python
user_info = api.whoami()
```

This makes an authenticated request and retrieves information about the
current Hugging Face user.

If the token is invalid or rejected, the request will raise an error.

### Initialise the inference client

``` python
client = InferenceClient(token=HF_TOKEN)
```

This creates a client object that can be used for supported hosted
inference tasks.

It does not yet send an image or make a model inference request.

## 3.7 Run the authentication test

In the VS Code terminal:

``` powershell
py -3.13 test_hf_connection.py
```

A successful result should look similar to:

``` text
Authentication successful!
Username: your_username
Inference client initialised successfully!
```

The username will be the authenticated Hugging Face account's actual
username.

## 3.8 Common errors and troubleshooting

  ------------------------------------------------------------------------------------
  Error or symptom                    What to check
  ----------------------------------- ------------------------------------------------
  `HF_TOKEN not found`                Confirm `.env` is in the project root, the
                                      variable is named `HF_TOKEN`, and the script is
                                      run from the project directory.

  `401 Unauthorized`                  Check whether the token value is correct, active
                                      and copied completely.

  `403 Forbidden`                     Inspect token permissions and any relevant
                                      model/provider access restrictions.

  `ModuleNotFoundError`               Install the missing package using
                                      `py -3.13 -m pip install -r requirements.txt`.

  Connection or timeout error         Check internet connectivity and retry.

  Wrong username                      Confirm that the token belongs to the intended
                                      Hugging Face account.
  ------------------------------------------------------------------------------------

### Important distinction: authentication versus inference

There are two separate checks:

1.  **Authentication:** Hugging Face recognises the token and identifies
    the account.
2.  **Inference:** A particular model can actually be called through an
    available Inference Provider using the token and the selected
    model/provider configuration.

Step 10 verifies the first and prepares the client for the second. We
will verify actual inference access when we call the model in a later
step.

### Step 10 completion criteria

-   [ ] Hugging Face account available.
-   [ ] Fine-grained token created or existing token inspected.
-   [ ] `Make calls to Inference Providers` permission enabled.
-   [ ] Token stored in `.env`.
-   [ ] `.env` excluded in `.gitignore`.
-   [ ] `test_hf_connection.py` created.
-   [ ] `whoami()` successfully authenticates.
-   [ ] `InferenceClient` initialised.

------------------------------------------------------------------------

# 4. Step 11 -- Image Loading and Inspection

## Objective

Accept an image through Streamlit, load it using Pillow, and inspect its
basic properties.

Students will learn to examine:

-   Image dimensions.
-   Image format.
-   Image colour mode.
-   RGB channels.
-   Individual pixel values.

We are not yet converting the image into a NumPy array or model-specific
tensor. That is outside the scope of this step.

## 4.1 Understand Pillow

Pillow is a Python imaging library. It provides tools to open, inspect,
convert and manipulate images.

The main import used in this exercise is:

``` python
from PIL import Image
```

Useful properties and methods:

  Property or method         Purpose
  -------------------------- -----------------------------------------
  `Image.open()`             Opens an image
  `image.size`               Returns `(width, height)`
  `image.width`              Returns image width
  `image.height`             Returns image height
  `image.format`             Returns format such as JPEG or PNG
  `image.mode`               Returns colour mode such as RGB or RGBA
  `image.convert("RGB")`     Converts the image to RGB mode
  `image.split()`            Separates the image into bands/channels
  `image.getpixel((x, y))`   Returns pixel value at a coordinate

## 4.2 Update app.py

Replace the basic Step 9 contents of `app.py` with the following
complete implementation:

``` python
import streamlit as st
from PIL import Image

# Configure the Streamlit page
st.set_page_config(
    page_title="AI Image Captioning Assistant",
    page_icon="🖼️",
    layout="wide"
)

# Display application heading and instructions
st.title("AI Image Captioning Assistant")

st.write(
    "Upload an image to inspect its properties "
    "and understand its numerical representation."
)

# Create an image uploader
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"]
)

# Continue only if the user uploaded a file
if uploaded_file is not None:

    # Open the uploaded file using Pillow
    image = Image.open(uploaded_file)

    st.subheader("Uploaded Image")

    # Display the original uploaded image
    st.image(
        image,
        caption="Your uploaded image",
        width=500
    )

    # Display image properties
    st.subheader("Image Properties")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Width", f"{image.width} px")

    with col2:
        st.metric("Height", f"{image.height} px")

    with col3:
        st.metric("Format", image.format or "Unknown")

    st.write("Original Colour Mode:", image.mode)

    # Convert to RGB so that we have three colour channels
    rgb_image = image.convert("RGB")

    # Separate the RGB channels
    red, green, blue = rgb_image.split()

    st.subheader("RGB Channel Inspection")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(red, caption="Red Channel")

    with col2:
        st.image(green, caption="Green Channel")

    with col3:
        st.image(blue, caption="Blue Channel")

    # Select the centre pixel for inspection
    x = rgb_image.width // 2
    y = rgb_image.height // 2

    # Retrieve its RGB values
    pixel_value = rgb_image.getpixel((x, y))

    st.subheader("Pixel Inspection")

    st.write(f"Pixel Coordinates: ({x}, {y})")
    st.write(f"RGB Values: {pixel_value}")

else:
    st.info("Please upload an image to begin.")
```

## 4.3 Understand the implementation in detail

### A. Import the libraries

``` python
import streamlit as st
from PIL import Image
```

-   Streamlit provides the user interface.
-   Pillow provides image loading and inspection functionality.

### B. Create the upload control

``` python
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"]
)
```

`st.file_uploader()` displays a file upload control in the browser.

The `type` argument restricts the file types accepted by this interface.

The returned object is a file-like uploaded object. It can be passed to
Pillow.

### C. Check whether a file was uploaded

``` python
if uploaded_file is not None:
```

If the user has not uploaded an image, the value is `None`.

The `if` statement ensures we attempt to load the image only after a
file has been supplied.

### D. Open the image

``` python
image = Image.open(uploaded_file)
```

Pillow reads the uploaded image and returns a Pillow Image object.

This object gives us access to image properties and image-processing
operations.

### E. Inspect image dimensions

``` python
image.width
image.height
image.size
```

For example, a 1920 × 1080 image has:

``` python
image.size
```

Expected result:

``` text
(1920, 1080)
```

Notice the order:

-   Pillow's `image.size` returns `(width, height)`.
-   Our conceptual image tensor convention in the earlier slide was
    `height × width × channels` (H × W × C).

These are two different ways of describing dimensions. Do not confuse
their ordering.

### F. Inspect the image format

``` python
image.format
```

Possible values include:

-   `JPEG`
-   `PNG`
-   `WEBP`

The format tells us how the image file is encoded. It is different from
the image's colour mode.

### G. Inspect the colour mode

``` python
image.mode
```

Common Pillow image modes:

  Mode     Explanation
  -------- -------------------------------------------
  `RGB`    Red, Green and Blue colour channels
  `RGBA`   Red, Green, Blue and Alpha (transparency)
  `L`      Grayscale, with one intensity channel
  `P`      Palette-based image

An uploaded image is not guaranteed to be RGB. For example, a PNG may
contain an alpha channel.

### H. Convert the image into RGB

``` python
rgb_image = image.convert("RGB")
```

This creates an RGB representation of the image.

It ensures that subsequent pixel inspection returns three colour values.

For an RGBA image, the alpha channel is not retained in this RGB
conversion.

This operation does not resize the image and does not normalize its
pixel values.

### I. Split the RGB channels

``` python
red, green, blue = rgb_image.split()
```

This produces three separate single-channel images.

Each channel contains the intensity of that colour at each pixel
location.

For a typical 8-bit channel:

-   0 represents no intensity for that channel.
-   255 represents maximum intensity for that channel.

The channel images are displayed in grayscale. Their brightness
represents the intensity of the corresponding colour channel.

### J. Inspect one pixel

``` python
x = rgb_image.width // 2
y = rgb_image.height // 2

pixel_value = rgb_image.getpixel((x, y))
```

This selects the centre pixel of the image.

For an RGB image, the returned value will look like:

``` text
(125, 180, 95)
```

This means:

-   Red intensity = 125
-   Green intensity = 180
-   Blue intensity = 95

The coordinate order for `getpixel()` is `(x, y)`, meaning
`(horizontal position, vertical position)`.

## 4.4 Run the application

Run:

``` powershell
py -3.13 -m streamlit run app.py
```

Upload a JPEG, PNG or WEBP image.

The interface should display:

1.  The uploaded image.
2.  Image width and height.
3.  Image format.
4.  Original colour mode.
5.  Red, Green and Blue channel images.
6.  The coordinates and RGB values of the centre pixel.

Try uploading images with different formats and colour modes where
possible.

## 4.5 What students should observe

### Observation 1: Image dimensions

Two images may have different widths and heights. These dimensions
describe their pixel grid.

### Observation 2: Image format and colour mode are different

JPEG and PNG describe file formats. RGB and RGBA describe how colour
information is represented.

### Observation 3: RGB channels are separate numerical layers

The three channel images together represent the colour information in an
RGB image.

### Observation 4: Pixel values are numerical

A pixel can be inspected as a tuple of channel intensities. This helps
connect the visual image to the numerical representation discussed in
the conceptual slides.

## 4.6 Important technical boundaries

-   This exercise uses Pillow's image object. It does not create a NumPy
    array.
-   It does not create a PyTorch tensor.
-   It does not resize or normalize the image.
-   It does not generate a caption.
-   It does not call the Qwen model.
-   The `RGB` conversion is a colour-mode conversion, not a
    model-specific preprocessing pipeline.

The later Qwen2.5-VL integration should use the model's supported
image-input and processor workflow rather than duplicating
model-specific preprocessing manually.

### Step 11 completion criteria

-   [ ] Streamlit uploader accepts supported image formats.
-   [ ] Pillow opens the uploaded image.
-   [ ] Original image is displayed.
-   [ ] Width and height are inspected.
-   [ ] File format is inspected.
-   [ ] Original colour mode is inspected.
-   [ ] Image is converted to RGB.
-   [ ] RGB channels are separated and displayed.
-   [ ] Centre pixel coordinates and RGB values are displayed.

------------------------------------------------------------------------

# 5. Final project structure after Step 11

By the end of Step 11, the project should look like this:

``` text
session_12_image_captioning/
│
├── app.py
├── image_captioner.py
├── test_hf_connection.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The `.env` file contains the private Hugging Face token. Keep it local
and do not share it.

The `image_captioner.py` file is reserved for the model integration
logic that we will implement later.

------------------------------------------------------------------------

# 6. Troubleshooting reference

  --------------------------------------------------------------------------------------------
  Problem                             Suggested action
  ----------------------------------- --------------------------------------------------------
  `py -3.13` is not recognised        Verify Python 3.13 installation and Windows Python
                                      Launcher configuration.

  `No module named streamlit`         Run `py -3.13 -m pip install -r requirements.txt`.

  `No module named PIL`               Install Pillow using `py -3.13 -m pip install pillow`.

  `No module named dotenv`            Install python-dotenv using
                                      `py -3.13 -m pip install python-dotenv`.

  Streamlit command is not found      Use `py -3.13 -m streamlit run app.py`.

  Hugging Face token not found        Check `.env` location, spelling and the current working
                                      directory.

  Hugging Face authentication fails   Verify the token is active and has the required
                                      permission.

  Image cannot be opened              Confirm the file is a supported, valid image. Try
                                      another JPEG or PNG.

  Browser does not open               Use the local URL printed in the Streamlit terminal.

  Port 8501 is occupied               Stop the other Streamlit process or use
                                      `py -3.13 -m streamlit run app.py --server.port 8502`.
  --------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 7. Learning outcomes -- Steps 9 to 11

After completing these three steps, students should be able to:

1.  Create and configure a Python application project.
2.  Install and manage Python dependencies using pip.
3.  Build and launch a basic Streamlit application.
4.  Store and load secrets using environment variables.
5.  Authenticate a Python application with Hugging Face.
6.  Initialise the Hugging Face inference client.
7.  Accept uploaded images through Streamlit.
8.  Load images using Pillow.
9.  Inspect image dimensions, formats and colour modes.
10. Convert images into RGB and separate colour channels.
11. Retrieve individual pixel values.

## What we have not built yet

The application currently inspects uploaded images. It does not yet
understand or describe their visual content.

The next major milestone is to connect the uploaded image to
**Qwen2.5-VL-7B-Instruct** through a supported Hugging Face Inference
Provider and generate our first image caption.

------------------------------------------------------------------------

**End of Steps 9--11 documentation.**
