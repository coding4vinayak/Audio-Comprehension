from flask import Flask, render_template, request, flash
import assemblyai as aai
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Replace with your AssemblyAI API key
ASSEMBLYAI_API_KEY = 'd9aab8b5403f473bb878038059b4dd3b'

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

    # Set AssemblyAI API key
    aai.settings.api_key = ASSEMBLYAI_API_KEY

    # Configuration for transcription (speaker_labels=True for speaker identification)
    config = aai.TranscriptionConfig(speaker_labels=True)

    # Initialize transcriber
    transcriber = aai.Transcriber()

    try:
        # Perform transcription
        transcript = transcriber.transcribe(file, config=config)

        # Prepare data for HTML rendering
        transcription_data = []
        for utterance in transcript.utterances:
            transcription_data.append({
                'speaker': f"Speaker {utterance.speaker}",
                'text': utterance.text
            })

        return render_template('upload.html', transcript=transcription_data)

    except Exception as e:
        flash(f'Transcription failed: {e}')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)