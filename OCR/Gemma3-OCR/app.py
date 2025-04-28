import streamlit as st
from PIL import Image
import io
import base64
import ollama
from pdf2image import convert_from_bytes

# Page configuration
st.set_page_config(
    page_title="Gemma3 - OCR",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and icon image
st.markdown("""
    # <img src="data:image/png;base64,{}" width="50" style="vertical-align: -12px;"> Gemma-3 OCR
""".format(base64.b64encode(open("/image/gemma3.png", "rb").read()).decode()), unsafe_allow_html=True)

# Clear button
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear 🚮️"):
        st.session_state.pop('ocr_result', None)
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract structured text from images or PDFs using Gemma-3 Vision!</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload File")
    uploaded_file = st.file_uploader("Choose an image or PDF...", type=['png', 'jpg', 'jpeg', 'pdf'])

    images_to_process = []

    if uploaded_file is not None:
        file_ext = uploaded_file.name.split('.')[-1].lower()  

        # Handle image files
        if file_ext in ['jpg', 'jpeg', 'png']:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            img_bytes = uploaded_file.getvalue()
            images_to_process.append(img_bytes)

        # Handle PDF files
        elif file_ext == 'pdf':
            st.info("Converting PDF to images...")
            try:
                pdf_images = convert_from_bytes(uploaded_file.read())
                for img in pdf_images:
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='PNG')
                    images_to_process.append(img_byte_arr.getvalue())
                st.image(pdf_images, caption=[f"Page {i+1}" for i in range(len(pdf_images))], use_column_width=True)
            except Exception as e:
                st.error(f"PDF processing failed: {e}")

        else:
            st.error("Unsupported file format.")

        # Button to extract text
        if images_to_process and st.button("Extract Text 📄", type="primary"):
            all_results = []
            with st.spinner("Processing..."):
                for idx, img_bytes in enumerate(images_to_process):
                    try:
                        response = ollama.chat(
                            model='gemma3:12b-it-qat',
                            messages=[{
                                'role': 'user',
                                'content': """Analyze the text in the provided image. Extract all readable content
                                              and present it in a structured Markdown format that is clear, concise, 
                                              and well-organized. Ensure proper formatting (e.g., headings, lists, tables or
                                              code blocks) as necessary to represent the content effectively.""",
                                'images': [img_bytes]
                            }]
                        )
                        result = response.message.content
                        all_results.append(f"### Page {idx+1}\n{result}")
                    except Exception as e:
                        all_results.append(f"### Page {idx+1}\nError: {str(e)}")

            st.session_state['ocr_result'] = "\n\n".join(all_results)

# Show OCR result
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image or PDF and click 'Extract Text' to see results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Gemma3 Vision Model")
