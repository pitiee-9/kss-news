from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'school-video-news-secret-key'

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'}

# Data file to store videos
DATA_FILE = 'videos.json'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/thumbnails', exist_ok=True)

# Load videos from JSON file
def load_videos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Save videos to JSON file
def save_videos(videos):
    with open(DATA_FILE, 'w') as f:
        json.dump(videos, f, indent=4)

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize with some sample videos
def init_videos():
    videos = load_videos()
    if not videos:
        videos = [
            {"id": 1, "title": "School Opening Ceremony", "year": 2023, "added": "2023-08-15", 
             "filename": "sample1.mp4", "thumbnail": "sample1.jpg", "category": "Event"},
            {"id": 2, "title": "Science Fair Highlights", "year": 2023, "added": "2023-09-10",
             "filename": "sample2.mp4", "thumbnail": "sample2.jpg", "category": "Academic"}
        ]
        save_videos(videos)
    return videos

# Routes
@app.route('/')
def index():
    videos = load_videos()
    return render_template('index.html', videos=videos)

@app.route('/admin')
def admin():
    videos = load_videos()
    return render_template('admin.html', videos=videos)

@app.route('/add_video', methods=['POST'])
def add_video():
    try:
        # Check if the post request has the file part
        if 'video' not in request.files:
            return jsonify({'success': False, 'error': 'No video file provided'})
        
        video_file = request.files['video']
        title = request.form.get('title')
        year = request.form.get('year')
        category = request.form.get('category', 'General')
        
        if not title or not year:
            return jsonify({'success': False, 'error': 'Title and year are required'})
        
        if video_file.filename == '':
            return jsonify({'success': False, 'error': 'No video file selected'})
        
        if video_file and allowed_file(video_file.filename):
            # Generate unique filename
            filename = secure_filename(video_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            video_file.save(video_path)
            
            # Handle thumbnail
            thumbnail_file = request.files.get('thumbnail')
            thumbnail_filename = None
            
            if thumbnail_file and thumbnail_file.filename != '':
                thumb_filename = secure_filename(thumbnail_file.filename)
                thumbnail_filename = f"thumb_{uuid.uuid4().hex}_{thumb_filename}"
                thumbnail_path = os.path.join('static/thumbnails', thumbnail_filename)
                thumbnail_file.save(thumbnail_path)
            
            # Load existing videos
            videos = load_videos()
            
            # Create new video
            new_video = {
                'id': max([v['id'] for v in videos], default=0) + 1,
                'title': title,
                'year': int(year),
                'category': category,
                'added': datetime.now().strftime('%Y-%m-%d'),
                'filename': unique_filename,
                'thumbnail': thumbnail_filename
            }
            
            # Add to list and save
            videos.append(new_video)
            save_videos(videos)
            
            return jsonify({'success': True, 'video': new_video})
        else:
            return jsonify({'success': False, 'error': 'Invalid file type'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/delete_video/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    try:
        videos = load_videos()
        video_to_delete = next((v for v in videos if v['id'] == video_id), None)
        
        if video_to_delete:
            # Remove the video file
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_to_delete['filename'])
            if os.path.exists(video_path):
                os.remove(video_path)
            
            # Remove the thumbnail if exists
            if video_to_delete.get('thumbnail'):
                thumb_path = os.path.join('static/thumbnails', video_to_delete['thumbnail'])
                if os.path.exists(thumb_path):
                    os.remove(thumb_path)
            
            # Remove from list
            videos = [v for v in videos if v['id'] != video_id]
            save_videos(videos)
            
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Video not found'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_videos')
def get_videos():
    videos = load_videos()
    return jsonify(videos)

@app.route('/video/<filename>')
def serve_video(filename):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(video_path)

if __name__ == '__main__':
    init_videos()
    app.run(debug=True)