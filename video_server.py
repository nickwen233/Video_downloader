from flask import Flask, request, jsonify
from flask_cors import CORS
import threading, yt_dlp, os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # allow requests from your Chrome extension

# Default download folder
DOWNLOAD_FOLDER = str(Path.home() / "Downloads")

def download_video(url, mode="video"):
    """
    Download a video or audio.
    mode: 'video' for full MP4, 'audio' for MP3
    """
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    # yt-dlp options
    if mode == "video":
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4'
        }
    elif mode == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    else:
        raise ValueError("Invalid mode. Use 'video' or 'audio'.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")

@app.route("/download", methods=["POST"])
def download_endpoint():
    """
    JSON input:
    {
        "url": "https://youtube.com/...",
        "mode": "video" or "audio"
    }
    """
    data = request.json or {}
    url = data.get("url")
    mode = data.get("mode", "video")

    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    threading.Thread(target=download_video, args=(url, mode), daemon=True).start()
    return jsonify({"status": "started", "mode": mode, "url": url})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

