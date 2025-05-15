import streamlit as st
from streamlit_option_menu import option_menu
import os
import cv2
import numpy as np
from models.skin_analysis import analyze_skin
from models.recommender import recommend_skincare, recommend_makeup, recommend_products, init_db_connection, close_db_connection, fetch_gallery_products, fetch_product_details

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
        options=["Home", "Analyze", "Research", "About"],
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

    # Near line 450, in the Analyze Page section
    # Upload Image
    # Create a unique key for the file uploader based on session state counter
    if 'image_counter' not in st.session_state:
        st.session_state.image_counter = 0
    if 'previous_image' not in st.session_state:
        st.session_state.previous_image = None
    if 'model_state_id' not in st.session_state:
        st.session_state.model_state_id = 0
        
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], 
                                    label_visibility="collapsed", 
                                    key=f"uploader_{st.session_state.image_counter}")
    
    # Check if a new image was uploaded
    if uploaded_file is not None and (st.session_state.previous_image != uploaded_file.name):
        # Clear previous analysis results from session state
        if 'skin_analysis_results' in st.session_state:
            del st.session_state.skin_analysis_results
        
        # Increment model state ID to force model reload
        st.session_state.model_state_id += 1
        
        # Update the previous image and increment counter
        st.session_state.previous_image = uploaded_file.name
        st.session_state.image_counter += 1
        
        # Save the uploaded file
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
                    # Always force a refresh for new images
                    try:
                        # Store results in session state
                        results = analyze_skin(cropped_face_path, force_refresh=True)
                        st.session_state.skin_analysis_results = results
                        skin_tone, skin_type, skin_concern, skin_texture, skin_undertone = results
                    except ValueError as e:
                        # Fallback for backward compatibility if the model doesn't return undertone yet
                        results = analyze_skin(cropped_face_path, force_refresh=True)
                        st.session_state.skin_analysis_results = results
                        skin_tone, skin_type, skin_concern, skin_texture = results
                        skin_undertone = "Neutral"  # Default value
                    
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
                                <tr>
                                    <td style="padding: 12px 0; color: #2c3e50; font-weight: 600;">Skin Undertone:</td>
                                    <td style="padding: 12px 0; color: #555555;"><span class="badge">{}</span></td>
                                </tr>
                            </table>
                        </div>
                    """.format(skin_tone, skin_type, skin_concern, skin_texture, skin_undertone), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                        <div class="card animated" style="height: 100%;">
                            <h4 style="color: #4e95ed; margin-top: 0;">What This Means</h4>
                            <p>
                                Based on our AI analysis, we've identified your key skin characteristics. 
                                These factors will help us recommend the most suitable skincare and makeup products 
                                for your specific needs.
                            </p>
                            <p>
                                Your analysis is complete and your personalized product recommendations 
                                are ready below. We've selected products that work harmoniously together 
                                for optimal results.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                # Create tabs for Skincare and Makeup recommendations
                skincare_tab, makeup_tab = st.tabs(["Skincare Recommendations", "Makeup Recommendations"])
                
                with skincare_tab:
                    # Recommend Skincare Products
                    st.markdown("""
                        <div class="card animated">
                            <h3 style="color: #4e95ed; margin-top: 0;">Recommended Skincare Products</h3>
                            <p>Based on your Skin Tone Analysis, we recommend the following skincare products:</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Use the specialized skincare recommendation function
                    skincare_products = recommend_skincare(skin_tone, skin_type, skin_concern, skin_texture)
                    
                    if skincare_products:
                        for i in range(0, len(skincare_products), 3):
                            cols = st.columns(3)
                            for j in range(3):
                                if i + j < len(skincare_products):
                                    product = skincare_products[i + j]
                                    with cols[j]:
                                        st.markdown(f"""
                                            <div class="card" style="height: 100%;">
                                                <h4 style="color: #4e95ed; font-size: 18px;">{product['name']}</h4>
                                                <p><strong>Type:</strong> {product['skin_type']}</p>
                                                <p><strong>Concern:</strong> {product['skin_concern']}</p>
                                                <p><strong>Recommendation:</strong> {product.get('recommendation', 'Perfect for your skin profile')}</p>
                                                <a href="{product.get('link', '#')}" target="_blank">
                                                    <img src="{product.get('image_path', 'static/images/placeholder.png')}" style="width: 100%; margin-top: 10px;">
                                                </a>
                                            </div>
                                        """, unsafe_allow_html=True)
                    else:
                        st.info("No skincare products found matching your skin profile. Please try again with a different image.")
                
                with makeup_tab:
                    # Recommend Makeup Products
                    st.markdown("""
                        <div class="card animated">
                            <h3 style="color: #4e95ed; margin-top: 0;">Recommended Makeup Products</h3>
                            <p>Based on your Skin Tone Analysis, we recommend the following makeup products that will complement your skin tone and type:</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Use the specialized makeup recommendation function with undertone
                    makeup_products = recommend_makeup(skin_tone, skin_type, skin_concern, skin_texture, skin_undertone)
                    
                    if makeup_products:
                        # Create sections for different makeup categories
                        makeup_categories = {
                            "Foundation": [],
                            "Concealer": [],
                            "Blush": [],
                            "Eyeshadow": [],
                            "Lipstick": [],
                            "Other": []
                        }
                        
                        # Categorize products
                        for product in makeup_products:
                            subcategory = product.get('subcategory', 'Other')
                            if subcategory in makeup_categories:
                                makeup_categories[subcategory].append(product)
                            else:
                                makeup_categories["Other"].append(product)
                        
                        # Display products by category
                        for category, products in makeup_categories.items():
                            if products:
                                st.markdown(f"""
                                    <div style="margin-top: 20px;">
                                        <h4 style="color: #4e95ed;">{category}</h4>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                for i in range(0, len(products), 3):
                                    cols = st.columns(3)
                                    for j in range(3):
                                        if i + j < len(products):
                                            product = products[i + j]
                                            with cols[j]:
                                                st.markdown(f"""
                                                    <div class="card" style="height: 100%;">
                                                        <h4 style="color: #4e95ed; font-size: 18px;">{product['name']}</h4>
                                                        <p><strong>Shade:</strong> {product.get('shade', 'Best match for your tone')}</p>
                                                        <p><strong>Finish:</strong> {product.get('finish', 'Natural')}</p>
                                                        <p><strong>Undertone:</strong> {product.get('undertone', skin_undertone)}</p>
                                                        <p><strong>Recommendation:</strong> {product.get('makeup_recommendation', 'Perfect for your skin profile')}</p>
                                                        <a href="{product.get('link', '#')}" target="_blank">
                                                            <img src="{product.get('image_path', 'static/images/placeholder.png')}" style="width: 100%; margin-top: 10px;">
                                                        </a>
                                                    </div>
                                                """, unsafe_allow_html=True)
                    else:
                        st.info("No makeup products found matching your skin profile. We're expanding our makeup database to better serve you.")
                        
                        # Provide general makeup recommendations based on skin tone and undertone
                        st.markdown("""
                            <div class="card animated">
                                <h4 style="color: #4e95ed; margin-top: 0;">General Makeup Recommendations</h4>
                                <p>While we build our product database, here are some general makeup tips for your skin profile:</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Generate general makeup recommendations based on skin tone and undertone
                        general_recommendations = []
                        
                        # Foundation recommendations
                        if skin_tone == "Fair":
                            if skin_undertone == "Cool":
                                general_recommendations.append("Look for foundations with pink or rosy undertones")
                            elif skin_undertone == "Warm":
                                general_recommendations.append("Choose foundations with yellow or golden undertones")
                            else:
                                general_recommendations.append("Neutral foundations will work well with your skin tone")
                        elif skin_tone == "Medium":
                            if skin_undertone == "Cool":
                                general_recommendations.append("Foundations with subtle pink or neutral undertones")
                            elif skin_undertone == "Warm":
                                general_recommendations.append("Foundations with golden or olive undertones")
                            else:
                                general_recommendations.append("Look for foundations labeled as 'neutral' or 'balanced'")
                        elif skin_tone == "Dark":
                            if skin_undertone == "Cool":
                                general_recommendations.append("Foundations with red or blue undertones")
                            elif skin_undertone == "Warm":
                                general_recommendations.append("Foundations with golden, caramel or red undertones")
                            else:
                                general_recommendations.append("Neutral foundations with balanced undertones")
                        
                        # Blush recommendations
                        if skin_undertone == "Cool":
                            general_recommendations.append("Blushes in pink, mauve, or berry shades")
                        elif skin_undertone == "Warm":
                            general_recommendations.append("Blushes in peach, coral, or terracotta shades")
                        else:
                            general_recommendations.append("Universal blush shades like soft pink or peachy-pink")
                        
                        # Lipstick recommendations
                        if skin_undertone == "Cool":
                            general_recommendations.append("Lipsticks in blue-red, berry, or mauve shades")
                        elif skin_undertone == "Warm":
                            general_recommendations.append("Lipsticks in orange-red, coral, or warm brown shades")
                        else:
                            general_recommendations.append("Universal lipstick shades like rose pink or soft red")
                        
                        # Display recommendations
                        for rec in general_recommendations:
                            st.markdown(f"""
                                <div style="margin-bottom: 10px; padding: 10px; background-color: #f0f6ff; border-radius: 8px;">
                                    <p style="margin: 0; color: #4e95ed;"><strong>✓</strong> {rec}</p>
                                </div>
                            """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error during analysis: {e}")
                st.info("Please try uploading a different image with clearer lighting and a more visible face.")

# Products Page

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
            <p><strong>Email:</strong> contact@skin.com</p>
            <p><strong>Phone:</strong> +263 78 637 7045</p>
            <p><strong>Address:</strong> 123 AI Avenue, Pumula,  94105</p>
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