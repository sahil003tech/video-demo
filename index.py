from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

UPLOAD_FOLDER = 'Videos'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/edit', methods=['POST'])
def edit_video():
    if 'video' not in request.files:
        return redirect(url_for('index'))

    file = request.files['video']
    output = request.form.to_dict()
    starttime = output['start']
    endtime = output['end']
    print(starttime, endtime)
    basedir = os.path.abspath(os.path.dirname(__file__))
    video_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], file.filename)
    file.save(video_path)

    action = request.form['action']

    if action == 'add_captions':
        print('enter in add caption')
        # Process the video and add captions
        processed_video = add_captions(video_path, basedir, file)
    elif action == 'resize_video':
        # Process the video and resize it
        processed_video = resize_video(video_path, starttime, endtime)
    else:
        return 'Invalid action'

    processed_video_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], 'edited_' + file.filename)
    processed_video.write_videofile(processed_video_path, codec="libx264")
    video_edit_path = processed_video_path

    # return redirect(url_for(processed_video_path))
    return send_file(processed_video_path, as_attachment=True)


def add_captions(video_path, basedir, file):
    video = VideoFileClip(video_path)
    print('start add caption')
    caption_text = "PodCast-Inc"
    caption = TextClip(caption_text, fontsize=50, color='gray')

    caption = caption.set_duration(video.duration)
    print('middle of caption')
    caption = caption.set_position(('center', 'bottom'))

    video_with_caption = CompositeVideoClip([video, caption])
    # Add captions to the video using MoviePy or any other video processing library
    print('end of caption')
    # Return the processed video clip
    return video_with_caption


def resize_video(video_path, starttime, endtime):
    start = float(starttime)
    end = float(endtime)
    video = VideoFileClip(video_path)
    resized_clip = video.subclip(start, end)  # Change the height as per your requirement

    # Resize the video using MoviePy or any other video processing library

    # Return the processed video clip
    return resized_clip


if __name__ == "__main__":
    app.run(debug=True, port=3000)
