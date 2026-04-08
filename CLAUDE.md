# Editor de Videos Profesional para Redes Sociales

## Descripcion

Skill de Claude Code para edicion profesional de video. Analiza clips, sugiere ajustes creativos, y genera videos listos para publicar en cualquier red social usando FFmpeg.

## Uso

```
/project:edit-video /ruta/al/video.mp4
```

Para multiples clips:
```
/project:edit-video /ruta/clip1.mp4 /ruta/clip2.mp4 /ruta/clip3.mp4
```

## Flujo de la skill (10 fases)

1. **Prerequisitos** - Verifica ffmpeg/ffprobe
2. **Analisis** - Info tecnica + analisis de brillo, audio, escenas, silencios
3. **Perfil de marca** - Nombre, colores corporativos, logo, tono
4. **Direccion creativa** - Sugerencias basadas en analisis, plataforma, proposito
5. **Estructura y ritmo** - Pacing, orden de clips, tipo de transiciones
6. **Texto y subtitulos** - Overlays, CTAs, subtitulos SRT
7. **Audio y musica** - Audio original, musica fondo, normalizacion
8. **Efectos visuales** - Color grading, fade, vineta, blur background, velocidad
9. **Logo y output** - Marca de agua, thumbnails, directorio salida
10. **Ejecucion** - Resumen, confirmacion, procesamiento

## Comandos del script

```bash
python3 scripts/video_editor.py info video.mp4           # Info basica
python3 scripts/video_editor.py analyze video.mp4         # Analisis profundo
python3 scripts/video_editor.py platforms                 # Plataformas disponibles
python3 scripts/video_editor.py thumbnail video.mp4       # Generar thumbnail
python3 scripts/video_editor.py concat a.mp4 b.mp4 --output out.mp4 --transition fade
python3 scripts/video_editor.py edit --config config.json # Edicion completa
```

## Plataformas soportadas

| Plataforma | Resolucion | Aspecto | Max duracion |
|---|---|---|---|
| TikTok | 1080x1920 | 9:16 | 10 min |
| Instagram Reels | 1080x1920 | 9:16 | 3 min |
| Instagram Stories | 1080x1920 | 9:16 | 60s |
| Instagram Feed | 1080x1080 | 1:1 | 60s |
| YouTube Shorts | 1080x1920 | 9:16 | 3 min |
| YouTube (16:9) | 1920x1080 | 16:9 | 12h |
| Twitter/X | 1080x1920 | 9:16 | 2m20s |
| Facebook Reels | 1080x1920 | 9:16 | 90s |
| LinkedIn | 1080x1920 | 9:16 | 10 min |

## Color grading disponible

none, vivid, warm, cool, vintage, cinematic, bw, moody, clean, high_energy

## Dependencias

- FFmpeg (con ffprobe)
- Python 3.8+
