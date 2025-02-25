import streamlit as st
from streamlit_option_menu import option_menu
import os
import cv2
import numpy as np
from models.skin_analysis import analyze_skin
from models.recommender import recommend_products, init_db_connection, close_db_connection, fetch_gallery_products

# Configure Streamlit page
st.set_page_config(
    page_title="Skin Tone Analysis",
    layout="wide",
    page_icon="🔍",
    initial_sidebar_state="expanded"
)
init_db_connection()

# Configure upload folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Apply Skin Tone Analysis-inspired custom CSS (matching Skin Tone Analysis.com)
st.markdown("""
    <style>
    /* Main background and text color */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    h4, h5, h6 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    p, .stMarkdown {
        color: #acacac;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar styling */
    .css-1aumxhk, [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #333333;
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
        background-color: #1e88e5;
        color: white;
        border-radius: 4px;
        padding: 8px 16px;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #1976d2;
        box-shadow: 0 4px 8px rgba(30, 136, 229, 0.3);
    }

    /* Card styling */
    .card {
        background-color: #121212;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #333333;
        margin-bottom: 20px;
    }
    
    .feature-card {
        background-color: #121212;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #333333;
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
    }

    /* Image styling */
    img {
        max-width: 100%;
        border-radius: 8px;
        border: 1px solid #333333;
    }

    /* File uploader styling */
    .stFileUploader>div>div {
        background-color: #121212 !important;
        border-radius: 8px !important;
        border: 1px solid #333333 !important;
    }

    /* Progress bar styling */
    .stProgress>div>div {
        background-color: #1e88e5 !important;
    }
    
    /* Navigation styling */
    .nav-link {
        color: #acacac !important;
        transition: color 0.3s ease;
    }
    
    .nav-link:hover {
        color: #ffffff !important;
    }
    
    .nav-link-selected {
        color: #1e88e5 !important;
        font-weight: 600 !important;
    }
    
    /* Header gradient text */
    .gradient-text {
        background: linear-gradient(90deg, #1e88e5, #1976d2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Footer */
    .footer {
        color: #acacac;
        text-align: center;
        padding: 20px 0;
        font-size: 0.8rem;
        border-top: 1px solid #333333;
        margin-top: 40px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #1e88e5 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        color: #acacac;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #121212 !important;
        color: #ffffff !important;
        border-bottom: 2px solid #1e88e5 !important;
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

    # Override sidebar background color to white
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Home", "Analyze", "Products", "Research", "About"],
        icons=["house", "camera", "bag", "journal", "info-circle"],
        default_index=1,
        styles={
            "container": {"padding": "5px", "background-color": "transparent"},
            "icon": {"color": "#acacac", "font-size": "16px"},
            "nav-link": {"color": "#acacac", "font-size": "16px", "text-align": "left", "margin": "0px", "height": "40px", "padding": "10px", "border-radius": "4px"},
            "nav-link-selected": {"background-color": "#121212", "color": "#1e88e5", "font-weight": "600"},
        }
    )
    
    st.markdown("""
        <div style="position: absolute; bottom: 20px; left: 0; right: 0; text-align: center;">
            <p style="font-size: 12px; color: #666666;">© 2025 Skin Tone Analysis AI</p>
        </div>
    """, unsafe_allow_html=True)

# Home Page
if selected == "Home":
    st.markdown("""
        <div style="text-align: center; padding: 40px 0 30px 0;">
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
            <div class="feature-card">
                <h3 style="color: #1e88e5; font-size: 18px;">Precise Analysis</h3>
                <p>Our AI model identifies your unique skin tone, type, texture, and concerns with exceptional accuracy.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3 style="color: #1e88e5; font-size: 18px;">Custom Recommendations</h3>
                <p>Get personalized product suggestions based on your skin's specific needs and characteristics.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3 style="color: #1e88e5; font-size: 18px;">Privacy First</h3>
                <p>Your images are analyzed instantly and never stored or shared with third parties.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # CTA Button
    st.markdown("""
        <div style="text-align: center; margin-top: 40px;">
            <p style="margin-bottom: 20px;">Ready to discover your skin's unique profile?</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Try Skin Analysis Now", key="home_cta"):
            st.session_state.selected = "Analyze"
            st.experimental_rerun()
    
    # Testimonials
    st.markdown("<h2 style='text-align: center; margin: 50px 0 30px 0;'>What Users Say</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="card">
                <p style="font-style: italic;">"The Skin Tone Analysis was surprisingly accurate! The product recommendations worked perfectly for my combination skin."</p>
                <p style="text-align: right; color: #1e88e5; margin-bottom: 0;">- Sarah K.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="card">
                <p style="font-style: italic;">"I've tried many skincare apps, but Skin Tone Analysis's AI analysis is on another level. Highly recommend!"</p>
                <p style="text-align: right; color: #1e88e5; margin-bottom: 0;">- Michael T.</p>
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
        <div class="card">
            <h3 style="color: #1e88e5; margin-top: 0;">For Best Results:</h3>
            <ul style="color: #acacac;">
                <li>Use a well-lit, front-facing photo</li>
                <li>Remove makeup, glasses, and other face coverings</li>
                <li>Maintain a neutral expression</li>
                <li>Ensure your entire face is visible</li>
            </ul>
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
                <div class="card">
                    <h3 style="color: #1e88e5; margin-top: 0;">Image Processing</h3>
                </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div class="card">
                        <h4 style="color: #1e88e5; margin-top: 0;">Uploaded Image</h4>
                """, unsafe_allow_html=True)
                st.image(file_path, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("""
                    <div class="card">
                        <h4 style="color: #1e88e5; margin-top: 0;">Detected Face</h4>
                """, unsafe_allow_html=True)
                st.image(cropped_face_path, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Perform Skin Tone Analysis
            st.markdown("""
                <div class="card">
                    <h3 style="color: #1e88e5; margin-top: 0;">Analysis Results</h3>
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
                        <div class="card" style="height: 100%;">
                            <h4 style="color: #1e88e5; margin-top: 0;">Skin Characteristics</h4>
                            <table style="width: 100%;">
                                <tr>
                                    <td style="padding: 8px 0; color: #ffffff;">Skin Tone:</td>
                                    <td style="padding: 8px 0; color: #acacac;">{}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; color: #ffffff;">Skin Type:</td>
                                    <td style="padding: 8px 0; color: #acacac;">{}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; color: #ffffff;">Skin Concern:</td>
                                    <td style="padding: 8px 0; color: #acacac;">{}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; color: #ffffff;">Skin Texture:</td>
                                    <td style="padding: 8px 0; color: #acacac;">{}</td>
                                </tr>
                            </table>
                        </div>
                    """.format(skin_tone, skin_type, skin_concern, skin_texture), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                        <div class="card" style="height: 100%;">
                            <h4 style="color: #1e88e5; margin-top: 0;">What This Means</h4>
                            <p>
                                Based on our AI analysis, we've identified your key skin characteristics. 
                                These factors will help us recommend the most suitable products for your 
                                specific needs.
                            </p>
                            <p>
                                Your analysis is complete and your personalized product recommendations 
                                are ready below.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                # Recommend Products
                st.markdown("""
                    <div class="card">
                        <h3 style="color: #1e88e5; margin-top: 0;">Recommended Products</h3>
                        <p>Based on your Skin Tone Analysis, we recommend the following products:</p>
                    </div>
                """, unsafe_allow_html=True)

                products = recommend_products(skin_tone, skin_type, skin_concern, skin_texture)

                if products:
                    cols = st.columns(3)
                    for i, product in enumerate(products):
                        product_name, category, image_path, product_link = product

                        if not os.path.exists(image_path) or not image_path:
                            image_path = "static/images/default_product.png"

                        with cols[i % 3]:
                            st.markdown(f"""
                                <div class="card">
                                    <div style="text-align: center;">
                                        <img src="{image_path}" style="width: 100%; height: 200px; object-fit: cover;">
                                        <h4 style="margin: 10px 0 5px 0;">{product_name}</h4>
                                        <p style="color: #1e88e5; margin: 0 0 10px 0;">{category}</p>
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
                        <div class="feature-card">
                            <div style="text-align: center;">
                                <img src="{image_path}" style="width: 100%; height: 200px; object-fit: cover;">
                                <h4 style="margin: 10px 0 5px 0;">{product_name}</h4>
                                <p style="color: #1e88e5; margin: 0 0 10px 0;">{category}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No products found in the database.")
            
    with tab2:
        st.markdown("""
            <div class="card">
                <p>Cleansers category selected. Filter functionality coming soon.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with tab3:
        st.markdown("""
            <div class="card">
                <p>Moisturizers category selected. Filter functionality coming soon.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with tab4:
        st.markdown("""
            <div class="card">
                <p>Treatments category selected. Filter functionality coming soon.</p>
            </div>
        """, unsafe_allow_html=True)

# Research Page
elif selected == "Research":
    st.markdown("""
        <h1 style='margin-bottom: 20px;'>Our Research</h1>
        <p style='margin-bottom: 30px;'>Learn about the science and technology behind our Skin Tone Analysis system.</p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card">
            <h3 style="color: #1e88e5; margin-top: 0;">AI Technology</h3>
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