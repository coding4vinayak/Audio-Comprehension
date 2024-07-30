from flask import Flask, render_template, request, flash
import assemblyai as aai

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Replace with your default AssemblyAI API key
DEFAULT_API_KEY = 'd9aab8b5403f473bb878038059b4dd3b'

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    # Check if API key is provided in the form
    user_api_key = request.form.get('api_key')

    transcript = transcribe_audio(file, user_api_key)
    
    if transcript:
        return render_template('upload.html', transcript=transcript)
    else:
        flash('Transcription failed')
        return redirect(request.url)

def transcribe_audio(file, api_key=None):
    # Set AssemblyAI API key
    if api_key:
        aai.settings.api_key = api_key
    else:
        aai.settings.api_key = DEFAULT_API_KEY

    # Initialize transcriber and transcribe audio file
    transcriber = aai.Transcriber()
    try:
        transcript = transcriber.transcribe(file)
        if transcript.status == aai.TranscriptStatus.completed:
            return transcript.text
        else:
            return f'Transcription status: {transcript.status}'
    except Exception as e:
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(debug=True)
