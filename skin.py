import tensorflow as tf
import numpy as np
import os
from PIL import Image

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

# Load Pre-trained Model (Modified for Multi-Output)
# Initialize model variable globally
model = None  

def load_model():
    """Loads the model only once and keeps it in memory."""
    global model  # Ensure we use a single instance

    if model is None:  # Load only if not already loaded
        print("DEBUG: Loading the skin analysis model...")

        # Load Pretrained Base Model
        base_model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False  # Freeze the base model

        # Add Global Pooling Layer
        x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)

        # Define Outputs
        skin_tone_output = tf.keras.layers.Dense(len(SKIN_TONE_LABELS), activation='softmax', name="skin_tone")(x)
        skin_type_output = tf.keras.layers.Dense(len(SKIN_TYPE_LABELS), activation='softmax', name="skin_type")(x)
        skin_concern_output = tf.keras.layers.Dense(len(SKIN_CONCERN_LABELS), activation='softmax', name="skin_concern")(x)
        skin_texture_output = tf.keras.layers.Dense(len(SKIN_TEXTURE_LABELS), activation='softmax', name="skin_texture")(x)

        # Build Model with Multiple Outputs
        model = tf.keras.Model(inputs=base_model.input, outputs=[skin_tone_output, skin_type_output, skin_concern_output, skin_texture_output])

    return model  # Always return the same instance
# Load the model once to avoid reloading issues
model = load_model()

# Skin Analysis Function
def analyze_skin(image_path, force_refresh=False):
    """Analyzes skin tone, type, texture, and concerns from an image file.

    Args:
        image_path (str): Path to the image file.
        force_refresh (bool): If True, reloads the model for fresh analysis.

    Returns:
        tuple: (skin_tone, skin_type, skin_concern, skin_texture)
    """
    global model  # Ensure we use the loaded model

    if not image_path or not os.path.exists(image_path):
        raise ValueError("Invalid image path. Please provide a valid image file.")

    try:
        # Reload Model if Forced Refresh
        if force_refresh:
            print("DEBUG: Forcing model reload for fresh analysis...")
            model = load_model()

        # Load and preprocess image
        img = Image.open(image_path).convert("RGB").resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Ensure model is loaded before making predictions
        if model is None:
            raise ValueError("Skin analysis model is not loaded. Check model initialization.")

        # Make predictions
        predictions = model.predict(img_array)

        # Debugging: Print raw predictions
        print(f"DEBUG: Model Predictions -> {predictions}")

        # Extract skin attributes
        skin_tone = SKIN_TONE_LABELS[np.argmax(predictions[0])]
        skin_type = SKIN_TYPE_LABELS[np.argmax(predictions[1])]
        skin_concern = SKIN_CONCERN_LABELS[np.argmax(predictions[2])]
        skin_texture = SKIN_TEXTURE_LABELS[np.argmax(predictions[3])]

        # Debugging: Print selected results
        print(f"DEBUG: Analysis Results -> Tone: {skin_tone}, Type: {skin_type}, Concern: {skin_concern}, Texture: {skin_texture}")

        return skin_tone, skin_type, skin_concern, skin_texture

    except Exception as e:
        raise ValueError(f"ERROR: Skin analysis failed: {e}")
