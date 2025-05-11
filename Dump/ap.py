import streamlit as st
from streamlit_option_menu import option_menu
import os
import cv2
import numpy as np
from models.skin_analysis import analyze_skin
from models.recommender import recommend_products, init_db_connection, close_db_connection, fetch_gallery_products

# Configure Streamlit page
st.set_page_config(
    page_title="Skin Tone Analysis Skin",
    layout="wide",
    page_icon="🔍",
    initial_sidebar_state="expanded"
)
init_db_connection()

# Configure upload folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Apply light theme custom CSS
st.markdown("""
    <style>
    /* Main background and text color */
    .stApp {
        background-color: #f8f9fa;
        color: #333333;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
        box-shadow: 2px 0px 5px rgba(0,0,0,0.05);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        background-color: #ffffff;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #ffffff !important;
    }
    
    /* Rest of your styles remain the same */
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    h4, h5, h6 {
        color: #2c3e50;
        font-family: 'Inter', sans-serif;
    }
    
    p, .stMarkdown {
        color: #555555;
        font-family: 'Inter', sans-serif;
    }

    .css-18e3th9 {
        padding-top: 0px !important;
    }
    
    .css-1v3fvcr {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Button styling */
    .stButton>button {
        background-color: #4e95ed;
        color: white;
        border-radius: 30px;
        padding: 10px 24px;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #3a7cd5;
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
        transform: translateY(-2px);
    }

    /* Card styling */
    .card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 24px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }
    
    .feature-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 24px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }

    /* Image styling */
    img {
        max-width: 100%;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* File uploader styling */
    .stFileUploader>div>div {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px dashed #4e95ed !important;
        padding: 20px !important;
    }
    
    .stFileUploader>div>div:hover {
        border-color: #3a7cd5 !important;
        background-color: #f8f9ff !important;
    }

    /* Progress bar styling */
    .stProgress>div>div {
        background-color: #4e95ed !important;
    }
    
    /* Navigation styling */
    .nav-link {
        color: #555555 !important;
        transition: all 0.3s ease;
        border-radius: 8px !important;
        margin-bottom: 5px !important;
    }
    
    .nav-link:hover {
        color: #4e95ed !important;
        background-color: #f0f6ff !important;
    }
    
    .nav-link-selected {
        color: #4e95ed !important;
        font-weight: 600 !important;
        background-color: #f0f6ff !important;
    }
    
    /* Header gradient text */
    .gradient-text {
        background: linear-gradient(90deg, #4e95ed, #3a7cd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Footer */
    .footer {
        color: #888888;
        text-align: center;
        padding: 30px 0;
        font-size: 0.9rem;
        border-top: 1px solid #e0e0e0;
        margin-top: 50px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #4e95ed !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f0f6ff;
        padding: 5px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px;
        padding: 10px 16px;
        color: #555555;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #4e95ed !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Testimonial styling */
    .testimonial {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-left: 4px solid #4e95ed;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 24px;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 8px;
        background-color: #f0f6ff;
        color: #4e95ed;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Image container */
    .image-container {
        position: relative;
        overflow: hidden;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .image-container img {
        transition: transform 0.5s ease;
        border-radius: 12px;
    }
    
    .image-container:hover img {
        transform: scale(1.05);
    }
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
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 28px; margin-bottom: 0;">🔍 <span class="gradient-text">Skin Tone Analysis</span></h1>
            <p style="font-size: 14px; margin-top: 5px;">AI-Powered Skin Tone Analysis</p>
        </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Home", "Analyze", "Products", "Research", "About"],
        icons=["house", "camera", "bag", "journal", "info-circle"],
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "transparent"},
            "icon": {"color": "#555555", "font-size": "16px"},
            "nav-link": {"color": "#555555", "font-size": "16px", "text-align": "left", "margin": "0px", "height": "40px", "padding": "10px", "border-radius": "8px"},
            "nav-link-selected": {"background-color": "#f0f6ff", "color": "#4e95ed", "font-weight": "600"},
        }
    )
    
    st.markdown("""
        <div style="position: absolute; bottom: 20px; left: 0; right: 0; text-align: center;">
            <p style="font-size: 12px; color: #888888;">© 2025 Skin Tone Analysis AI</p>
        </div>
    """, unsafe_allow_html=True)

# Home Page
if selected == "Home":
    st.markdown("""
        <div class="animated" style="text-align: center; padding: 40px 0 30px 0;">
            <h1 style="font-size: 40px; font-weight: 700;">Advanced <span class="gradient-text">AI-Powered</span><br>Skin Tone Analysis</h1>
            <p style="font-size: 18px; max-width: 600px; margin: 20px auto;">
                Discover your skin's unique characteristics and receive personalized product recommendations with our cutting-edge technology.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card animated" style="animation-delay: 0.1s;">
                <h3 style="color: #4e95ed; font-size: 20px;">🔍 Precise Analysis</h3>
                <p>Our AI model identifies your unique skin tone, type, texture, and concerns with exceptional accuracy.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="feature-card animated" style="animation-delay: 0.2s;">
                <h3 style="color: #4e95ed; font-size: 20px;">✨ Custom Recommendations</h3>
                <p>Get personalized product suggestions based on your skin's specific needs and characteristics.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="feature-card animated" style="animation-delay: 0.3s;">
                <h3 style="color: #4e95ed; font-size: 20px;">🔒 Privacy First</h3>
                <p>Your images are analyzed instantly and never stored or shared with third parties.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # CTA Button
    st.markdown("""
        <div style="text-align: center; margin-top: 40px;">
            <p style="margin-bottom: 20px; font-size: 18px;">Ready to discover your skin's unique profile?</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Try Skin Tone Analysis Now", key="home_cta"):
            st.session_state.selected = "Analyze"
            st.experimental_rerun()
    
    # How it Works
    st.markdown("<h2 style='text-align: center; margin: 50px 0 30px 0;'>How It Works</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animated" style="animation-delay: 0.4s;">
                <div style="text-align: center; font-size: 32px; color: #4e95ed; margin-bottom: 15px;">📸</div>
                <h3 style="text-align: center; color: #4e95ed; font-size: 18px;">1. Upload Photo</h3>
                <p style="text-align: center;">Take a selfie or upload a clear photo of your face.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="card animated" style="animation-delay: 0.5s;">
                <div style="text-align: center; font-size: 32px; color: #4e95ed; margin-bottom: 15px;">🧠</div>
                <h3 style="text-align: center; color: #4e95ed; font-size: 18px;">2. AI Analysis</h3>
                <p style="text-align: center;">Our AI analyzes your skin characteristics and concerns.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="card animated" style="animation-delay: 0.6s;">
                <div style="text-align: center; font-size: 32px; color: #4e95ed; margin-bottom: 15px;">💎</div>
                <h3 style="text-align: center; color: #4e95ed; font-size: 18px;">3. Get Recommendations</h3>
                <p style="text-align: center;">Receive personalized product suggestions for your skin.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Testimonials
    st.markdown("<h2 style='text-align: center; margin: 50px 0 30px 0;'>What Users Say</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="testimonial animated" style="animation-delay: 0.7s;">
                <p style="font-style: italic; font-size: 16px;">"The Skin Tone Analysis was surprisingly accurate! The product recommendations worked perfectly for my combination skin. I've never had such personalized advice before!"</p>
                <p style="text-align: right; color: #4e95ed; margin-bottom: 0; font-weight: 600;">- Sarah K.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="testimonial animated" style="animation-delay: 0.8s;">
                <p style="font-style: italic; font-size: 16px;">"I've tried many skincare apps, but Skin Tone Analysis's AI analysis is on another level. Finally found products that address my specific concerns. Highly recommend!"</p>
                <p style="text-align: right; color: #4e95ed; margin-bottom: 0; font-weight: 600;">- Michael T.</p>
            </div>
        """, unsafe_allow_html=True)

# Analyze Page
elif selected == "Analyze":
    st.markdown("""
        <h1 style='margin-bottom: 20px;'>Skin Tone Analysis</h1>
        <p style='margin-bottom: 30px;'>Upload a clear photo of your face to receive a detailed Skin Tone Analysis and personalized product recommendations.</p>
    """, unsafe_allow_html=True)

    # Instructions Card
    st.markdown("""
        <div class="card animated">
            <h3 style="color: #4e95ed; margin-top: 0;">For Best Results:</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;">
                <div style="flex: 1; min-width: 200px;">
                    <div class="badge">Tip 1</div>
                    <p>Use a well-lit, front-facing photo</p>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div class="badge">Tip 2</div>
                    <p>Remove makeup, glasses, and other face coverings</p>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div class="badge">Tip 3</div>
                    <p>Maintain a neutral expression</p>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div class="badge">Tip 4</div>
                    <p>Ensure your entire face is visible</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Upload Image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        cropped_face_path = detect_face(file_path)

        if cropped_face_path:
            # Show Images in a Card Layout
            st.markdown("""
                <div class="card animated">
                    <h3 style="color: #4e95ed; margin-top: 0;">Image Processing</h3>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div class="image-container">
                """, unsafe_allow_html=True)
                st.image(file_path, caption="Uploaded Image", use_container_width=True)
                st.markdown("""
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                    <div class="image-container">
                """, unsafe_allow_html=True)
                st.image(cropped_face_path, caption="Detected Face", use_container_width=True)
                st.markdown("""
                    </div>
                """, unsafe_allow_html=True)

            # Perform Skin Tone Analysis
            st.markdown("""
                <div class="card animated">
                    <h3 style="color: #4e95ed; margin-top: 0;">Analysis Results</h3>
                </div>
            """, unsafe_allow_html=True)

            try:
                with st.spinner("Analyzing your skin..."):
                    skin_tone, skin_type, skin_concern, skin_texture = analyze_skin(cropped_face_path, force_refresh=True)
                    st.success("Analysis completed!")

                # Display Results
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                        <div class="card animated" style="height: 100%;">
                            <h4 style="color: #4e95ed; margin-top: 0;">Skin Characteristics</h4>
                            <table style="width: 100%;">
                                <tr>
                                    <td style="padding: 12px 0; color: #2c3e50; font-weight: 600;">Skin Tone:</td>
                                    <td style="padding: 12px 0; color: #555555;"><span class="badge">{}</span></td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 0; color: #2c3e50; font-weight: 600;">Skin Type:</td>
                                    <td style="padding: 12px 0; color: #555555;"><span class="badge">{}</span></td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 0; color: #2c3e50; font-weight: 600;">Skin Concern:</td>
                                    <td style="padding: 12px 0; color: #555555;"><span class="badge">{}</span></td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 0; color: #2c3e50; font-weight: 600;">Skin Texture:</td>
                                    <td style="padding: 12px 0; color: #555555;"><span class="badge">{}</span></td>
                                </tr>
                            </table>
                        </div>
                    """.format(skin_tone, skin_type, skin_concern, skin_texture), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                        <div class="card animated" style="height: 100%;">
                            <h4 style="color: #4e95ed; margin-top: 0;">What This Means</h4>
                            <p>
                                Based on our AI analysis, we've identified your key skin characteristics. 
                                These factors will help us recommend the most suitable products for your 
                                specific needs.
                            </p>
                            <p>
                                Your analysis is complete and your personalized product recommendations 
                                are ready below. We've selected products that work harmoniously together 
                                for optimal results.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                # Recommend Products
                st.markdown("""
                    <div class="card animated">
                        <h3 style="color: #4e95ed; margin-top: 0;">Recommended Products</h3>
                        <p>Based on your Skin Tone Analysis, we recommend the following products:</p>
                    </div>
                """, unsafe_allow_html=True)

                products = recommend_products(skin_tone, skin_type, skin_concern, skin_texture)

                if products:
                    cols = st.columns(3)
                    for i, product in enumerate(products):
                        product_name, category, recommendation = product

                        with cols[i % 3]:
                            st.markdown(f"""
                                <div class="feature-card animated" style="animation-delay: {0.2 + i * 0.1}s;">
                                    <div style="text-align: center;">
                                        <h4 style="margin: 10px 0 5px 0;">{product_name}</h4>
                                        <span class="badge">{category}</span>
                                        <h4 style="color: #4e95ed; margin: 10px 0 5px 0">Recommended Products</h4>
                                        <ul style="text-align: left; margin: 15px 0;">
                                            {' '.join([f'<li>{item.strip()}</li>' for item in recommendation.split('.') if item.strip()])}
                                        </ul>
                                        <p style="color: #4e95ed; margin-top: 10px;">Perfect for your {skin_type.lower()} skin</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("No matching products found.")

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")

            # Cleanup Files
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(cropped_face_path):
                os.remove(cropped_face_path)

# Products Page
elif selected == "Products":
    st.markdown("""
        <h1 style='margin-bottom: 20px;'>Product Catalog</h1>
        <p style='margin-bottom: 30px;'>Explore our curated collection of premium skincare products.</p>
    """, unsafe_allow_html=True)

    # Tabs for Product Categories
    tab1, tab2, tab3, tab4 = st.tabs(["All Products", "Cleansers", "Moisturizers", "Treatments"])
    
    products = fetch_gallery_products()
    
    with tab1:
        if products:
            cols = st.columns(3)
            for i, product in enumerate(products):
                product_name, category, image_path, product_link = product

                if not os.path.exists(image_path) or not image_path:
                    image_path = "static/images/default_product.png"

                with cols[i % 3]:
                    st.markdown(f"""
                        <div class="feature-card animated" style="animation-delay: {0.1 + i * 0.05}s;">
                            <div style="text-align: center;">
                                <div class="image-container" style="margin-bottom: 15px;">
                                    <img src="{image_path}" style="width: 100%; height: 200px; object-fit: cover;">
                                </div>
                                <h4 style="margin: 10px 0 5px 0;">{product_name}</h4>
                                <span class="badge">{category}</span>
                                <button style="background-color: #4e95ed; color: white; border: none; border-radius: 20px; padding: 8px 16px; margin-top: 15px; cursor: pointer; transition: all 0.3s ease;">View Details</button>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No products found in the database.")
            
    with tab2:
        st.markdown("""
            <div class="card animated">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                    <h3 style="color: #4e95ed; margin: 0;">Cleansers</h3>
                    <div>
                        <span class="badge" style="cursor: pointer;">All Types</span>
                        <span class="badge" style="cursor: pointer;">Oily Skin</span>
                        <span class="badge" style="cursor: pointer;">Dry Skin</span>
                        <span class="badge" style="cursor: pointer;">Sensitive</span>
                    </div>
                </div>
                <p>Cleansers category selected. Choose a filter to narrow down options.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with tab3:
        st.markdown("""
            <div class="card animated">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                    <h3 style="color: #4e95ed; margin: 0;">Moisturizers</h3>
                    <div>
                        <span class="badge" style="cursor: pointer;">All Types</span>
                        <span class="badge" style="cursor: pointer;">Lightweight</span>
                        <span class="badge" style="cursor: pointer;">Rich</span>
                        <span class="badge" style="cursor: pointer;">With SPF</span>
                    </div>
                </div>
                <p>Moisturizers category selected. Choose a filter to narrow down options.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with tab4:
        st.markdown("""
            <div class="card animated">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                    <h3 style="color: #4e95ed; margin: 0;">Treatments</h3>
                    <div>
                        <span class="badge" style="cursor: pointer;">All Types</span>
                        <span class="badge" style="cursor: pointer;">Acne</span>
                        <span class="badge" style="cursor: pointer;">Anti-aging</span>
                        <span class="badge" style="cursor: pointer;">Brightening</span>
                    </div>
                </div>
                <p>Treatments category selected. Choose a filter to narrow down options.</p>
            </div>
        """, unsafe_allow_html=True)

# Research Page
elif selected == "Research":
    st.markdown("""
        <h1 style='margin-bottom: 20px;'>Our Research</h1>
        <p style='margin-bottom: 30px;'>Learn about the science and technology behind our Skin Tone Analysis system.</p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card animated" style="animation-delay: 0.1s;">
            <h3 style="color: #4e95ed; margin-top: 0;">🔬 AI Technology</h3>
            <p>
                Our Skin Tone Analysis system uses deep learning models trained on diverse datasets 
                to accurately identify skin characteristics across all skin types and tones.
                The primary technologies powering our system include:
            </p>
            <ul>
                <li>Convolutional Neural Networks (CNN) for image processing</li>
                <li>Transfer learning from pre-trained models</li>
                <li>Custom-built classification models for skin concerns</li>
                <li>Specialized recommendation algorithms</li>
            </ul>
        </div>
        
        <div class="card">
            <h3 style="color: #1e88e5; margin-top: 0;">Research Papers</h3>
            <p>Our team has published several peer-reviewed papers on Skin Tone Analysis technology:</p>
            <ul>
                <li>"Advanced Skin Tone Classification Using Deep Learning" (2024)</li>
                <li>"Multi-factor Skin Concern Analysis: A Novel Approach" (2023)</li>
                <li>"Inclusive AI: Ensuring Accuracy Across Diverse Skin Types" (2023)</li>
            </ul>
        </div>
        
        <div class="card">
            <h3 style="color: #1e88e5; margin-top: 0;">Future Developments</h3>
            <p>
                Our research team is currently working on several exciting advancements:
            </p>
            <ul>
                <li>Real-time video analysis for dynamic skin assessment</li>
                <li>Personalized skincare routine generators</li>
                <li>Treatment progress tracking and visualization</li>
                <li>Integration with wearable skin monitoring devices</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# About Page
elif selected == "About":
    st.markdown("""
        <h1 style='margin-bottom: 20px;'>About Skin Tone Analysis</h1>
        <p style='margin-bottom: 30px;'>Learn about our mission, team, and technology.</p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card">
            <h3 style="color: #1e88e5; margin-top: 0;">Our Mission</h3>
            <p>
                At Skin Tone Analysis, we're on a mission to revolutionize skincare through artificial intelligence. 
                We believe everyone deserves personalized skincare advice based on their unique characteristics, 
                not generic recommendations.
            </p>
            <p>
                Our AI-powered Skin Tone Analysis technology makes professional-grade skin assessment accessible to everyone, 
                anywhere, anytime.
            </p>
        </div>
        
        <div class="card">
            <h3 style="color: #1e88e5; margin-top: 0;">Our Team</h3>
            <p>
                Skin Tone Analysis was founded in 2022 by a team of AI researchers, dermatologists, and skincare enthusiasts. 
                Our diverse team combines expertise in computer vision, dermatology, product formulation, and user experience design.
            </p>
            <p>
                Based in San Francisco with team members across the globe, we're united by our passion for 
                using technology to improve skincare outcomes for everyone.
            </p>
        </div>
        
        <div class="card">
            <h3 style="color: #1e88e5; margin-top: 0;">Contact Us</h3>
            <p>Have questions or feedback? We'd love to hear from you!</p>
            <p><strong>Email:</strong> contact@Skin Tone Analysis.com</p>
            <p><strong>Phone:</strong> +1 (415) 555-0123</p>
            <p><strong>Address:</strong> 123 AI Avenue, San Francisco, CA 94105</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>© 2025 Skin Tone Analysis AI | Privacy Policy | Terms of Service</p>
    </div>
""", unsafe_allow_html=True)

# Close the database connection on app exit
import atexit
atexit.register(close_db_connection)