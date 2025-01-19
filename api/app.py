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
        # Set the path for temporary file saving
        file_path = os.path.join("uploads", filename)
        file.save(file_path)

        # Upload the file to Vercel Blob Storage
        upload_url = f"{STORE_URL}/{filename}"

        with open(file_path, 'rb') as f:
            response = requests.put(upload_url, data=f)

        if response.status_code == 200:
            # Successfully uploaded to Blob Storage
            uploaded_url = f"{STORE_URL}/{filename}"
            print(f"File uploaded to: {uploaded_url}")

            # Process the uploaded file (e.g., prediction logic)
            preprocessed_audio = preprocess_audio(file_path)
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
