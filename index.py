from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import subprocess
import whisper

from whisper.utils import WriteVTT
from whisper.utils import write_vtt

#
# import speech_recognition as sr

model = whisper.load_model("base.en")

UPLOAD_FOLDER = 'Videos'
output_dir = 'content'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['output_dir'] = output_dir


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def edit_video():
    global processed_video
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
        # # Process the video and add captions
        # processed_video = add_captions(video_path)
        # print('************************', processed_video)
    elif action == 'resize_video':
        # Process the video and resize it
        processed_video = resize_video(video_path, starttime, endtime)
    else:
        return 'Invalid action'

    processed_video_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], 'edited_' + file.filename)
    processed_video.write_videofile(processed_video_path, codec="libx264")
    video_edit_path = processed_video_path

    # return redirect(url_for(processed_video_path))
    return send_file(video_edit_path, as_attachment=True)


# def video2mp3(video_path, output_ext="mp3"):
#     filename, ext = os.path.splitext(video_path)
#     subprocess.call(["ffmpeg", "-y", "-i", video_path, f"{filename}.{output_ext}"],
#                     stdout=subprocess.DEVNULL,
#                     stderr=subprocess.STDOUT)
#     return f"{filename}.{output_ext}"
#
#
# #
#
# def add_captions(video_path):
#     # result = model.transcribe(video_path)
#     # print(result["text"])
#
#     audio_file = video2mp3(video_path)
#
#     options = dict(beam_size=5, best_of=5)
#     translate_options = dict(task="translate", **options)
#     result = model.transcribe(audio_file, **translate_options)
#     print('=========================', result["segments"])
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     audio_path = audio_file.split(".")[0]
#     print(audio_path)
#     vtt_path = os.path.join(audio_path + ".vtt")
#
#     with open(os.path.join(audio_path + ".vtt"), 'w', encoding='utf-8') as vtt:
#         vtt_writer = WriteVTT(vtt_path)
#         vtt_writer.write_result(result['segments'], file=vtt, options={
#             "language": "en",
#             "cue_format": "start-end",
#             "max_line_width": "None",
#             "max_line_count":"None",
#             "highlight_words": "false"
#         })
#     #     write_vtt(result['segments'], file=vtt)
#     #     print('vtt file written successfully', os.path.abspath(vtt_path))
#     subtitle_path = os.path.join(audio_path + ".vtt")
#     subtitle = r"C:\Users\HP\PycharmProjects\video-demo\Videos\input.vtt"
#     print("+++++++++++++++++++", subtitle)
#     output_video = "_subtitled.mp4"
#
#     os.system(f"ffmpeg -i {video_path} -i {subtitle} -c copy -c:s mov_text -metadata:s:s:0 language=en {output_video}")
#
#     return output_video


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
