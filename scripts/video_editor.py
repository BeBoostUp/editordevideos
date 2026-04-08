#!/usr/bin/env python3
"""
Video Editor for Social Media - FFmpeg wrapper
Edita videos para publicar en cualquier red social.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ============================================================================
# PRESETS DE PLATAFORMAS
# ============================================================================

PLATFORM_PRESETS = {
    "tiktok": {
        "name": "TikTok",
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "max_duration": 600,
        "video_codec": "libx264",
        "profile": "high",
        "level": "4.2",
        "video_bitrate": "8M",
        "maxrate": "10M",
        "bufsize": "12M",
        "crf": "21",
        "audio_codec": "aac",
        "audio_bitrate": "128k",
        "audio_sample_rate": 44100,
        "fps": 30,
        "max_file_size_mb": 287,
    },
    "instagram_reels": {
        "name": "Instagram Reels",
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "max_duration": 180,
        "video_codec": "libx264",
        "profile": "main",
        "level": "4.0",
        "video_bitrate": "3500k",
        "maxrate": "3500k",
        "bufsize": "3500k",
        "crf": "23",
        "audio_codec": "aac",
        "audio_bitrate": "256k",
        "audio_sample_rate": 44100,
        "fps": 30,
        "max_file_size_mb": 4096,
    },
    "instagram_stories": {
        "name": "Instagram Stories",
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "max_duration": 60,
        "video_codec": "libx264",
        "profile": "main",
        "level": "4.0",
        "video_bitrate": "3500k",
        "maxrate": "3500k",
        "bufsize": "3500k",
        "crf": "23",
        "audio_codec": "aac",
        "audio_bitrate": "256k",
        "audio_sample_rate": 44100,
        "fps": 30,
        "max_file_size_mb": 4096,
    },
    "instagram_feed": {
        "name": "Instagram Feed (Cuadrado)",
        "width": 1080,
        "height": 1080,
        "aspect_ratio": "1:1",
        "max_duration": 60,
        "video_codec": "libx264",
        "profile": "main",
        "level": "4.0",
        "video_bitrate": "3500k",
        "maxrate": "3500k",
        "bufsize": "3500k",
        "crf": "23",
        "audio_codec": "aac",
        "audio_bitrate": "256k",
        "audio_sample_rate": 44100,
        "fps": 30,
        "max_file_size_mb": 4096,
    },
    "youtube_shorts": {
        "name": "YouTube Shorts",
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "max_duration": 180,
        "video_codec": "libx264",
        "profile": "high",
        "level": "4.2",
        "video_bitrate": "10M",
        "maxrate": "12M",
        "bufsize": "15M",
        "crf": "18",
        "audio_codec": "aac",
        "audio_bitrate": "384k",
        "audio_sample_rate": 48000,
        "fps": 30,
        "max_file_size_mb": 256000,
    },
    "twitter": {
        "name": "Twitter / X",
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "max_duration": 140,
        "video_codec": "libx264",
        "profile": "high",
        "level": "4.2",
        "video_bitrate": "5M",
        "maxrate": "8M",
        "bufsize": "10M",
        "crf": "23",
        "audio_codec": "aac",
        "audio_bitrate": "128k",
        "audio_sample_rate": 44100,
        "fps": 30,
        "max_file_size_mb": 512,
    },
    "facebook_reels": {
        "name": "Facebook Reels",
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "max_duration": 90,
        "video_codec": "libx264",
        "profile": "high",
        "level": "4.0",
        "video_bitrate": "6M",
        "maxrate": "8M",
        "bufsize": "10M",
        "crf": "21",
        "audio_codec": "aac",
        "audio_bitrate": "128k",
        "audio_sample_rate": 48000,
        "fps": 30,
        "max_file_size_mb": 4096,
    },
    "linkedin": {
        "name": "LinkedIn",
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "max_duration": 600,
        "video_codec": "libx264",
        "profile": "high",
        "level": "4.2",
        "video_bitrate": "8M",
        "maxrate": "10M",
        "bufsize": "12M",
        "crf": "21",
        "audio_codec": "aac",
        "audio_bitrate": "128k",
        "audio_sample_rate": 48000,
        "fps": 30,
        "max_file_size_mb": 5120,
    },
    "youtube_landscape": {
        "name": "YouTube (Horizontal)",
        "width": 1920,
        "height": 1080,
        "aspect_ratio": "16:9",
        "max_duration": 43200,
        "video_codec": "libx264",
        "profile": "high",
        "level": "4.2",
        "video_bitrate": "12M",
        "maxrate": "15M",
        "bufsize": "20M",
        "crf": "18",
        "audio_codec": "aac",
        "audio_bitrate": "384k",
        "audio_sample_rate": 48000,
        "fps": 30,
        "max_file_size_mb": 256000,
    },
}


# ============================================================================
# FUNCIONES DE ANALISIS
# ============================================================================


def check_ffmpeg():
    """Verifica que FFmpeg y FFprobe esten instalados."""
    for tool in ["ffmpeg", "ffprobe"]:
        if not shutil.which(tool):
            print(f"ERROR: {tool} no esta instalado.", file=sys.stderr)
            print("Instala con: apt-get install ffmpeg (Linux) o brew install ffmpeg (Mac)", file=sys.stderr)
            sys.exit(1)


def probe_video(input_path: str) -> dict:
    """Obtiene informacion detallada del video usando ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        input_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def get_video_info(input_path: str) -> dict:
    """Extrae informacion util del video."""
    probe = probe_video(input_path)

    video_stream = None
    audio_stream = None
    for stream in probe.get("streams", []):
        if stream["codec_type"] == "video" and video_stream is None:
            video_stream = stream
        elif stream["codec_type"] == "audio" and audio_stream is None:
            audio_stream = stream

    fmt = probe.get("format", {})
    duration = float(fmt.get("duration", 0))
    file_size_mb = int(fmt.get("size", 0)) / (1024 * 1024)

    info = {
        "duration": duration,
        "duration_formatted": format_time(duration),
        "file_size_mb": round(file_size_mb, 2),
        "format": fmt.get("format_name", "unknown"),
        "bitrate": int(fmt.get("bit_rate", 0)) // 1000,
    }

    if video_stream:
        info.update({
            "width": int(video_stream.get("width", 0)),
            "height": int(video_stream.get("height", 0)),
            "video_codec": video_stream.get("codec_name", "unknown"),
            "fps": eval_fps(video_stream.get("r_frame_rate", "0/1")),
            "pixel_format": video_stream.get("pix_fmt", "unknown"),
        })

    if audio_stream:
        info.update({
            "audio_codec": audio_stream.get("codec_name", "unknown"),
            "audio_sample_rate": int(audio_stream.get("sample_rate", 0)),
            "audio_channels": int(audio_stream.get("channels", 0)),
        })
    else:
        info["has_audio"] = False

    return info


