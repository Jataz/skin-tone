import tensorflow as tf
import numpy as np
import os
from PIL import Image
import streamlit as st

# Configure TensorFlow (Ensure GPU Memory Growth)
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Define Class Labels
SKIN_TONE_LABELS = ["Fair", "Medium", "Dark"]
SKIN_TYPE_LABELS = ["Normal", "Dry", "Oily", "Combination", "Sensitive"]
SKIN_CONCERN_LABELS = [
    "Cystic Acne", "Blackheads", "Whiteheads",
    "Hyperpigmentation", "Melasma", "Dark Spots",
    "Fine Lines", "Wrinkles", "Aging",
    "Dullness", "Dehydration",
    "Redness", "Rosacea", "Irritation", "Sunburn"
]
SKIN_TEXTURE_LABELS = [
    "Velvety", "Soft", "Smooth",
    "Flaky", "Harsh", "Rough",
    "Patchy", "Uneven", "Bumpy",
    "Large Pores",
    "Peeling", "Tight", "Scaly"
]

# Add makeup-specific undertone detection
SKIN_UNDERTONE_LABELS = ["Cool", "Neutral", "Warm"]

# Load Pre-trained Model (Modified for Multi-Output)
# Initialize model variable globally
model = None  

def load_model(model_name="EfficientNetB0"):
    """Loads the model only once and keeps it in memory.
    
    Args:
        model_name (str): Name of the pretrained model to use as base.
                          Options: "EfficientNetB0", "EfficientNetB3", "MobileNetV2", 
                          "ResNet50V2", "DenseNet121", "NASNetMobile", "Xception"
    """
    global model  # Ensure we use a single instance

    if model is None:  # Load only if not already loaded
        print(f"DEBUG: Loading the skin analysis model with {model_name} base...")
        
        # Check if we have a pre-trained model file
        model_path = os.path.join(os.path.dirname(__file__), "est_fitzpatrick_skin_tone_model.keras")
        
        if os.path.exists(model_path):
            print(f"DEBUG: Loading pre-trained model from {model_path}")
            model = tf.keras.models.load_model(model_path)
            return model
            
        # If no pre-trained model exists, create a new one with the specified base model
        # Select base model according to parameter
        if model_name == "EfficientNetB0":
            base_model = tf.keras.applications.EfficientNetB0(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        elif model_name == "EfficientNetB3":
            base_model = tf.keras.applications.EfficientNetB3(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        elif model_name == "MobileNetV2":
            base_model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        elif model_name == "ResNet50V2":
            base_model = tf.keras.applications.ResNet50V2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        elif model_name == "DenseNet121":
            base_model = tf.keras.applications.DenseNet121(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        elif model_name == "NASNetMobile":
            base_model = tf.keras.applications.NASNetMobile(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        elif model_name == "Xception":
            base_model = tf.keras.applications.Xception(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        else:
            print(f"WARNING: Unknown model name '{model_name}', defaulting to EfficientNetB0")
            base_model = tf.keras.applications.EfficientNetB0(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        
        # Fine-tune the top layers of the base model
        base_model.trainable = True
        for layer in base_model.layers[:-20]:  # Freeze all but the last 20 layers
            layer.trainable = False

        # Add Global Pooling Layer
        x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
        
        # Improve feature extraction with more complex layers
        x = tf.keras.layers.Dense(1024, activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.4)(x)  # Increased dropout for better generalization
        x = tf.keras.layers.Dense(512, activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.3)(x)

        # Define Outputs
        skin_tone_output = tf.keras.layers.Dense(len(SKIN_TONE_LABELS), activation='softmax', name="skin_tone")(x)
        skin_type_output = tf.keras.layers.Dense(len(SKIN_TYPE_LABELS), activation='softmax', name="skin_type")(x)
        skin_concern_output = tf.keras.layers.Dense(len(SKIN_CONCERN_LABELS), activation='softmax', name="skin_concern")(x)
        skin_texture_output = tf.keras.layers.Dense(len(SKIN_TEXTURE_LABELS), activation='softmax', name="skin_texture")(x)
        skin_undertone_output = tf.keras.layers.Dense(len(SKIN_UNDERTONE_LABELS), activation='softmax', name="skin_undertone")(x)

        # Build Model with Multiple Outputs
        model = tf.keras.Model(inputs=base_model.input, 
                              outputs=[skin_tone_output, skin_type_output, skin_concern_output, 
                                      skin_texture_output, skin_undertone_output])

    return model  # Always return the same instance

# Load the model once to avoid reloading issues
model = load_model()

# Add this import at the top
import streamlit as st

# Modify the analyze_skin function (around line 90)
def analyze_skin(image_path, force_refresh=True):
    """Analyzes skin tone, type, texture, concerns, and undertone from an image file.

    Args:
        image_path (str): Path to the image file.
        force_refresh (bool): If True, reloads the model for fresh analysis.

    Returns:
        tuple: (skin_tone, skin_type, skin_concern, skin_texture, skin_undertone)
    """
    global model  # Ensure we use the loaded model

    if not image_path or not os.path.exists(image_path):
        raise ValueError("Invalid image path. Please provide a valid image file.")

    try:
        # Get current model state ID from session state or create it
        current_state_id = st.session_state.get('model_state_id', 0)
        
        # Store the last model state ID we used
        if 'last_model_state_id' not in st.session_state:
            st.session_state.last_model_state_id = -1
        
        # Check if we need to reload the model based on state change
        model_state_changed = current_state_id != st.session_state.last_model_state_id
        
        # Reload Model if Forced Refresh or State Changed
        if force_refresh or model_state_changed:
            print(f"DEBUG: Forcing model reload for fresh analysis... State ID: {current_state_id}")
            # Clear TensorFlow session to release previous model resources
            tf.keras.backend.clear_session()
            # Set model to None to force a complete reload
            global model
            model = None
            # Reload the model
            model = load_model()
            # Update the last model state ID
            st.session_state.last_model_state_id = current_state_id

        # Load and preprocess image
        img = Image.open(image_path).convert("RGB")
        
        # Apply image enhancement techniques
        img = tf.image.adjust_contrast(np.array(img), 1.2)  # Slightly increase contrast
        img = tf.image.adjust_brightness(img, 0.1)  # Slightly increase brightness
        
        # Resize with better quality
        img = tf.image.resize(img, (224, 224), method=tf.image.ResizeMethod.BICUBIC)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Disable TensorFlow caching for this prediction
        tf.config.experimental.set_synchronous_execution(True)
        
        # Ensure model is loaded before making predictions
        if model is None:
            raise ValueError("Skin analysis model is not loaded. Check model initialization.")

        # Make predictions with caching disabled
        with tf.device('/CPU:0'):  # Force CPU execution to avoid GPU caching
            predictions = model.predict(img_array, verbose=0)

        # Debugging: Print raw predictions
        print(f"DEBUG: Model Predictions -> {predictions}")

        # Extract skin attributes
        skin_tone = SKIN_TONE_LABELS[np.argmax(predictions[0])]
        skin_type = SKIN_TYPE_LABELS[np.argmax(predictions[1])]
        skin_concern = SKIN_CONCERN_LABELS[np.argmax(predictions[2])]
        skin_texture = SKIN_TEXTURE_LABELS[np.argmax(predictions[3])]
        
        # For backward compatibility, provide a default undertone if the model doesn't have it yet
        if len(predictions) >= 5:
            skin_undertone = SKIN_UNDERTONE_LABELS[np.argmax(predictions[4])]
        else:
            # Default to neutral if undertone prediction is not available
            skin_undertone = "Neutral"

        # Debugging: Print selected results
        print(f"DEBUG: Analysis Results -> Tone: {skin_tone}, Type: {skin_type}, Concern: {skin_concern}, Texture: {skin_texture}, Undertone: {skin_undertone}")

        return skin_tone, skin_type, skin_concern, skin_texture, skin_undertone

    except Exception as e:
        raise ValueError(f"ERROR: Skin analysis failed: {e}")
