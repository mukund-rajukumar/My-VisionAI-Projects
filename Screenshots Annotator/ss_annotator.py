from PIL import Image, PngImagePlugin

import glob #Used to retrieve file paths matching a specified pattern 
import pandas as pd
import os
import google.generativeai as genai
import time
from typing import Dict

def load_or_create_dataframe_from_schema(output_folder, filename, schema):
    """Loads an existing DataFrame from a CSV file or creates a new one based on the provided schema.

    Args:
        output_folder (str): The path to the output folder.
        filename (str): The name of the CSV file.
        schema (Dict[str, type]): A dictionary defining column names and their data types.

    Returns:
        pandas.DataFrame: The loaded or created DataFrame.
    """

    try:
        os.makedirs(output_folder, exist_ok=True)
        full_fname = os.path.join(output_folder, filename)

        if os.path.isfile(full_fname):
            df = pd.read_csv(full_fname)
        else:
            df = pd.DataFrame(columns=schema.keys())
            df = df.astype(schema)
        return df
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error loading or creating DataFrame: {e}")

def write_text_to_png(image_path, output_path, text_data):
    """Writes text data to a PNG image's metadata.

    Args:
        image_path (str): Path to the input PNG image.
        output_path (str): Path to the output PNG image with metadata.
        text_data (Dict[str, str]): A dictionary of key-value pairs to be stored as metadata.
    """
    img = Image.open(image_path)
    metadata = PngImagePlugin.PngInfo()

    for key, value in text_data.items():
        metadata.add_text(key, str(value))

    img.save(output_path, pnginfo=metadata)

def get_image_desc(image_file, df, resized_width, img_desc_prompt):
    """Processes an image file, generates descriptions, and updates a DataFrame.

    Args:
        image_file (str): Path to the image file to be processed.
        df (pd.DataFrame): The pandas DataFrame to store image descriptions.
            Must have columns for image filename, short description, and long description.
        resized_width (int): The desired width for image resizing before description generation.
        img_desc_prompt (str): The prompt string to be used for the LLM API call to generate image descriptions.

    Prints processing information and updates the DataFrame with image details and generated descriptions.

    Raises:
        ValueError: If the provided DataFrame (df) doesn't have the expected columns.
    """
    print(f"\nProcessing {image_file}\n")
    with Image.open(image_file) as img:
        width, height = img.size
        aspect_ratio = width/height
        resized_img = img.resize((resized_width,int(resized_width/aspect_ratio)),Image.Resampling.LANCZOS)
        llm_response = make_api_call(img_desc_prompt, resized_img)
        parts = llm_response.text.split('|')
        # Extract the first and second parts
        print(parts[0].strip()+" | "+parts[1].strip())

        # Add a new row to the DataFrame
        df.loc[len(df)] = [image_file, parts[0].strip(), parts[1].strip()]

def make_api_call(prompt, image):
    """Calls a Large Language Model (LLM) API to generate text based on a prompt and image.

    Args:
        prompt (str): The text prompt for the LLM.
        image (Image.Image): The image to be analyzed by the LLM.

    Returns:
        genai.TextGenerationResponse: The response object from the LLM API.
    """
    try:
        response = model.generate_content([prompt, image])
    except Exception as e: 
        if e.code == 429:
            print ("Rate Limit Error")
            # Implement retry logic or handle the error appropriately
            return handle_rate_limit_error(prompt, image)

    return response

def handle_rate_limit_error(prompt, image):
    """Handles rate limit errors from the LLM API by implementing a retry logic.

    Args:
        prompt (str): The text prompt for the LLM.
        image (Image.Image): The image to be analyzed by the LLM.

    Returns:
        genai.TextGenerationResponse: The response object from the LLM API after retrying.
    """
    time.sleep(60)
    return model.generate_content([prompt, image])            

if __name__ == '__main__':    
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    """ START: Change only below fields """
    output_folder = '/Users/mukund/Desktop/Screenshots'
    csv_fname = 'image_descriptions.csv'
    col1 = 'Image File'
    col2 = 'Long Desc'
    col3 = 'Short Desc'
    resized_img_width = 100
    img_desc_prompt = "Write 1-line summary and a 3-word phrase summary for the image content. Remove all puncutation marks from the 3-word summary. Append the 2 responses into single line with separator |"

    """ END: Change only below fields """

    schema = {
        col1: str,
        col2: str,
        col3: str
    }

    try:
        # Create a table to store long and short description of each of the screenshots
        df = load_or_create_dataframe_from_schema(output_folder, csv_fname, schema)
        print(df.head())
    except Exception as e:
        print(f"CREATE_DATAFRAME: An error occurred: {e}")

    # Get the list of screenshot files in the folder you want to process
    image_files = glob.glob(f"{output_folder}/Screenshot*.png") 
    image_files.sort()
    print(image_files)

    try:
        # Send each image file to LLM to get a long form and short form description of the image
        for image_file in image_files:
            if image_file not in df[col1].values:
                get_image_desc(image_file, df, resized_img_width, img_desc_prompt)
    except Exception as e:
        print(f"PROCESS_IMAGE: An error occurred: {e}")

    try:
        # Save the updated table to a CSV file
        os.makedirs(output_folder, exist_ok=True)
        full_fname = os.path.join(output_folder, csv_fname)
        df.to_csv(full_fname, index=False)

        # Add the long form description of screenshot to EXIF header of image into the Comments field
        for index, row in df.iterrows():
            old_file_path = row[col1]
            new_file_path = row[col3].strip() + '.png'
            new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_path)
            new_file_path = new_file_path.replace(",", "")
           
            if os.path.exists(old_file_path):
                # Check if new file already exists
                counter = 1
                while os.path.exists(new_file_path):
                    new_file_name = f"{row[col3].strip()}_{counter}.png"
                    new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
                    new_file_path = new_file_path.replace(",", "")
                    counter += 1
                os.rename(old_file_path, new_file_path)
            else:
                print(f"File {old_file_path} does not exist.")

            if os.path.exists(new_file_path):
                print(new_file_path)
                write_text_to_png(new_file_path, new_file_path,{"Comments": row[col2]})
            else:
                print(f"Write_text_to_png: File {new_file_path} does not exist.")

    except Exception as e:
        print(f"An error occurred: {e}")