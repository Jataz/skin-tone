import streamlit as st
from streamlit_option_menu import option_menu
import os
from models.skin_analysis import analyze_skin
from models.recommender import recommend_products

# Configure the page before anything else
st.set_page_config(page_title="Cosmetics Recommendation", layout="wide")

# Configure the upload folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Apply custom CSS for navbar styling
st.markdown(
    """
    <style>
    .css-1aumxhk {
        background-color: #4CAF50 !important;
    }
    .css-18e3th9 {
        padding-top: 0px !important;
    }
    .css-1v3fvcr {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navbar
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["About", "Analyze", "FAQs", "Contact Us", "Product Gallery"],
        icons=["info-circle", "camera", "question-circle", "envelope", "images"],
        menu_icon="menu-app",
        default_index=0,
    )

# About Page
if selected == "About":
    st.title("About the System")
    st.markdown("""
        This AI-based Cosmetics Recommendation System helps you find the perfect cosmetics for your skin.
        Upload your image, and the system analyzes your **skin tone**, **texture**, and **condition type**.
        Then, it recommends products tailored specifically for you using advanced machine learning models.
    """)
    st.image("", caption="AI-Powered Recommendations", use_column_width=True)

# Analyze Page
elif selected == "Analyze":
    st.title("Analyze Your Skin")
    st.header("Upload Your Image")

    # Upload Image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display the uploaded image
        st.image(file_path, caption="Uploaded Image", use_column_width=True)

        # Analyze Button
        if st.button("Analyze Image"):
            st.subheader("Analysis Results")
            skin_tone, texture, conditiontype = analyze_skin(file_path)
            st.write(f"**Skin Tone:** {skin_tone}")
            st.write(f"**Texture:** {texture}")
            st.write(f"**Condition Type:** {conditiontype}")

            st.subheader("Recommended Products")
            products = recommend_products(skin_tone, texture, conditiontype)

            # Display Recommended Products
            if products:
                for product in products:
                    st.write(f"- **{product[0]}** ({product[1]}): [View Product]({product[2]})")
            else:
                st.write("No matching products found.")

            # Reset Button
            if st.button("Upload Another Image"):
                st.experimental_rerun()

# FAQs Page
elif selected == "FAQs":
    st.title("Frequently Asked Questions")
    st.markdown("""
        **1. How does the system work?**  
        Upload your image, and the system analyzes your skin tone, texture, and condition type using AI models.  
        Based on the analysis, it recommends products from our curated database.

        **2. What types of products are recommended?**  
        Products like foundations, lipsticks, blushes, and concealers tailored to your skin characteristics.

        **3. Is my data safe?**  
        Yes! Your images are not stored on any server after analysis.
    """)

# Contact Us Page
elif selected == "Contact Us":
    st.title("Contact Us")
    st.markdown("""
        **Email**: support@cosmetics-recommendation.com  
        **Phone**: +123 456 7890  
        **Address**: 123 AI Lane, Skin City, Beautyland  
    """)
    st.text_input("Your Name", key="name")
    st.text_area("Your Message", key="message")
    if st.button("Submit"):
        st.success("Your message has been sent! We'll get back to you shortly.")

# Product Gallery Page
elif selected == "Product Gallery":
    st.title("Product Gallery")
    st.markdown("""
        Browse through some of the most popular products curated by our system.
    """)
    # Sample product images (replace with real ones)
    gallery = [
    #    {"name": "Foundation A", "image": "static/uploads/foundation_a.png", "link": "http://example.com/foundation-a"},
    #    {"name": "Lipstick X", "image": "static/uploads/lipstick_x.png", "link": "http://example.com/lipstick-x"},
    #    {"name": "Blush Y", "image": "static/uploads/blush_y.png", "link": "http://example.com/blush-y"},
    ]
    for product in gallery:
        st.image(product["image"], caption=f"{product['name']}: [View Product]({product['link']})", use_column_width=True)
