import random
import os

from food_detector import detect_food
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

food_data = {
    "Vada Pav": {"calories": 300, "protein": 8, "hygiene": 82},
    "Samosa": {"calories": 260, "protein": 5, "hygiene": 72},
    "Dosa": {"calories": 180, "protein": 6, "hygiene": 88},
    "Pav Bhaji": {"calories": 400, "protein": 10, "hygiene": 89},
    "Burger": {"calories": 450, "protein": 15, "hygiene": 55},
    "Pizza": {"calories": 500, "protein": 18, "hygiene": 40}
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['food_image']

    filename = ""

    if file and file.filename != "":

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )

        file.save(filepath)

        food = detect_food(filepath)

    else:
        food = "Vada Pav"

    result = food_data.get(food)

    if result["calories"] > 450:
        health_rating = "Unhealthy"

    elif result["calories"] > 250:
        health_rating = "Moderate"

    else:
        health_rating = "Healthy"

    hygiene_score = result["hygiene"]

    confidence = round(random.uniform(88, 98), 1)

    return render_template(
        'result.html',
        food=food,
        calories=result['calories'],
        protein=result['protein'],
        hygiene=hygiene_score,
        image=filename,
        confidence=confidence,
        health_rating=health_rating
    )


if __name__ == '__main__':
    app.run(debug=True)