from dotenv import load_dotenv
from PIL import Image, PngImagePlugin
#from io import BytesIO

import glob #Used to retrieve file paths matching a specified pattern 
import pandas as pd
import os
import google.generativeai as genai
import time

# Load the DataFrame from a CSV file, or create a new one if the file doesn't exist

def cleanup_csv(filename):
    try:
        os.path.isfile(filename)
        df = pd.read_csv(filename)
        df['Long Desc'] = None
        df['Short Desc'] = None
        #print(df['description'].str.split('\n', expand=True))
        print(df.head())

        split_df = df['description'].str.split('\n', expand=True)
        split_df.columns = ['Long Desc', 'Short Desc', 'Extra1', 'Extra2']
        split_df['Short Desc'] = split_df['Short Desc'] + split_df['Extra1'] + split_df['Extra2']

        print(split_df)        
        print(df.head())
        df.to_csv('image_descriptions_v2.csv', index=False)
    except Exception as e:
        print(f"An error occurred: {e}")

def rename_files(csv_fname):
    try:
        df = pd.read_csv(csv_fname)
        print(df.head())
        for index, row in df.iterrows():
            old_file_path = row['image_file']
            new_file_name = row['short description'].strip() + '.png'  # Adjust extension as needed
            new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)

            # Check if new file already exists
            counter = 1
            while os.path.exists(new_file_path):
                new_file_name = f"{row['short description'].strip()}_{counter}.png"
                new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
                counter += 1
           
            if os.path.exists(old_file_path):
                os.rename(old_file_path, new_file_path)
            else:
                print(f"File {old_file_path} does not exist.")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except OSError as e:
        print(f"Error renaming file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def write_text_to_png(image_path, output_path, text_data):
  """Writes text data to a PNG image's metadata.

  Args:
    image_path: Path to the input PNG image.
    output_path: Path to the output PNG image with metadata.
    text_data: A dictionary of key-value pairs to be stored as metadata.
  """
  img = Image.open(image_path)
  metadata = PngImagePlugin.PngInfo()

  for key, value in text_data.items():
    metadata.add_text(key, str(value))

  img.save(output_path, pnginfo=metadata)

def load_or_create_dataframe(filename):
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=['image_file', 'description'])
    return df

def get_png_files(folder_path):
    return glob.glob(f"{folder_path}/*.png")

# processing the images 
def process_image(image_file):
    # load_dotenv()
    # genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    # model = genai.GenerativeModel('gemini-1.5-flash')

    print(f"\nProcessing {image_file}\n")
    with Image.open(image_file) as img:
        width, height = img.size
        aspect_ratio = width/height
        resized_img = img.resize((100,int(100/aspect_ratio)),Image.Resampling.LANCZOS)
        # with BytesIO() as buffer:
        #    img.save(buffer, format='PNG')
        #    image_bytes = buffer.getvalue()
        prompt = "Write 1-line summary and a 2-word summary for the image content. Append the 2 responses into single line with separator |"
        response = make_api_call(prompt, resized_img)
        print(response.text)
        #print(image_file+":"+response.text)

        # Add a new row to the DataFrame
        df.loc[len(df)] = [image_file, response.text]

def make_api_call(prompt, image):
    try:
        response = model.generate_content([prompt, image])
    except Exception as e: 
        if e.code == 429:
            print ("Rate Limit Error")
            # Implement retry logic or handle the error appropriately
            return handle_rate_limit_error(prompt, image)

    return response

def handle_rate_limit_error(prompt, image):
    # Implement logic to handle rate limit errors
    # For example, exponential backoff or waiting for a specific time
    time.sleep(60)
    return model.generate_content([prompt, image])            

    print(response.text)
    return response

if __name__ == '__main__':    

    load_dotenv()
    # api_key = os.environ.get('GOOGLE_API_KEY')
    # print(api_key)
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    genai.configure(api_key='AIzaSyDly7Ynux-Mq60j5_JOQaI1pJFIzw50qx0')
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        # cleanup_csv('image_descriptions.csv')

        # rename_files('image_descriptions.csv') 

        df = pd.read_csv('image_descriptions.csv')
        print(df.head())
        for index, row in df.iterrows():
            old_file_name = row['image_file']
            new_file_name = row['short description'].strip() + '.png'
            new_file_name = os.path.join(os.path.dirname(old_file_name), new_file_name)

            if os.path.exists(new_file_name):
                print(new_file_name)
                write_text_to_png(new_file_name,new_file_name,{"Comments": row['long description']})
            else:
                print(f"Write_text_to_png: File {new_file_name} does not exist.")

        # # get the list of image files in the folder yopu want to process
        # image_files = get_png_files("/Users/mukund/Desktop/Screenshots") 
        # image_files.sort()

        # for image_file in image_files:
        #     if image_file not in df['image_file'].values:
        #         process_image(image_file)

        # # Save the DataFrame to a CSV file
        # df.to_csv('image_descriptions.csv', index=False)
        
    except Exception as e:
        print(f"An error occurred: {e}")