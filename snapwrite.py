# snapwrite.py
# proof of concept for Louis Anslow's PhotoCamera project
# © Archie McKenzie, 2023

# ----- IMPORTS -----  #
import openai
import replicate
import os

# ----- EDITABLE VARIABLES -----  #

image_path = "./princeton.jpeg" # path to image

openai.api_key = "" # OpenAI API Key
REPLICATE_API_TOKEN = "" # Replicate API Key

# ----- DRIVER INITIALIZATION -----  #

# loads from dotenv if they haven't been set in-script
if (openai.api_key == ""):
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

if (REPLICATE_API_TOKEN == ""):
    from dotenv import load_dotenv
    load_dotenv()
    REPLICATE_API_TOKEN =  os.getenv("REPLICATE_API_TOKEN")

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# ----- PROCESS PHOTO -----  #

image_description = replicate.run(
    "j-min/clip-caption-reward:de37751f75135f7ebbe62548e27d6740d5155dfefdf6447db35c9865253d7e06",
    input={"image": open(image_path, "rb")}
)

# ----- CALL GPT -----  #

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a poet AI who writes poems based on the images you are told about."},
        {"role": "user", "content": f"Write me a poem about the following image: ${image_description}"},
    ]
)
poem = completion['choices'][0]['message']['content']

# ----- PRINT RESULT -----  #

print("# ------ POETRY CAMERA ------ #")
print("\n" + poem + "\n")
print("# ------ #")