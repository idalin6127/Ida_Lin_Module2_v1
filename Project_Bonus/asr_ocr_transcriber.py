import os
import whisper
import pytesseract
from pytesseract import image_to_string
from PIL import Image
import subprocess
import json
import glob
import shutil

# Step 0: Set Parameters
YOUTUBE_URLS = [
    "https://www.youtube.com/watch?v=g44qNS_nxfU",
    "https://www.youtube.com/watch?v=XxT9C61E2VE",
    "https://www.youtube.com/watch?v=PczCM3GwB4Q",
    "https://www.youtube.com/watch?v=kPuZ4BoaaUQ",
    "https://www.youtube.com/watch?v=Q-0os7z7aJ4",
    "https://www.youtube.com/watch?v=NJh-5mm-8g0",
    "https://www.youtube.com/watch?v=eRykFYdqjEo",
    "https://www.youtube.com/watch?v=rCBDcKD8UEg",
    "https://www.youtube.com/watch?v=PRCWrYjXH0Q",
    "https://www.youtube.com/watch?v=9It06-7Ol18",
]

os.makedirs("videos", exist_ok=True)
os.makedirs("frames", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

# Step 1: Download full video (video + audio)
def download_video(url):
    cmd = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",  # force output to mp4
        "-o", "videos/%(id)s.%(ext)s",
        url
    ]
    subprocess.run(cmd, check=True)

# Step 2: Transcribe audio using Whisper
def transcribe_video(video_path):
    model = whisper.load_model("medium")  # or 'large' if you have GPU and need better accuracy
    result = model.transcribe(video_path)
    return result

# Step 3: Extract frames from video
def extract_frames(video_path, every_n_sec=15):
    video_id = os.path.basename(video_path).split('.')[0]
    output_pattern = f"frames/{video_id}_%03d.jpg"
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps=1/{every_n_sec}",
        output_pattern,
        "-hide_banner",
        "-loglevel", "error"
    ]
    subprocess.run(cmd, check=True)

# Step 4: OCR on frames
def do_ocr_on_frames(video_id, interval_sec=15):
    text_blocks = []
    frame_files = sorted(f for f in os.listdir("frames") if f.startswith(video_id))
    for i, fname in enumerate(frame_files):
        image_path = os.path.join("frames", fname)
        img = Image.open(image_path)
        text = image_to_string(img)
        if text.strip():
            timestamp = i * interval_sec
            text_blocks.append({"timestamp": timestamp, "text": text.strip()})
    return text_blocks

# Step 5: Save .jsonl
def save_jsonl(transcript, ocr_texts, video_id):
    output_path = "talks_transcripts.jsonl"
    with open(output_path, "a", encoding="utf-8") as f:
        for segment in transcript['segments']:
            f.write(json.dumps({
                "video_id": video_id,
                "start": segment['start'],
                "end": segment['end'],
                "text": segment['text']
            }, ensure_ascii=False) + "\n")
        for ocr in ocr_texts:
            f.write(json.dumps({
                "video_id": video_id,
                "timestamp": ocr["timestamp"],
                "ocr_text": ocr["text"]
            }, ensure_ascii=False) + "\n")

# Step 6: Cleanup frames
def clear_frames():
    shutil.rmtree("frames")
    os.makedirs("frames", exist_ok=True)

# Main process
for url in YOUTUBE_URLS:
    video_id = url.split("v=")[-1]
    
    # Look for video files
    video_files = glob.glob(f"videos/{video_id}.*")
    video_file = next((f for f in video_files if f.endswith((".mp4", ".mkv", ".webm"))), None)

    if not video_file:
        print(f"Downloading video for {video_id} ...")
        try:
            download_video(url)
        except subprocess.CalledProcessError as e:
            print(f"Download failed for {video_id}: {e}")
            continue

        video_files = glob.glob(f"videos/{video_id}.*")
        video_file = next((f for f in video_files if f.endswith((".mp4", ".mkv", ".webm"))), None)

    if not video_file:
        print(f"Could not find valid video file for {video_id}, skipping.")
        continue

    print(f"Transcribing video: {video_file} ...")
    transcription = transcribe_video(video_file)

    print(f"Extracting frames from: {video_file} ...")
    extract_frames(video_file)

    print(f"Running OCR for {video_id} ...")
    ocr_results = do_ocr_on_frames(video_id)

    print(f"Saving transcription and OCR output for {video_id} ...")
    save_jsonl(transcription, ocr_results, video_id)

    print(f"Cleaning up temporary frames for {video_id} ...")
    clear_frames()

print("✅ All done!")
