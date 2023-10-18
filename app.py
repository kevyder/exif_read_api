import os
from flask import Flask, request, jsonify
from helpers import allowed_file_extension, process_image

app = Flask(__name__)


@app.route("/exif", methods=["POST"])
def exif_data():
    if "image" not in request.files:
        response = jsonify({"message": "No file part in the request"})
        response.status_code = 400
        return response

    image = request.files["image"]
    image_name, image_extension = os.path.splitext(image.filename)

    if not image_name:
        response = jsonify({"message": "No file selected for uploading"})
        response.status_code = 400
        return response

    if allowed_file_extension(image_extension):
        exif_data = process_image(image)
        response = jsonify(exif_data)
        response.status_code = 201
        return response
    else:
        response = jsonify(
            {"message": "Allowed file types are tiff, jpeg, jpg, png, webp, heic"}
        )
        response.status_code = 400
        return response


if __name__ == "__main__":
    app.run()
