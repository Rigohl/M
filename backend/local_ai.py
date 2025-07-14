from transformers import pipeline
from PIL import Image, ImageDraw, ImageFont


# Generación de texto con Hugging Face
async def generate_song_lyrics_local(prompt: str):
    try:
        generator = pipeline("text-generation", model="gpt2")
        result = generator(prompt, max_length=200, num_return_sequences=1)
        return result[0]["generated_text"]
    except Exception as e:
        raise Exception(f"Error al generar letras: {str(e)}")


# Generación de arte de álbum con PIL
async def generate_album_art_local(description: str):
    try:
        # Crear una imagen básica con texto
        img = Image.new("RGB", (600, 600), color=(73, 109, 137))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((10, 10), description, fill=(255, 255, 0), font=font)
        img.save("album_art.png")
        return "album_art.png"
    except Exception as e:
        raise Exception(f"Error al generar arte de álbum: {str(e)}")
