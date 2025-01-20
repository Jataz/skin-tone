import tensorflow as tf
import numpy as np
from PIL import Image

# Skin tone categories
SKIN_TONE_LABELS = ["Fair", "Medium", "Dark"]

# Load MobileNetV2 and fine-tune
def load_model():
    base_model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False  # Freeze the base model

    # Add custom layers for skin tone classification
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(len(SKIN_TONE_LABELS), activation='softmax')  # 3 categories
    ])
    return model

# Load the model
model = load_model()

# Analyze skin tone
def analyze_skin(image_path):
    # Load and preprocess the image
    img = Image.open(image_path).convert("RGB").resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict using the model
    predictions = model.predict(img_array)
    skin_tone = SKIN_TONE_LABELS[np.argmax(predictions)]

    # Simplified texture and condition analysis
    texture = "Smooth" if np.mean(img_array) > 0.5 else "Rough"
    condition = "Dry" if np.std(img_array) < 0.1 else "Oily"

    return skin_tone, texture, condition
