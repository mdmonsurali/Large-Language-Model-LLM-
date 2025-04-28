# Gemma3 - OCR

This project leverages Gemma3 vision capabilities and Streamlit to create a 100% locally running computer vision app that can perform both OCR and extract structured text from the image.

## Installation and setup

**Setup Ollama**:
   ```bash
   # setup ollama on linux 
   curl -fsSL https://ollama.com/install.sh | sh
   # pull gemma-3 vision model
   ollama run gemma3:12b-it-qat
   ```

**Install Dependencies**:
   Ensure you have Python 3.11 or later installed.
   ```bash
   pip install streamlit ollama pillow
   ```

**Running in Google Colab**:
   ```bash
	!pip install pdf2image
	!apt-get install poppler-utils
	!pip install pyngrok
   ```
   Require ngrok authtoken. Go to the link, create an account, and generate your free authtoken. Link: https://dashboard.ngrok.com/authtokens
   
   Follow the Run_Gemma3_OCR_Colab.ipynb file.
