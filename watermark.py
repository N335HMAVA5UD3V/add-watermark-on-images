import streamlit as st
import cv2
import os


def add_watermark(image_path, watermark_path):
    # Read the original image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Read the watermark image
    watermark = cv2.imread(watermark_path)

    # Resize the watermark to fit the original image
    watermark_resized = cv2.resize(watermark, (img.shape[1], img.shape[0]))

    # Blend the images
    watermarked_image = cv2.addWeighted(img, 1, watermark_resized, 0.5, 0)

    return watermarked_image


def add_text_watermark(image_path, watermark_text):
    # Read the original image
    img = cv2.imread(image_path)

    # Convert image to RGB (OpenCV uses BGR by default)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Add text watermark
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottom_left_corner_of_text = (10, img.shape[0] - 10)
    font_scale = 1
    font_color = (255, 255, 255)
    line_type = 2
    cv2.putText(img, watermark_text, bottom_left_corner_of_text, font, font_scale, font_color, line_type)

    return img


def main():
    opt = st.radio('Select mode of Watermark', ("Image Watermark", "Text Watermark"))
    if opt == "Image Watermark":
        image_file = st.file_uploader("Choose an image..", type=["jpg", "png", "jpeg"])
        if image_file is not None:
            # Display uploaded image
            st.image(image_file, caption="Uploaded Image", use_column_width=True)

            # Upload watermark image
            watermark_file = st.file_uploader("Upload watermark image", type=['jpg', 'jpeg', 'png'])
            if watermark_file is not None:
                # Display watermark image
                st.image(watermark_file, caption="Watermark Image", use_column_width=True)

                if st.button("Add Watermark"):
                    # Save uploaded files to temporary locations
                    temp_image_path = "temp_image.jpg"
                    temp_watermark_path = "temp_watermark.png"
                    with open(temp_image_path, "wb") as f:
                        f.write(image_file.read())
                    with open(temp_watermark_path, "wb") as f:
                        f.write(watermark_file.read())

                    # Add watermark
                    watermarked_image = add_watermark(temp_image_path, temp_watermark_path)

                    # Display watermarked image
                    st.image(watermarked_image, caption="Watermarked Image", use_column_width=True)

                    # Remove temporary files
                    os.remove(temp_image_path)
                    os.remove(temp_watermark_path)
    elif opt == "Text Watermark":
        image_file = st.file_uploader("Choose an image..", type=["jpg", "png", "jpeg"])
        if image_file is not None:
            # Display uploaded image
            st.image(image_file, caption="Uploaded Image", use_column_width=True)

            # Get watermark text from user input
            watermark_text = st.text_input("Enter watermark text:")

            if st.button("Add Watermark"):
                # Save uploaded file to a temporary location
                temp_image_path = "temp_image.jpg"
                with open(temp_image_path, "wb") as f:
                    f.write(image_file.read())

                # Add watermark
                watermarked_image = add_text_watermark(temp_image_path, watermark_text)

                # Display watermarked image
                st.image(watermarked_image, caption="Watermarked Image", use_column_width=True)

                # Remove temporary file
                os.remove(temp_image_path)


if __name__ == "__main__":
    main()