def eval_fps(fps_str: str) -> float:
    """Evalua un string de FPS como '30000/1001' -> 29.97."""
    try:
        if "/" in fps_str:
            num, den = fps_str.split("/")
            return round(int(num) / int(den), 2)
        return float(fps_str)
    except (ValueError, ZeroDivisionError):
        return 0.0


def format_time(seconds: float) -> str:
    """Formatea segundos a HH:MM:SS."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def parse_time(time_str: str) -> float:
    """Convierte HH:MM:SS o MM:SS o SS a segundos."""
    parts = time_str.strip().split(":")
    parts = [float(p) for p in parts]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0]


# ============================================================================
# FUNCIONES DE EDICION
# ============================================================================


def build_ffmpeg_command(
    input_path: str,
    output_path: str,
    platform: str,
    trim_start: float = None,
    trim_end: float = None,
    speed: float = 1.0,
    text_overlays: list = None,
    audio_path: str = None,
    audio_volume: float = 0.3,
    remove_audio: bool = False,
    brightness: float = 0.0,
    contrast: float = 1.0,
    saturation: float = 1.0,
    fade_in: float = 0.0,
    fade_out: float = 0.0,
    video_duration: float = 0.0,
) -> list:
    """Construye el comando FFmpeg completo."""
    preset = PLATFORM_PRESETS[platform]
    w = preset["width"]
    h = preset["height"]

    cmd = ["ffmpeg", "-y"]

    # Input con trim
    if trim_start is not None:
        cmd.extend(["-ss", str(trim_start)])
    cmd.extend(["-i", input_path])
    if trim_end is not None:
        duration = trim_end - (trim_start or 0)
        cmd.extend(["-t", str(duration)])

    # Audio externo
    if audio_path and not remove_audio:
        cmd.extend(["-i", audio_path])

    # Video filters
    vfilters = []

    # Velocidad
    if speed != 1.0:
        vfilters.append(f"setpts={1.0/speed}*PTS")

    # Color adjustments
    eq_parts = []
    if brightness != 0.0:
        eq_parts.append(f"brightness={brightness}")
    if contrast != 1.0:
        eq_parts.append(f"contrast={contrast}")
    if saturation != 1.0:
        eq_parts.append(f"saturation={saturation}")
    if eq_parts:
        vfilters.append(f"eq={':'.join(eq_parts)}")

    # Scale + pad para la plataforma
    vfilters.append(
        f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black,"
        f"setsar=1"
    )

    # Text overlays
    if text_overlays:
        for overlay in text_overlays:
            text = overlay.get("text", "").replace("'", "\\'").replace(":", "\\:")
            x = overlay.get("x", "(w-text_w)/2")
            y = overlay.get("y", "h-th-50")
            fontsize = overlay.get("fontsize", 48)
            fontcolor = overlay.get("fontcolor", "white")
            box = overlay.get("box", True)
            boxcolor = overlay.get("boxcolor", "black@0.6")
            borderw = overlay.get("borderw", 8)

            dt = f"drawtext=text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={x}:y={y}"
            if box:
                dt += f":box=1:boxcolor={boxcolor}:boxborderw={borderw}"

            # Show time control
            show_from = overlay.get("show_from")
            show_until = overlay.get("show_until")
            if show_from is not None and show_until is not None:
                dt += f":enable='between(t,{show_from},{show_until})'"
            elif show_from is not None:
                dt += f":enable='gte(t,{show_from})'"
            elif show_until is not None:
                dt += f":enable='lte(t,{show_until})'"

            vfilters.append(dt)

    # Fade in/out
    if fade_in > 0:
        vfilters.append(f"fade=t=in:st=0:d={fade_in}")
    if fade_out > 0 and video_duration > 0:
        fade_start = video_duration - fade_out
        if trim_end and trim_start:
            fade_start = (trim_end - trim_start) / speed - fade_out
        vfilters.append(f"fade=t=out:st={max(0, fade_start)}:d={fade_out}")

    # FPS
    vfilters.append(f"fps={preset['fps']}")

    cmd.extend(["-vf", ",".join(vfilters)])

    # Video codec settings
    cmd.extend([
        "-c:v", preset["video_codec"],
        "-profile:v", preset["profile"],
        "-level:v", preset["level"],
        "-preset", "slow",
        "-crf", preset["crf"],
        "-b:v", preset["video_bitrate"],
        "-maxrate", preset["maxrate"],
        "-bufsize", preset["bufsize"],
        "-pix_fmt", "yuv420p",
    ])

    # Audio
    if remove_audio:
        cmd.append("-an")
    else:
        afilters = []
        if speed != 1.0:
            afilters.append(f"atempo={speed}")

        if audio_path:
            # Mix original (muted) + external audio
            cmd.extend([
                "-filter_complex",
                f"[0:a]volume=0.0[orig];[1:a]volume={audio_volume}[music];[orig][music]amix=inputs=2:duration=shortest[aout]",
                "-map", "0:v",
                "-map", "[aout]",
            ])
        elif afilters:
            cmd.extend(["-af", ",".join(afilters)])

        cmd.extend([
            "-c:a", preset["audio_codec"],
            "-b:a", preset["audio_bitrate"],
            "-ar", str(preset["audio_sample_rate"]),
            "-ac", "2",
        ])

    # Container settings
    cmd.extend([
        "-movflags", "+faststart",
        "-f", "mp4",
        output_path,
    ])

    return cmd


def run_ffmpeg(cmd: list) -> bool:
    """Ejecuta un comando FFmpeg mostrando el progreso."""
    print(f"\nEjecutando: {' '.join(cmd[:6])}... -> {cmd[-1]}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR FFmpeg:\n{result.stderr[-500:]}", file=sys.stderr)
        return False
    print("Video generado exitosamente.")
    return True


def edit_video(config: dict) -> bool:
    """Edita un video segun la configuracion proporcionada."""
    input_path = config["input"]
    platforms = config["platforms"]
    output_dir = config.get("output_dir", os.path.dirname(input_path) or ".")

    os.makedirs(output_dir, exist_ok=True)
    input_name = Path(input_path).stem
    video_info = get_video_info(input_path)

    results = {}

    for platform in platforms:
        if platform not in PLATFORM_PRESETS:
            print(f"Plataforma '{platform}' no reconocida. Saltando.", file=sys.stderr)
            continue

        preset = PLATFORM_PRESETS[platform]
        output_path = os.path.join(output_dir, f"{input_name}_{platform}.mp4")

        # Check duration limit
        effective_duration = video_info["duration"]
        trim_start = config.get("trim_start")
        trim_end = config.get("trim_end")
        speed = config.get("speed", 1.0)

        if trim_start is not None and trim_end is not None:
            effective_duration = (trim_end - trim_start) / speed
        elif trim_end is not None:
            effective_duration = trim_end / speed

        if effective_duration > preset["max_duration"]:
            print(
                f"AVISO: Video ({format_time(effective_duration)}) excede el limite "
                f"de {preset['name']} ({format_time(preset['max_duration'])}). "
                f"Se recortara automaticamente."
            )
            if trim_start is None:
                trim_start = 0
            trim_end = (trim_start or 0) + preset["max_duration"] * speed

        cmd = build_ffmpeg_command(
            input_path=input_path,
            output_path=output_path,
            platform=platform,
            trim_start=trim_start,
            trim_end=trim_end,
            speed=speed,
            text_overlays=config.get("text_overlays"),
            audio_path=config.get("audio_path"),
            audio_volume=config.get("audio_volume", 0.3),
            remove_audio=config.get("remove_audio", False),
            brightness=config.get("brightness", 0.0),
            contrast=config.get("contrast", 1.0),
            saturation=config.get("saturation", 1.0),
            fade_in=config.get("fade_in", 0.0),
            fade_out=config.get("fade_out", 0.0),
            video_duration=video_info["duration"],
        )

        success = run_ffmpeg(cmd)
        results[platform] = {
            "success": success,
            "output": output_path if success else None,
        }

        if success:
            out_info = get_video_info(output_path)
            results[platform]["output_info"] = {
                "size_mb": out_info["file_size_mb"],
                "duration": out_info["duration_formatted"],
                "resolution": f"{out_info.get('width', '?')}x{out_info.get('height', '?')}",
            }

    return results


# ============================================================================
# CLI
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Editor de video para redes sociales"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # Comando: info
    info_parser = subparsers.add_parser("info", help="Mostrar informacion del video")
    info_parser.add_argument("input", help="Ruta al video")

    # Comando: platforms
    subparsers.add_parser("platforms", help="Listar plataformas disponibles")

    # Comando: edit
    edit_parser = subparsers.add_parser("edit", help="Editar video")
    edit_parser.add_argument("--config", required=True, help="Ruta al archivo JSON de configuracion")

    args = parser.parse_args()

    check_ffmpeg()

    if args.command == "info":
        info = get_video_info(args.input)
        print(json.dumps(info, indent=2, ensure_ascii=False))

    elif args.command == "platforms":
        for key, preset in PLATFORM_PRESETS.items():
            print(f"  {key:25s} {preset['name']:30s} {preset['width']}x{preset['height']}  max {format_time(preset['max_duration'])}")

    elif args.command == "edit":
        with open(args.config) as f:
            config = json.load(f)
        results = edit_video(config)
        print("\n" + "=" * 60)
        print("RESULTADOS:")
        print("=" * 60)
        for platform, result in results.items():
            status = "OK" if result["success"] else "ERROR"
            print(f"  [{status}] {PLATFORM_PRESETS[platform]['name']}")
            if result.get("output_info"):
                oi = result["output_info"]
                print(f"         Archivo: {result['output']}")
                print(f"         Tamano: {oi['size_mb']} MB | Duracion: {oi['duration']} | Resolucion: {oi['resolution']}")
        print(json.dumps(results, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
