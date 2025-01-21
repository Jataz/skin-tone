import tensorflow as tf
import numpy as np
from PIL import Image

# Configure TensorFlow
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Load pre-trained model
def load_model():
    base_model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False  # Freeze the base model

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')  # 3 categories: Fair, Medium, Dark
    ])
    return model

model = load_model()
SKIN_TONE_LABELS = ["Fair", "Medium", "Dark"]

def analyze_skin(image_path):
    try:
        img = Image.open(image_path).convert("RGB").resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        skin_tone = SKIN_TONE_LABELS[np.argmax(predictions)]
        texture = "Smooth" if np.mean(img_array) > 0.5 else "Rough"
        conditiontype = "Dry" if np.std(img_array) < 0.1 else "Oily"

        return skin_tone, texture, conditiontype
    except Exception as e:
        raise ValueError(f"Error analyzing skin: {e}")
