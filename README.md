# Editor de Videos Profesional para Redes Sociales

Skill de Claude Code que convierte clips de video en contenido profesional listo para cualquier red social.

## Que hace

- Analiza tus videos (brillo, audio, escenas, silencios)
- Te guia con preguntas profesionales (marca, tono, ritmo, colores)
- Aplica color grading, textos, subtitulos, musica, transiciones
- Exporta optimizado para cada plataforma (TikTok, Instagram, YouTube, Twitter, etc.)

## Requisitos

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

Python 3.8+ (incluido en la mayoria de sistemas).

## Uso con Claude Code

```
/project:edit-video /ruta/al/video.mp4
```

Claude te guiara paso a paso.

## Uso desde terminal

```bash
# Info del video
python3 scripts/video_editor.py info video.mp4

# Analisis profundo (brillo, audio, escenas)
python3 scripts/video_editor.py analyze video.mp4

# Plataformas disponibles
python3 scripts/video_editor.py platforms

# Generar thumbnail
python3 scripts/video_editor.py thumbnail video.mp4

# Concatenar clips con transicion
python3 scripts/video_editor.py concat clip1.mp4 clip2.mp4 --output final.mp4 --transition crossfade

# Editar con configuracion JSON
python3 scripts/video_editor.py edit --config config.json
```

## Funcionalidades

- **Analisis**: deteccion de escenas, silencios, brillo, loudness (LUFS)
- **Color grading**: vivid, warm, cool, vintage, cinematic, bw, moody, clean, high_energy
- **Texto**: overlays con posicion, timing, colores corporativos, CTAs
- **Subtitulos**: burn-in desde archivo SRT
- **Logo/watermark**: con posicion, opacidad y escala configurables
- **Audio**: normalizacion loudness, musica de fondo, control de volumen
- **Transiciones**: crossfade, fade, wipe, slide, circle y 30+ opciones via xfade
- **Efectos**: vineta, blur background, fade in/out, cambio de velocidad
- **Multi-plataforma**: exporta simultaneamente para todas las redes sociales

## Ejemplo de config JSON

```json
{
  "input": "video.mp4",
  "platforms": ["tiktok", "instagram_reels"],
  "output_dir": "./output",
  "color_grade": "cinematic",
  "text_overlays": [{"text": "Sigueme!", "position": "bottom", "fontsize": 56}],
  "normalize_audio": true,
  "fade_in": 0.5,
  "fade_out": 0.5,
  "vignette": true,
  "generate_thumbnail": true
}
```

## Licencia

MIT
