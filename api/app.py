import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Vercel Blob Storage information
STORE_URL = "https://p3rgufsgjts1ytbg.public.blob.vercel-storage.com"
STORE_ID = "store_P3RgufsGJTS1YTbg"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"msg": "No file uploaded."})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No file selected."})

    if file:
        filename = file.filename
        # Define the blob URL to upload to
        upload_url = f"{STORE_URL}/{filename}"

        # Upload the file directly to Vercel Blob Storage
        response = requests.put(upload_url, data=file)

        if response.status_code == 200:
            # Successfully uploaded to Blob Storage
            uploaded_url = f"{STORE_URL}/{filename}"
            print(f"File uploaded to: {uploaded_url}")

            # Process the uploaded file (e.g., prediction logic)
            # Preprocess the audio and call your prediction functions
            preprocessed_audio = preprocess_audio(file)  # Adjust function to handle in-memory file
            res1, res2, res3, res4 = predict_alzheimer(preprocessed_audio)

            # Return prediction results
            return jsonify({
                "res3": res3,
                "res4": str(res4),
                "file_url": uploaded_url  # Return the Blob URL for reference
            })
        else:
            return jsonify({"msg": "Failed to upload file to Blob Storage."}), 500

if __name__ == "__main__":
    app.run(debug=True)
