from flask import Flask, render_template, request, flash, redirect
import assemblyai as aai
from openai import OpenAI

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Replace with your AssemblyAI API key
aai.settings.api_key = "d9aab8b5403f473bb878038059b4dd3b"

# Replace with your OpenAI API key
openai_client = OpenAI(
    api_key="6aec37dcb7fb4180b43df55a302fb07d",
    base_url="https://api.aimlapi.com",
)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Initialize transcriber
    transcriber = aai.Transcriber()

    try:
        # Perform transcription
        transcript = transcriber.transcribe(file)

        # Check if transcription was successful
        if transcript.status == aai.TranscriptStatus.error:
            flash(f'Transcription failed: {transcript.error}')
            return redirect(request.url)

        # Get the transcription text
        transcription_text = transcript.text

        # Summarize using the OpenAI client
        response = openai_client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant who knows everything.",
                },
                {
                    "role": "user",
                    "content": transcription_text,
                },
            ],
        )

        # Extract summarized text from OpenAI's response
        summary = response.choices[0].message.content

        return render_template('upload.html', transcription=transcription_text, summary=summary)

    except Exception as e:
        flash(f'Error: {e}')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
