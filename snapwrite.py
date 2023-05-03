# snapwrite.py
# proof of concept for Louis Anslow's PoetryCamera project
# © Archie McKenzie, 2023

# ----- IMPORTS -----  #
import openai
import replicate
import os
import threading
import time

# ----- EDITABLE VARIABLES -----  #

image_path = "./images/princeton_snowy.jpeg" # path to image

openai.api_key = "" # OpenAI API Key
REPLICATE_API_TOKEN = "" # Replicate API Key

# ----- TIME PRINTING -----  #

def print_time():
    global t
    while True:
        time.sleep(1)
        t += 1
        print(t)

t = 0
stop_event = threading.Event()
thread = threading.Thread(target=print_time)
thread.daemon = True
thread.start()

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
        {"role": "user", "content": f"Write a brief, clever poem about the following image: {image_description}"},
    ]
)
poem = completion['choices'][0]['message']['content']

stop_event.set()

# ----- PRINT RESULT -----  #

print("# ------ POETRY CAMERA ------ #")
print("\n" + poem + "\n")
print("# ------ END ------ #")

# ----- WRITE .TXT -----  #

file = open("poem.txt", "w")

file.write("# ------ POETRY CAMERA ------ #")
file.write("\n\n")
file.write(poem)
file.write("\n\n")
file.write(f"Inspired by an image of {image_description}")
file.write("\n\n")
file.write("# ------ END ------ #")

file.close()