from flask import Flask, render_template, request, redirect, url_for
import openai
import os
import sys

app = Flask(__name__)

# Configure your OpenAI API key
try:
    openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
    sys.stderr.write("Please set the environment variable OPENAI_API_KEY with the value of your API key.\n")
    exit(1)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "audio_file" not in request.files:
            return "No file uploaded.", 400

        audio_file = request.files["audio_file"]

        if audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            transcript_text = transcript["text"]

            return render_template("transcription.html", transcript=transcript_text)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
