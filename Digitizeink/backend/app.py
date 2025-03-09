from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Import CORS
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import cv2
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

# MongoDB setup
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["image_text_db"]
collection = db["extracted_texts"]

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask Image Upload API!"}), 200

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Process image for OCR
        image = cv2.imread(filepath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        denoised = cv2.fastNlMeansDenoising(thresh, h=10)
        processed_image = Image.fromarray(denoised)

        extracted_text = pytesseract.image_to_string(processed_image).strip()

        # Store data in MongoDB
        data = {
            "filename": filename,
            "filepath": filepath,
            "extracted_text": extracted_text
        }
        collection.insert_one(data)

        return jsonify({
            "message": "File uploaded and processed successfully",
            "filename": filename,
            "filepath": filepath,
            "extracted_text": extracted_text
        }), 200

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == "__main__":
    app.run(debug=True)
