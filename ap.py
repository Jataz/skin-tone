import streamlit as st
from streamlit_option_menu import option_menu
import os
import cv2
import numpy as np
import urllib
from models.skin_analysis import analyze_skin
from models.recommender import recommend_products, init_db_connection, close_db_connection,fetch_gallery_products

# Configure Streamlit page
st.set_page_config(page_title="Facial Skin Analysis & Cosmetics Recommendation", layout="wide")
init_db_connection()

# Configure upload folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Apply custom CSS for styling
st.markdown("""
    <style>
    .css-1aumxhk { background-color: #4CAF50 !important; }
    .css-18e3th9 { padding-top: 0px !important; }
    .css-1v3fvcr { padding-left: 1rem !important; padding-right: 1rem !important; }
    img { max-width: 300px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Function to detect face and extract skin area
def detect_face(image_path):
    """Detects the face and extracts skin area from the image."""
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load OpenCV face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        if len(faces) == 0:
            st.warning("No face detected. Please upload a clear image of your face.")
            return None

        # Extract the largest detected face
        x, y, w, h = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]
        face_region = image[y:y+h, x:x+w]

        # Save cropped face image
        cropped_face_path = os.path.splitext(image_path)[0] + "_face.jpg"
        cv2.imwrite(cropped_face_path, face_region)

        return cropped_face_path

    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["About", "Analyze", "FAQs", "Contact Us", "Product Gallery"],
        icons=["info-circle", "camera", "question-circle", "envelope", "images"],
        menu_icon="menu-app",
        default_index=1,
    )

# About Page
if selected == "About":
    st.title("About the System")
    st.markdown("""
        This AI-powered **Facial Skin Analysis System** helps you find the best cosmetics based on your skin.
        - Upload an image of your **face**.
        - The system **detects your skin tone, texture, type, and concerns**.
        - Personalized product recommendations are provided.
    """)

# Analyze Page
elif selected == "Analyze":
    st.title("Facial Skin Analysis")
    st.header("Upload a **clear image of your face**")

    # Upload Image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        cropped_face_path = detect_face(file_path)

        if cropped_face_path:
            # 🔹 Styled Card for Images
            st.markdown(
                """
                <style>
                .image-card {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    gap: 15px;
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    width: 100%;
                    text-align: center;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # 🔹 Show Images in a Card Layout
            col1, col2 = st.columns(2)
            with col1:
                st.image(file_path, caption="Uploaded Image", use_container_width=True)
            with col2:
                st.image(cropped_face_path, caption="Detected Face", use_container_width=True)

            # 🔹 Perform Skin Analysis
            st.subheader("Analysis Results")
            try:
                st.write("Processing fresh skin analysis...")
                skin_tone, skin_type, skin_concern, skin_texture = analyze_skin(cropped_face_path, force_refresh=True)
                st.write("Analysis completed.")

                # Display Results
                st.write(f"**Skin Tone:** {skin_tone}")
                st.write(f"**Skin Type:** {skin_type}")
                st.write(f"**Skin Concern:** {skin_concern}")
                st.write(f"**Skin Texture:** {skin_texture}")

                # Recommend Products
                st.subheader("Recommended Products")
                products = recommend_products(skin_tone, skin_type, skin_concern, skin_texture)

                if products:
                    for product in products:
                        product_name, category, image_path, product_link = product

                        if not os.path.exists(image_path) or not image_path:
                            image_path = "static/images/default_product.png"

                        st.image(image_path, caption=f"**{product_name}** ({category})", use_container_width=True)
                else:
                    st.write("No matching products found.")

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")

            # 🔹 Cleanup Files
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(cropped_face_path):
                os.remove(cropped_face_path)

            st.success("Analysis complete! Upload another image to analyze again.")


# FAQs Page
elif selected == "FAQs":
    st.title("Frequently Asked Questions")
    st.markdown("""
        **1. What type of image should I upload?**  
        - A **clear front-facing photo** of your face with **good lighting**.
        - Avoid makeup, filters, or obstructions (glasses, masks).

        **2. How does the system analyze my skin?**  
        - It detects your **skin tone, type, texture, and concerns**.
        - Uses a **pretrained AI model** to provide recommendations.

        **3. Are my photos stored?**  
        - **No.** Your images are **not stored** after analysis.
    """)

# Contact Us Page
elif selected == "Contact Us":
    st.title("Contact Us")
    st.markdown("""
        📧 **Email**: support@cosmetics-recommendation.com  
        📞 **Phone**: +123 456 7890  
        🏢 **Address**: 123 AI Lane, Skin City, Beautyland  
    """)

# Product Gallery Page
elif selected == "Product Gallery":
    st.title("Product Gallery")
    st.markdown("Browse through our curated skincare products.")

    products = fetch_gallery_products()

    if products:
        for product in products:
            product_name, category, image_path, product_link = product

            if not os.path.exists(image_path) or not image_path:
                image_path = "static/images/default_product.png"

            st.image(image_path, caption=f"**{product_name}** ({category})", use_container_width=True)  # ✅ FIXED
    else:
        st.warning("No products found in the database.")

# Close the database connection on app exit
import atexit
atexit.register(close_db_connection)
