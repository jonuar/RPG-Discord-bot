import unicodedata
from PIL import Image

def quitar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def obtener_imagen_raza(raza):
    return f"assets/raza_{quitar_acentos(raza.lower())}.png"

def obtener_imagen_clase(clase):
    return f"assets/clase_{quitar_acentos(clase.lower())}.png"

def combinar_imagenes_misma_altura(ruta1, ruta2, alto):
    img1 = Image.open(ruta1)
    img2 = Image.open(ruta2)
    # Redimensiona ambas imágenes al mismo alto, ajustando el ancho proporcionalmente
    proporcion1 = alto / img1.height
    ancho1 = int(img1.width * proporcion1)
    img1 = img1.resize((ancho1, alto))

    proporcion2 = alto / img2.height
    ancho2 = int(img2.width * proporcion2)
    img2 = img2.resize((ancho2, alto))

    # Crea una nueva imagen para combinar ambas
    nueva = Image.new('RGBA', (ancho1 + ancho2, alto))
    nueva.paste(img1, (0, 0))
    nueva.paste(img2, (ancho1, 0))
    nueva_ruta = "temp_combinada.png"
    nueva.save(nueva_ruta)
    return nueva_ruta

def redimensionar_por_alto(ruta, alto=100):
    img = Image.open(ruta)
    proporcion = alto / img.height
    ancho = int(img.width * proporcion)
    img = img.resize((ancho, alto))
    nueva_ruta = f"temp_{ruta.replace('/', '_')}"
    img.save(nueva_ruta)
    return nueva_ruta