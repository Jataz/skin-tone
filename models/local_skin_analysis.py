import tensorflow as tf
import numpy as np
import os
from PIL import Image

# Define Labels
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

# Initialize model variable globally
model = None  

def load_model():
    """Loads the model only once from a local file."""
    global model
    #model_path = "skin_tone_model.h5"
    model_path = os.path.join(os.path.dirname(__file__), "skin_tone_model.h5")

    if model is None:  # Load only if not already loaded
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ERROR: Model file '{model_path}' not found. Train and save the model first.")
        print(f"DEBUG: Loading model from '{model_path}'...")
        model = tf.keras.models.load_model(model_path)

    return model

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
            model = None  # Reset model to force reload
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
