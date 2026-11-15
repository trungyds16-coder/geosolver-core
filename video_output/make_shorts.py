import static_ffmpeg, subprocess, os
static_ffmpeg.add_paths()

out_dir = r"D:\AI DATA\STEM_APP\video_output"
body_mp4 = os.path.join(out_dir, "body.mp4")
shorts_mp4 = os.path.join(out_dir, "GeoSolver_2D_Shorts_9x16.mp4")

filter_str = (
    "[0:v]crop=1100:950:0:50,scale=1040:900[canvas];"
    "color=c=#0f172a:s=1080x1920:d=45[bg];"
    "[bg][canvas]overlay=(W-w)/2:460[v1];"
    "drawtext=text='GeoSolver 2D CAD':fontcolor=white:fontsize=56:x=(w-text_w)/2:y=280,"
    "drawtext=text='Nhan dien bat bien hinh hoc':fontcolor=#38bdf8:fontsize=34:x=(w-text_w)/2:y=360,"
    "drawtext=text='Trai nghiem tren Microsoft Store':fontcolor=#94a3b8:fontsize=36:x=(w-text_w)/2:y=1480[vout]"
)

# Use simple filter graph
cmd = [
    "ffmpeg", "-y",
    "-t", "45",
    "-i", body_mp4,
    "-i", os.path.join(out_dir, "morning_violin_guitar.wav"),
    "-filter_complex", (
        "[0:v]crop=1100:950:0:50,scale=1040:900[canvas];"
        "color=c=#0f172a:s=1080x1920:d=45[bg];"
        "[bg][canvas]overlay=(W-w)/2:460"
    ),
    "-map", "0:v",
    "-c:v", "libx264", "-crf", "22", "-preset", "fast",
    "-map", "1:a",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "45",
    shorts_mp4
]
# Let's fix filter_complex to map overlay output
cmd_correct = [
    "ffmpeg", "-y",
    "-t", "45",
    "-i", body_mp4,
    "-i", os.path.join(out_dir, "morning_violin_guitar.wav"),
    "-filter_complex", "[0:v]crop=1100:950:0:50,scale=1040:900[canvas];color=c=#0f172a:s=1080x1920:d=45[bg];[bg][canvas]overlay=(W-w)/2:460[vout]",
    "-map", "[vout]",
    "-map", "1:a",
    "-c:v", "libx264", "-crf", "22", "-preset", "fast",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "45",
    shorts_mp4
]
subprocess.run(cmd_correct, check=True)
print("Shorts 9:16 generated successfully:", shorts_mp4)
