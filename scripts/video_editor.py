#!/usr/bin/env python3
"""
Video Editor Profesional para Redes Sociales - FFmpeg wrapper
Edita videos con calidad profesional para cualquier red social.
Capacidades: analisis, color grading, transiciones, subtitulos, logos, thumbnails.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ============================================================================
# PRESETS DE PLATAFORMAS
# ============================================================================

PLATFORM_PRESETS = {
    "tiktok": {
        "name": "TikTok", "width": 1080, "height": 1920, "aspect_ratio": "9:16",
        "max_duration": 600, "video_codec": "libx264", "profile": "high", "level": "4.2",
        "video_bitrate": "8M", "maxrate": "10M", "bufsize": "12M", "crf": "21",
        "audio_codec": "aac", "audio_bitrate": "128k", "audio_sample_rate": 44100,
        "fps": 30, "max_file_size_mb": 287,
    },
    "instagram_reels": {
        "name": "Instagram Reels", "width": 1080, "height": 1920, "aspect_ratio": "9:16",
        "max_duration": 180, "video_codec": "libx264", "profile": "main", "level": "4.0",
        "video_bitrate": "3500k", "maxrate": "3500k", "bufsize": "3500k", "crf": "23",
        "audio_codec": "aac", "audio_bitrate": "256k", "audio_sample_rate": 44100,
        "fps": 30, "max_file_size_mb": 4096,
    },
    "instagram_stories": {
        "name": "Instagram Stories", "width": 1080, "height": 1920, "aspect_ratio": "9:16",
        "max_duration": 60, "video_codec": "libx264", "profile": "main", "level": "4.0",
        "video_bitrate": "3500k", "maxrate": "3500k", "bufsize": "3500k", "crf": "23",
        "audio_codec": "aac", "audio_bitrate": "256k", "audio_sample_rate": 44100,
        "fps": 30, "max_file_size_mb": 4096,
    },
    "instagram_feed": {
        "name": "Instagram Feed (1:1)", "width": 1080, "height": 1080, "aspect_ratio": "1:1",
        "max_duration": 60, "video_codec": "libx264", "profile": "main", "level": "4.0",
        "video_bitrate": "3500k", "maxrate": "3500k", "bufsize": "3500k", "crf": "23",
        "audio_codec": "aac", "audio_bitrate": "256k", "audio_sample_rate": 44100,
        "fps": 30, "max_file_size_mb": 4096,
    },
    "youtube_shorts": {
        "name": "YouTube Shorts", "width": 1080, "height": 1920, "aspect_ratio": "9:16",
        "max_duration": 180, "video_codec": "libx264", "profile": "high", "level": "4.2",
        "video_bitrate": "10M", "maxrate": "12M", "bufsize": "15M", "crf": "18",
        "audio_codec": "aac", "audio_bitrate": "384k", "audio_sample_rate": 48000,
        "fps": 30, "max_file_size_mb": 256000,
    },
    "youtube_landscape": {
        "name": "YouTube (16:9)", "width": 1920, "height": 1080, "aspect_ratio": "16:9",
        "max_duration": 43200, "video_codec": "libx264", "profile": "high", "level": "4.2",
        "video_bitrate": "12M", "maxrate": "15M", "bufsize": "20M", "crf": "18",
        "audio_codec": "aac", "audio_bitrate": "384k", "audio_sample_rate": 48000,
        "fps": 30, "max_file_size_mb": 256000,
    },
    "twitter": {
        "name": "Twitter / X", "width": 1080, "height": 1920, "aspect_ratio": "9:16",
        "max_duration": 140, "video_codec": "libx264", "profile": "high", "level": "4.2",
        "video_bitrate": "5M", "maxrate": "8M", "bufsize": "10M", "crf": "23",
        "audio_codec": "aac", "audio_bitrate": "128k", "audio_sample_rate": 44100,
        "fps": 30, "max_file_size_mb": 512,
    },
    "facebook_reels": {
        "name": "Facebook Reels", "width": 1080, "height": 1920, "aspect_ratio": "9:16",
        "max_duration": 90, "video_codec": "libx264", "profile": "high", "level": "4.0",
        "video_bitrate": "6M", "maxrate": "8M", "bufsize": "10M", "crf": "21",
        "audio_codec": "aac", "audio_bitrate": "128k", "audio_sample_rate": 48000,
        "fps": 30, "max_file_size_mb": 4096,
    },
    "linkedin": {
        "name": "LinkedIn", "width": 1080, "height": 1920, "aspect_ratio": "9:16",
        "max_duration": 600, "video_codec": "libx264", "profile": "high", "level": "4.2",
        "video_bitrate": "8M", "maxrate": "10M", "bufsize": "12M", "crf": "21",
        "audio_codec": "aac", "audio_bitrate": "128k", "audio_sample_rate": 48000,
        "fps": 30, "max_file_size_mb": 5120,
    },
}

# ============================================================================
# COLOR GRADING PRESETS
# ============================================================================

COLOR_GRADES = {
    "none": "",
    "vivid": "eq=saturation=1.4:contrast=1.1:brightness=0.03",
    "warm": "colorbalance=rs=0.15:gs=0.05:bs=-0.1:rm=0.1:gm=0.02:bm=-0.05,eq=saturation=1.1",
    "cool": "colorbalance=rs=-0.1:gs=-0.05:bs=0.2:rh=-0.08:bh=0.15,eq=contrast=1.1",
    "vintage": "curves=preset=vintage,eq=saturation=0.8:contrast=1.15",
    "cinematic": "colorbalance=rs=0.15:gs=-0.05:bs=-0.15:rm=0.05:bm=0.1:bh=0.12,eq=saturation=0.9:contrast=1.2:brightness=-0.03",
    "bw": "hue=s=0,eq=contrast=1.2",
    "moody": "eq=brightness=-0.08:contrast=1.3:saturation=0.7,curves=preset=darker",
    "clean": "eq=contrast=1.05:saturation=1.05,unsharp=3:3:0.5",
    "high_energy": "eq=saturation=1.4:contrast=1.3:brightness=0.05,unsharp=5:5:1.0",
}

# ============================================================================
# UTILIDADES
# ============================================================================

def check_ffmpeg():
    for tool in ["ffmpeg", "ffprobe"]:
        if not shutil.which(tool):
            print(f"ERROR: {tool} no esta instalado.", file=sys.stderr)
            sys.exit(1)

def format_time(seconds):
    h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"

def parse_time(time_str):
    parts = [float(p) for p in time_str.strip().split(":")]
    if len(parts) == 3: return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2: return parts[0] * 60 + parts[1]
    return parts[0]

def eval_fps(fps_str):
    try:
        if "/" in fps_str:
            n, d = fps_str.split("/")
            return round(int(n) / int(d), 2)
        return float(fps_str)
    except (ValueError, ZeroDivisionError):
        return 0.0

def run_cmd(cmd, capture=True):
    r = subprocess.run(cmd, capture_output=capture, text=True)
    return r

# ============================================================================
# ANALISIS DE VIDEO
# ============================================================================

def probe_video(path):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", path]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(r.stdout)

def get_video_info(path):
    probe = probe_video(path)
    vs, aus = None, None
    for s in probe.get("streams", []):
        if s["codec_type"] == "video" and not vs: vs = s
        elif s["codec_type"] == "audio" and not aus: aus = s
    fmt = probe.get("format", {})
    dur = float(fmt.get("duration", 0))
    info = {
        "duration": dur, "duration_formatted": format_time(dur),
        "file_size_mb": round(int(fmt.get("size", 0)) / 1048576, 2),
        "format": fmt.get("format_name", "unknown"),
        "bitrate_kbps": int(fmt.get("bit_rate", 0)) // 1000,
    }
    if vs:
        info.update({
            "width": int(vs.get("width", 0)), "height": int(vs.get("height", 0)),
            "video_codec": vs.get("codec_name", "?"), "fps": eval_fps(vs.get("r_frame_rate", "0/1")),
            "pixel_format": vs.get("pix_fmt", "?"),
        })
    if aus:
        info.update({
            "audio_codec": aus.get("codec_name", "?"),
            "audio_sample_rate": int(aus.get("sample_rate", 0)),
            "audio_channels": int(aus.get("channels", 0)),
            "has_audio": True,
        })
    else:
        info["has_audio"] = False
    return info

def analyze_video(path):
    """Analisis profundo: escenas, silencios, brillo, loudness."""
    info = get_video_info(path)
    analysis = {"basic_info": info, "scenes": [], "silences": [], "brightness": "unknown", "loudness": {}}

    # Scene detection
    try:
        r = run_cmd(["ffmpeg", "-i", path, "-vf", "select=gt(scene\\,0.3),showinfo", "-f", "null", "-"])
        for line in r.stderr.split("\n"):
            if "pts_time:" in line:
                m = re.search(r"pts_time:(\d+\.?\d*)", line)
                if m: analysis["scenes"].append(round(float(m.group(1)), 2))
    except Exception:
        pass

    # Silence detection
    try:
        r = run_cmd(["ffmpeg", "-i", path, "-af", "silencedetect=noise=-30dB:d=0.5", "-f", "null", "-"])
        starts, ends = [], []
        for line in r.stderr.split("\n"):
            if "silence_start:" in line:
                m = re.search(r"silence_start:\s*(\d+\.?\d*)", line)
                if m: starts.append(float(m.group(1)))
            elif "silence_end:" in line:
                m = re.search(r"silence_end:\s*(\d+\.?\d*)", line)
                if m: ends.append(float(m.group(1)))
        for i in range(min(len(starts), len(ends))):
            analysis["silences"].append({"start": round(starts[i], 2), "end": round(ends[i], 2), "duration": round(ends[i] - starts[i], 2)})
    except Exception:
        pass

    # Brightness analysis (sample first 100 frames)
    try:
        r = run_cmd(["ffmpeg", "-i", path, "-vf", "signalstats,metadata=mode=print:key=lavfi.signalstats.YAVG", "-frames:v", "100", "-f", "null", "-"])
        vals = [float(m.group(1)) for m in re.finditer(r"lavfi\.signalstats\.YAVG=(\d+\.?\d*)", r.stderr)]
        if vals:
            avg = sum(vals) / len(vals)
            analysis["brightness_avg"] = round(avg, 1)
            if avg < 70: analysis["brightness"] = "oscuro"
            elif avg > 180: analysis["brightness"] = "brillante"
            else: analysis["brightness"] = "normal"
    except Exception:
        pass

    # Audio loudness
    try:
        r = run_cmd(["ffmpeg", "-i", path, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
        m = re.search(r'\{[^}]*"input_i"[^}]*\}', r.stderr, re.DOTALL)
        if m:
            loudness = json.loads(m.group(0))
            analysis["loudness"] = {
                "integrated": loudness.get("input_i", "?"),
                "true_peak": loudness.get("input_tp", "?"),
                "lra": loudness.get("input_lra", "?"),
            }
    except Exception:
        pass

    return analysis

# ============================================================================
# GENERACION DE THUMBNAILS
# ============================================================================

def generate_thumbnail(input_path, output_path=None, method="best"):
    if not output_path:
        output_path = str(Path(input_path).with_suffix(".thumb.jpg"))
    if method == "best":
        cmd = ["ffmpeg", "-y", "-i", input_path, "-vf", "thumbnail=300", "-frames:v", "1", "-vsync", "vfr", output_path]
    else:
        cmd = ["ffmpeg", "-y", "-i", input_path, "-vf", "select=gt(scene\\,0.4),scale=640:-1", "-vsync", "vfr", "-frames:v", "1", output_path]
    r = run_cmd(cmd)
    return output_path if r.returncode == 0 else None

# ============================================================================
# CONCATENACION CON TRANSICIONES
# ============================================================================

def concat_clips(clip_paths, output_path, transition="crossfade", transition_duration=0.5, fps=30):
    """Concatena clips con transiciones xfade."""
    if len(clip_paths) < 2:
        print("Se necesitan al menos 2 clips para concatenar.", file=sys.stderr)
        return False

    # Get durations
    durations = []
    for p in clip_paths:
        info = get_video_info(p)
        durations.append(info["duration"])

    n = len(clip_paths)
    inputs = []
    for p in clip_paths:
        inputs.extend(["-i", p])

    # Build filter complex
    parts = []

    # Normalize all video inputs
    for i in range(n):
        parts.append(f"[{i}:v]settb=AVTB,fps={fps}[v{i}]")

    # Chain xfade for video
    if n == 2:
        offset = durations[0] - transition_duration
        parts.append(f"[v0][v1]xfade=transition={transition}:duration={transition_duration}:offset={offset}[vout]")
        parts.append(f"[0:a][1:a]acrossfade=d={transition_duration}[aout]")
    else:
        prev_v = "v0"
        prev_a = "0:a"
        cumulative_offset = 0
        for i in range(1, n):
            cumulative_offset += durations[i-1] - transition_duration
            out_v = "vout" if i == n-1 else f"vt{i}"
            out_a = "aout" if i == n-1 else f"at{i}"
            parts.append(f"[{prev_v}][v{i}]xfade=transition={transition}:duration={transition_duration}:offset={cumulative_offset}[{out_v}]")
            parts.append(f"[{prev_a}][{i}:a]acrossfade=d={transition_duration}[{out_a}]")
            prev_v = out_v
            prev_a = out_a

    fc = ";".join(parts)

    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", output_path]

    print(f"Concatenando {n} clips con transicion '{transition}'...")
    r = run_cmd(cmd)
    if r.returncode != 0:
        print(f"Error concat:\n{r.stderr[-500:]}", file=sys.stderr)
        return False
    print(f"Concatenacion exitosa: {output_path}")
    return True

# ============================================================================
# EDICION PRINCIPAL
# ============================================================================

def build_ffmpeg_command(input_path, output_path, platform, config):
    preset = PLATFORM_PRESETS[platform]
    w, h = preset["width"], preset["height"]

    cmd = ["ffmpeg", "-y"]

    # Trim
    trim_start = config.get("trim_start")
    trim_end = config.get("trim_end")
    if trim_start is not None:
        cmd.extend(["-ss", str(trim_start)])
    cmd.extend(["-i", input_path])
    if trim_end is not None:
        cmd.extend(["-t", str(trim_end - (trim_start or 0))])

    # Extra inputs
    audio_path = config.get("audio_path")
    image_overlay = config.get("image_overlay")
    subtitle_file = config.get("subtitle_file")

    input_idx = 1
    audio_input_idx = None
    logo_input_idx = None

    if audio_path and not config.get("remove_audio", False):
        cmd.extend(["-i", audio_path])
        audio_input_idx = input_idx
        input_idx += 1

    if image_overlay and image_overlay.get("path"):
        cmd.extend(["-i", image_overlay["path"]])
        logo_input_idx = input_idx
        input_idx += 1

    # Build video filter chain
    vf = []
    speed = config.get("speed", 1.0)
    if speed != 1.0:
        vf.append(f"setpts={1.0/speed}*PTS")

    # Color adjustments
    brightness = config.get("brightness", 0.0)
    contrast = config.get("contrast", 1.0)
    saturation = config.get("saturation", 1.0)
    gamma = config.get("gamma", 1.0)
    eq_parts = []
    if brightness != 0.0: eq_parts.append(f"brightness={brightness}")
    if contrast != 1.0: eq_parts.append(f"contrast={contrast}")
    if saturation != 1.0: eq_parts.append(f"saturation={saturation}")
    if gamma != 1.0: eq_parts.append(f"gamma={gamma}")
    if eq_parts:
        vf.append(f"eq={':'.join(eq_parts)}")

    # Color grading preset
    grade = config.get("color_grade", "none")
    if grade in COLOR_GRADES and COLOR_GRADES[grade]:
        vf.append(COLOR_GRADES[grade])

    # Aspect ratio handling
    aspect_mode = config.get("aspect_mode", "letterbox")
    if aspect_mode == "blur_background" and preset["height"] > preset["width"]:
        # Blur background for vertical from horizontal
        vf.append(f"split[original][bg];"
                   f"[bg]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},boxblur=25[blurred];"
                   f"[original]scale={w}:{h}:force_original_aspect_ratio=decrease[fg];"
                   f"[blurred][fg]overlay=(W-w)/2:(H-h)/2")
    elif aspect_mode == "crop":
        vf.append(f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}")
    else:  # letterbox
        vf.append(f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black,setsar=1")

    # Subtitles
    if subtitle_file:
        esc = subtitle_file.replace("'", "\\'").replace(":", "\\:")
        vf.append(f"subtitles='{esc}':force_style='FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2'")

    # Text overlays
    for ov in config.get("text_overlays", []):
        text = ov.get("text", "").replace("'", "\\'").replace(":", "\\:")
        pos_map = {"arriba": "50", "top": "50", "centro": "(h-th)/2", "center": "(h-th)/2",
                   "abajo": "h-th-50", "bottom": "h-th-50"}
        y = pos_map.get(ov.get("position", "bottom"), ov.get("y", "h-th-50"))
        x = ov.get("x", "(w-text_w)/2")
        fs = ov.get("fontsize", 56)
        fc = ov.get("fontcolor", "white")
        dt = f"drawtext=text='{text}':fontsize={fs}:fontcolor={fc}:x={x}:y={y}"
        if ov.get("box", True):
            bc = ov.get("boxcolor", "black@0.6")
            dt += f":box=1:boxcolor={bc}:boxborderw={ov.get('borderw', 8)}"
        sf, su = ov.get("show_from"), ov.get("show_until")
        if sf is not None and su is not None:
            dt += f":enable='between(t,{sf},{su})'"
        elif sf is not None:
            dt += f":enable='gte(t,{sf})'"
        elif su is not None:
            dt += f":enable='lte(t,{su})'"
        vf.append(dt)

    # Vignette
    if config.get("vignette", False):
        vf.append("vignette=PI/4")

    # Fade in/out
    fade_in = config.get("fade_in", 0.0)
    fade_out = config.get("fade_out", 0.0)
    if fade_in > 0:
        vf.append(f"fade=t=in:st=0:d={fade_in}")
    if fade_out > 0:
        info = get_video_info(input_path)
        dur = info["duration"]
        if trim_end and trim_start: dur = (trim_end - trim_start) / speed
        elif trim_end: dur = trim_end / speed
        vf.append(f"fade=t=out:st={max(0, dur - fade_out)}:d={fade_out}")

    vf.append(f"fps={preset['fps']}")

    # Handle complex filter graph for logo overlay
    if logo_input_idx is not None:
        ov_cfg = image_overlay
        scale = ov_cfg.get("scale", 0.15)
        opacity = ov_cfg.get("opacity", 0.7)
        pos = ov_cfg.get("position", "top_right")
        pos_map = {
            "top_right": "W-w-20:20", "top_left": "20:20",
            "bottom_right": "W-w-20:H-h-20", "bottom_left": "20:H-h-20",
            "center": "(W-w)/2:(H-h)/2",
        }
        ov_pos = pos_map.get(pos, "W-w-20:20")

        vf_str = ",".join(vf)
        fc = (f"[0:v]{vf_str}[base];"
              f"[{logo_input_idx}:v]scale=iw*{scale}:-1,format=rgba,colorchannelmixer=aa={opacity}[logo];"
              f"[base][logo]overlay={ov_pos}")

        cmd.extend(["-filter_complex", fc])
    else:
        cmd.extend(["-vf", ",".join(vf)])

    # Video codec
    cmd.extend(["-c:v", preset["video_codec"], "-profile:v", preset["profile"],
                "-level:v", preset["level"], "-preset", "slow", "-crf", preset["crf"],
                "-b:v", preset["video_bitrate"], "-maxrate", preset["maxrate"],
                "-bufsize", preset["bufsize"], "-pix_fmt", "yuv420p"])

    # Audio
    if config.get("remove_audio", False):
        cmd.append("-an")
    else:
        af = []
        if speed != 1.0:
            # Chain atempo for values outside 0.5-2.0
            s = speed
            while s > 2.0:
                af.append("atempo=2.0")
                s /= 2.0
            while s < 0.5:
                af.append("atempo=0.5")
                s *= 2.0
            if 0.5 <= s <= 2.0:
                af.append(f"atempo={s}")

        orig_vol = config.get("original_audio_volume", 1.0)
        if orig_vol != 1.0:
            af.append(f"volume={orig_vol}")

        if config.get("normalize_audio", False):
            af.append("loudnorm=I=-14:TP=-1.5:LRA=11")

        if fade_in > 0:
            af.append(f"afade=t=in:d={fade_in}")
        if fade_out > 0:
            info = get_video_info(input_path)
            dur = info["duration"]
            if trim_end and trim_start: dur = (trim_end - trim_start) / speed
            af.append(f"afade=t=out:st={max(0, dur - fade_out)}:d={fade_out}")

        if audio_input_idx is not None:
            avol = config.get("audio_volume", 0.3)
            cmd.extend(["-filter_complex",
                f"[0:a]{','.join(af) if af else 'anull'}[orig];[{audio_input_idx}:a]volume={avol}[music];[orig][music]amix=inputs=2:duration=first:dropout_transition=3[aout]",
                "-map", "0:v", "-map", "[aout]"])
        elif af:
            cmd.extend(["-af", ",".join(af)])

        cmd.extend(["-c:a", preset["audio_codec"], "-b:a", preset["audio_bitrate"],
                    "-ar", str(preset["audio_sample_rate"]), "-ac", "2"])

    # Metadata & container
    if config.get("strip_metadata", True):
        cmd.extend(["-map_metadata", "-1"])
    cmd.extend(["-movflags", "+faststart", "-f", "mp4", output_path])
    return cmd

def edit_video(config):
    """Edita video segun configuracion."""
    input_path = config["input"]
    platforms = config["platforms"]
    output_dir = config.get("output_dir", os.path.dirname(input_path) or ".")
    os.makedirs(output_dir, exist_ok=True)
    name = Path(input_path).stem
    results = {}

    for platform in platforms:
        if platform not in PLATFORM_PRESETS:
            print(f"Plataforma '{platform}' no reconocida.", file=sys.stderr)
            continue
        preset = PLATFORM_PRESETS[platform]
        out = os.path.join(output_dir, f"{name}_{platform}.mp4")
        cmd = build_ffmpeg_command(input_path, out, platform, config)

        print(f"\n[{preset['name']}] Procesando...")
        r = run_cmd(cmd)
        success = r.returncode == 0
        if not success:
            print(f"ERROR:\n{r.stderr[-500:]}", file=sys.stderr)
        results[platform] = {"success": success, "output": out if success else None}

        if success:
            oi = get_video_info(out)
            results[platform]["output_info"] = {
                "size_mb": oi["file_size_mb"], "duration": oi["duration_formatted"],
                "resolution": f"{oi.get('width','?')}x{oi.get('height','?')}",
            }
            # Thumbnail
            if config.get("generate_thumbnail", False):
                thumb = os.path.join(output_dir, f"{name}_{platform}_thumb.jpg")
                generate_thumbnail(out, thumb)
                results[platform]["thumbnail"] = thumb
            print(f"[{preset['name']}] OK -> {out}")

    return results

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Editor de video profesional para redes sociales")
    sub = parser.add_subparsers(dest="command")

    p_info = sub.add_parser("info", help="Info del video")
    p_info.add_argument("input")

    p_analyze = sub.add_parser("analyze", help="Analisis profundo del video")
    p_analyze.add_argument("input")

    sub.add_parser("platforms", help="Listar plataformas")

    p_thumb = sub.add_parser("thumbnail", help="Generar thumbnail")
    p_thumb.add_argument("input")
    p_thumb.add_argument("--output", default=None)

    p_concat = sub.add_parser("concat", help="Concatenar clips con transiciones")
    p_concat.add_argument("clips", nargs="+")
    p_concat.add_argument("--output", required=True)
    p_concat.add_argument("--transition", default="crossfade")
    p_concat.add_argument("--duration", type=float, default=0.5)

    p_edit = sub.add_parser("edit", help="Editar video")
    p_edit.add_argument("--config", required=True)

    args = parser.parse_args()
    check_ffmpeg()

    if args.command == "info":
        print(json.dumps(get_video_info(args.input), indent=2, ensure_ascii=False))

    elif args.command == "analyze":
        print(json.dumps(analyze_video(args.input), indent=2, ensure_ascii=False))

    elif args.command == "platforms":
        for k, p in PLATFORM_PRESETS.items():
            print(f"  {k:25s} {p['name']:25s} {p['width']}x{p['height']}  max {format_time(p['max_duration'])}")

    elif args.command == "thumbnail":
        r = generate_thumbnail(args.input, args.output)
        print(f"Thumbnail: {r}" if r else "Error generando thumbnail")

    elif args.command == "concat":
        concat_clips(args.clips, args.output, args.transition, args.duration)

    elif args.command == "edit":
        with open(args.config) as f:
            config = json.load(f)
        results = edit_video(config)
        print("\n" + "=" * 60)
        print("RESULTADOS:")
        print("=" * 60)
        for plat, res in results.items():
            status = "OK" if res["success"] else "ERROR"
            name = PLATFORM_PRESETS.get(plat, {}).get("name", plat)
            print(f"  [{status}] {name}")
            if res.get("output_info"):
                oi = res["output_info"]
                print(f"         -> {res['output']}")
                print(f"         {oi['size_mb']}MB | {oi['duration']} | {oi['resolution']}")
            if res.get("thumbnail"):
                print(f"         Thumbnail: {res['thumbnail']}")
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
