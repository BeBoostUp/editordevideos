# Editor de Videos de Alto Impacto para Redes Sociales

## Filosofia de Edicion

Este editor NO aplica efectos mecanicamente. Cada decision sigue 3 principios:

1. **Ritmo** - Modular la cadencia (voz como instrumento ritmico, curva dramatica)
2. **Diseno Sonoro** - Construir capas (voz + SFX transicion + SFX impacto + silencio)
3. **Edicion Consciente** - Cada corte, efecto y silencio tiene justificacion narrativa

Guia completa: `resources/guides/edicion_alto_impacto.md`

## Uso

```
/project:edit-video /ruta/al/video.mp4
```

## Reglas Criticas de Edicion

- Las frases SIEMPRE terminan ANTES de aplicar una transicion
- El CTA NUNCA se corta
- Los SFX tienen justificacion narrativa (no se anaden por anadir)
- El audio se limpia suavemente (no destruir naturalidad)
- Los subtitulos se transcriben del VIDEO FINAL para sync perfecto
- Cada silencio detectado es un punto natural de transicion

## Flujo (10 fases)

1. **Prerequisitos** - ffmpeg/ffprobe
2. **Analisis** - Info + brillo + loudness + escenas + silencios
3. **Perfil de marca** - Nombre, colores, logo, tono
4. **Direccion creativa** - Sugerencias basadas en analisis
5. **Estructura y ritmo** - Curva dramatica, hook/cuerpo/CTA, transiciones
6. **Subtitulos** - Estilo CapCut, sync perfecto, palabras clave resaltadas
7. **Diseno sonoro** - Capas: voz + SFX transicion + SFX impacto + silencio
8. **Efectos visuales** - Color grading, vineta, fade
9. **Output** - Logo, thumbnail, directorio
10. **Ejecucion** - Resumen, confirmacion, render

## Biblioteca de Recursos: 318 assets

- 68 transiciones (58 built-in + 10 custom)
- 38+ color grades
- 72 efectos visuales
- 84 SFX (6 pro whoosh + 43 glitch + 35 generados)
- 12 estilos de subtitulos
- 10 efectos de audio
- 2133 tipografias instaladas

Catalogo: `resources/catalog.json`

## Comandos

```bash
python3 scripts/video_editor.py info video.mp4
python3 scripts/video_editor.py analyze video.mp4
python3 scripts/video_editor.py platforms
python3 scripts/video_editor.py thumbnail video.mp4
python3 scripts/video_editor.py concat a.mp4 b.mp4 --output out.mp4 --transition fade
python3 scripts/video_editor.py edit --config config.json
```

## Dependencias

- FFmpeg (con ffprobe)
- Python 3.8+
- Whisper (para transcripcion automatica)
