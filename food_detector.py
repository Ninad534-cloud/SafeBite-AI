from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)

from tensorflow.keras.preprocessing import image
import numpy as np

model = MobileNetV2(weights="imagenet")


def detect_food(img_path):

    img = image.load_img(img_path, target_size=(224,224))

    x = image.img_to_array(img)

    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x)

    preds = model.predict(x)

    label = decode_predictions(preds, top=1)[0][0][1]

    label = label.lower()

    if "pizza" in label:
        return "Pizza"

    elif "burger" in label:
        return "Burger"

    else:
        return "Vada Pav"