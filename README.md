# Editor de Videos para Redes Sociales

Edita videos automaticamente para cualquier red social usando Claude Code + FFmpeg.

## Requisitos

- [FFmpeg](https://ffmpeg.org/) instalado en el sistema
- Python 3.8+
- Claude Code

### Instalar FFmpeg

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows (con Chocolatey)
choco install ffmpeg
```

## Uso

### Con Claude Code (recomendado)

Invoca la skill desde Claude Code:

```
/project:edit-video /ruta/al/video.mp4
```

Claude te guiara con preguntas interactivas para configurar la edicion.

### Desde la terminal

```bash
# Ver info del video
python3 scripts/video_editor.py info mi_video.mp4

# Ver plataformas disponibles
python3 scripts/video_editor.py platforms

# Editar con archivo de configuracion
python3 scripts/video_editor.py edit --config config.json
```

### Ejemplo de archivo de configuracion

```json
{
  "input": "mi_video.mp4",
  "platforms": ["tiktok", "instagram_reels", "youtube_shorts"],
  "output_dir": "./output",
  "trim_start": 5.0,
  "trim_end": 60.0,
  "speed": 1.0,
  "text_overlays": [
    {
      "text": "Sigueme!",
      "y": "h-th-50",
      "fontsize": 56,
      "fontcolor": "white",
      "box": true,
      "show_from": 3,
      "show_until": 8
    }
  ],
  "remove_audio": false,
  "brightness": 0.05,
  "contrast": 1.1,
  "saturation": 1.2,
  "fade_in": 0.5,
  "fade_out": 0.5
}
```

## Plataformas soportadas

| Plataforma | Aspecto | Duracion max |
|---|---|---|
| TikTok | 9:16 | 10 min |
| Instagram Reels | 9:16 | 3 min |
| Instagram Stories | 9:16 | 60s |
| Instagram Feed | 1:1 | 60s |
| YouTube Shorts | 9:16 | 3 min |
| YouTube (horizontal) | 16:9 | 12h |
| Twitter/X | 9:16 | 2m20s |
| Facebook Reels | 9:16 | 90s |
| LinkedIn | 9:16 | 10 min |

## Licencia

MIT
