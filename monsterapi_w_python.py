# Required library imports
from monsterapi import client
from pydantic import BaseModel, ValidationError, conint
from typing import Literal
import os
import time
import random
import subprocess
import requests as re

# Define data model with validation rules using Pydantic
class SDInputModel(BaseModel):
    negprompt: str
    samples: int
    steps: conint(ge=30, le=60)  #type:ignore    Steps must be between 30 and 60
    aspect_ratio: Literal["square", "portrait", "landscape"]
    guidance_scale: int
    seed: conint(ge=1000, le=10000)  #type:ignore    Seed must be between 1000 and 10000

# Initialize MonsterAPI client
api_key = "Your API key here"
monster_client = client(api_key)
model = 'txt2img'

# Get current script directory and prepare default file path
script_dir = os.getcwd()
file_name = "Generated_image.jpg"
file_path = os.path.join(script_dir, file_name)

# Function to accept advanced image generation settings from user
def adv_setting():
    global img_open  # Used later to determine whether to open generated images
    while True:
        print("\n\nEnter values for the following fields ↓\n")
        try:
            # Collect user inputs
            input_data = {
                "prompt": prompt,
                "negprompt": str(input("Enter negative prompt: ")).lower(),
                "samples": int(input("Enter number of images to be generated: ")),
                "steps": int(input("Enter number of denoising steps.(Accepted values[30-60]): ")),
                "aspect_ratio": str(input("Enter aspect_ratio(square, portrait, landscape): ")).lower(),
                "guidance_scale": int(input("Enter guidance_scale(Accepted values([5-50])): ")),
                "seed": int(input("Enter seed for randomization(1000-10,000): ")),
            }

            # Validate user input against SDInputModel
            validated = SDInputModel(**input_data)

            # Ask user whether to open multiple images after generation
            if input_data['samples'] > 1:
                img_open = str(input(f"Do you want to open all ({input_data['samples']}) images when generated? (y/n): "))

            break  # Exit loop on successful input and validation

        except ValidationError as ve:
            print(f"\n\n{ve}", "\n\nVALIDATION ERROR!")
        except ValueError:
            print("\nVALUE ERROR!\nPlease enter valid numbers.")

    print("\nGenerating image...")
    return input_data

# Welcome message
print("\nHello! Welcome to MonsterAPI.\n")

# Prompt user for text-to-image generation prompt
prompt = str(input("Enter a brief prompt to generate an image: "))

# Offer default or advanced settings
while True:
    print("\n\nEnter 'default' to generate with default settings\n\t\t or \nEnter 'advance' for custom settings\n")
    setting_input = str(input()).lower()

    if setting_input == "default":
        input_data = {
            'prompt': prompt,
            'negprompt': 'bad anatomy',
            'samples': 1,
            'steps': 50,
            'aspect_ratio': 'square',
            'guidance_scale': 7.5,
            'seed': random.randint(1000, 10000),
        }
        print("\nSeed generated:", input_data.get('seed', 'NotFound'))
        print("\nGenerating image...")
        break

    elif setting_input == "advance":
        input_data = adv_setting()
        break

    else:
        print("Invalid input!")

# Generate images using MonsterAPI
try:
    result = monster_client.generate(model, input_data)
    print("\nLink(s) for the image(s):", result['output'])

except TimeoutError as e:
    print(f"\nERROR: Image generation timed out.")
    print("The API queue may be overloaded. Please try again after a couple of hours.")
    retry = input("Do you still want to retry? (y/n): ").lower()
    if retry == 'y':
        print("Generating image...")
        result = monster_client.generate(model, input_data)
    else:
        exit(1)

img_urls = result['output']  # List of generated image URLs

# Download and optionally open each generated image
for idx, img_url in enumerate(img_urls, start=1):
    file_name = f"Generated_image_{idx}.jpg"
    file_path = os.path.join(script_dir, file_name)

    response = re.get(img_url)

    if response.status_code == 200:
        # Save image to disk
        with open(file_path, 'wb') as file:
            file.write(response.content)
            file.flush()
            os.fsync(file.fileno())  # Ensure data is fully written to disk
            print(f"Image {idx} saved to: {file_path}")

        # Open image if user requested
        if input_data['samples'] == 1 or (img_open == "y" or img_open == "yes"):
            time.sleep(0.5)
            subprocess.Popen(["python", "open_image.py", file_path])

    else:
        print(f"Failed to download image {idx}")