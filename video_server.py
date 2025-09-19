from flask import Flask, request, jsonify
from flask_cors import CORS
import threading, yt_dlp, os, shutil
from pathlib import Path

app = Flask(__name__)
CORS(app)  # allow Chrome extension requests

def has_ffmpeg():
    """Check if ffmpeg is available in PATH."""
    return shutil.which("ffmpeg") is not None

def download_video(url, fmt=None, outdir=None):
    outdir = outdir or str(Path.home() / "Downloads")
    os.makedirs(outdir, exist_ok=True)

    # fallback if ffmpeg not found and user requested merging formats
    if fmt and "+" in fmt and not has_ffmpeg():
        print("[WARN] ffmpeg not found. Falling back to 'best' format.")
        fmt = "best"

    ydl_opts = {
        'outtmpl': os.path.join(outdir, '%(title)s.%(ext)s'),
        'format': fmt or "best",
        'ignoreerrors':True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"[ERROR] {e} — falling back to 'best'")
        # retry with 'best'
        ydl_opts['format'] = 'best'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

@app.route("/download", methods=["POST"])
def download_endpoint():
    data = request.json or {}
    url = data.get("url")
    fmt = data.get("format")
    outdir = data.get("outdir")

    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    threading.Thread(target=download_video, args=(url, fmt, outdir), daemon=True).start()
    return jsonify({"status": "started", "url": url, "format": fmt or "best"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

