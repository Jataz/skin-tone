import streamlit as st
from models.skin_analysis import analyze_skin
from models.recommender import recommend_products
import os

# Configure upload folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Streamlit App
st.title("AI-Based Cosmetics Recommendation System")

# Image Upload
st.header("Upload Your Image")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded file
    image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="Uploaded Image", use_column_width=True)

    # Analyze Skin
    skin_tone, texture, conditiontype = analyze_skin(image_path)
    st.write(f"**Detected Skin Tone:** {skin_tone}")
    st.write(f"**Skin Texture:** {texture}")
    st.write(f"**Skin conditiontype:** {conditiontype}")

    # Recommendations
    st.header("Recommended Products")
    products = recommend_products(skin_tone, texture, conditiontype)
    if products:
        for product in products:
            st.write(f"- **{product[0]}** ({product[1]}): [View Product]({product[2]})")
    else:
        st.write("No matching products found.")
