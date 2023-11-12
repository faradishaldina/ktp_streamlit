import streamlit as st
from PIL import Image
from ktp_ocr import ktp_scan, read_ktp  # Import the ktp_scan function from the ktp_ocr.py file


def main():
    st.title('Simple KTP Scanner App')

    st.write("Upload a KTP image for scanning:")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button('Scan'):
            st.write("Scanning...")
            image_path = "temp_image.jpg"
            image.save(image_path)
            result = read_ktp(image_path)  # Call the ktp_scan function
            st.write("Scanned Text:")
            st.write(result)

if __name__ == '__main__':
    main()
