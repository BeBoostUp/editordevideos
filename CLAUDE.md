# Editor de Videos para Redes Sociales

## Descripcion del proyecto

Herramienta de edicion de video automatizada para preparar contenido listo para publicar en cualquier red social. Usa FFmpeg como motor de procesamiento y Claude Code como interfaz conversacional.

## Estructura del proyecto

```
editordevideos/
├── .claude/
│   └── commands/
│       └── edit-video.md       # Skill principal - invocable con /project:edit-video
├── scripts/
│   └── video_editor.py         # Script Python que orquesta FFmpeg
├── CLAUDE.md                   # Este archivo
└── README.md                   # Documentacion del proyecto
```

## Como usar

El usuario invoca la skill con:
```
/project:edit-video /ruta/al/video.mp4
```

Claude entonces:
1. Analiza el video con ffprobe
2. Hace preguntas sobre la edicion deseada
3. Genera un JSON de configuracion
4. Ejecuta FFmpeg con los parametros correctos
5. Entrega los videos listos para cada plataforma

## Plataformas soportadas

| Plataforma        | Resolucion  | Aspecto | Duracion max |
|-------------------|-------------|---------|--------------|
| TikTok            | 1080x1920   | 9:16    | 10 min       |
| Instagram Reels   | 1080x1920   | 9:16    | 3 min        |
| Instagram Stories | 1080x1920   | 9:16    | 60 seg       |
| Instagram Feed    | 1080x1080   | 1:1     | 60 seg       |
| YouTube Shorts    | 1080x1920   | 9:16    | 3 min        |
| YouTube Landscape | 1920x1080   | 16:9    | 12 horas     |
| Twitter / X       | 1080x1920   | 9:16    | 2m20s        |
| Facebook Reels    | 1080x1920   | 9:16    | 90 seg       |
| LinkedIn          | 1080x1920   | 9:16    | 10 min       |

## Dependencias

- **FFmpeg** (con ffprobe) - motor de procesamiento de video
- **Python 3.8+** - script orquestador

## Comandos utiles

```bash
# Ver informacion de un video
python3 scripts/video_editor.py info video.mp4

# Listar plataformas disponibles
python3 scripts/video_editor.py platforms

# Editar video con configuracion JSON
python3 scripts/video_editor.py edit --config config.json
```

## Funcionalidades de edicion

- Recorte temporal (trim inicio/fin)
- Cambio de velocidad (0.5x a 2x)
- Texto superpuesto con posicion y timing
- Musica de fondo con control de volumen
- Ajustes de brillo, contraste y saturacion
- Fade in / fade out
- Re-escalado automatico para cada plataforma
- Padding automatico para mantener aspect ratio
