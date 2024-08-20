# Screenshot Description Generator

This Python script utilizes Google Generative AI (GenAI) to automatically generate long and short descriptions for screenshot images. It leverages a Large Language Model (LLM) to analyze the content of each screenshot and provide concise summaries.

**Features:**

* Generates long-form and short-form descriptions for screenshots.
* Uses GenAI's LLM capabilities for image analysis.
* Saves descriptions to a CSV file for further use.
* Optionally renames screenshots based on the short descriptions.
* Embeds long descriptions as metadata in PNG images (experimental).

**Requirements:**

* Python 3.x
* Pillow library (`pip install Pillow`)
* Pandas library (`pip install pandas`)
* Google GenerativeAI library (follow installation instructions from Google AI)
* A Google Cloud project with GenAI API enabled

**Instructions:**

1. Install required libraries (mentioned above).
2. Set up your Google Cloud project and obtain an API key for GenAI.
3. Save the API key in a file named `.env` in the project directory (refer to dotenv documentation for details).
4. Configure the script by editing the following sections in the code (marked as `START: Change only below fields` and `END: Change only below fields`):
    * `output_folder`: Path to the folder containing screenshots.
    * `csv_fname`: Name of the CSV file to store descriptions.
    * `col1`: Column name for image file paths in the CSV.
    * `col2`: Column name for long descriptions in the CSV.
    * `col3`: Column name for short descriptions in the CSV.
    * `resized_img_width`: Desired width for resizing images before processing (affects LLM performance).
    * `img_desc_prompt`: The prompt string used for the LLM API call to generate descriptions.
5. Run the script: `python script_name.py`

**Notes:**

* This script uses GenAI, which may incur costs depending on your usage. Refer to Google Cloud pricing for details.
* The script currently supports PNG images.
* Embedding descriptions in image metadata (EXIF) is an experimental feature and might not work on all systems.

**Additional Information:**

* The script utilizes several helper functions:
    * `load_or_create_dataframe_from_schema`: Loads or creates a DataFrame for storing image descriptions.
    * `write_text_to_png`: Embeds text data as metadata in a PNG image (experimental).
    * `get_image_desc`: Processes an image file, generates descriptions, and updates the DataFrame.
    * `make_api_call`: Calls the GenAI API to generate text based on a prompt and image.
    * `handle_rate_limit_error`: Implements retry logic for API rate limits.

This script provides a basic framework for automatically generating image descriptions. You can modify it to suit your specific needs and explore further functionalities offered by GenAI and the libraries used.