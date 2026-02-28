import discord
from discord.ext import commands
from discord.ext.commands import MemberNotFound, CommandInvokeError
from db import get_database
from config import Config
import random
from dialogs import obtener_dialogo
from assets_utils import combinar_tres_horizontal, obtener_imagen_raza, obtener_imagen_clase, combinar_imagenes_misma_altura, redimensionar_por_alto
import re

'''
TO DO:
-Short decription: classes/races
-Error Handling
-Dev/prod env
-Testing
'''

DISCORD_TOKEN = Config.DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

database = get_database()

# RACES = [
#     "Humano", "Elfo", "Orco", "Enano", "Gnomo", "Goblin", "Trol", "Dracónido", "Tiefling", "Mediano"
# ]

RACES = [
    {"nombre": "Humano", "descripcion": "Maestro en sobrevivir a lunes y dragones."},
    {"nombre": "Elfo", "descripcion": "Orejas largas, paciencia corta."},
    {"nombre": "Orco", "descripcion": "Fuerza bruta, sutileza opcional."},
    {"nombre": "Enano", "descripcion": "Barba épica, altura económica."},
    {"nombre": "Gnomo", "descripcion": "Pequeño tamaño, grandes travesuras."},
    {"nombre": "Goblin", "descripcion": "Pequeño, verde y siempre tramando algo."},
    {"nombre": "Trol", "descripcion": "Grande, fuerte y no muy fan del jabón."},
    {"nombre": "Dracónido", "descripcion": "Aliento de dragón, aliento matutino."},
    {"nombre": "Tiefling", "descripcion": "Cuernos grandes, secretos más grandes."},
    {"nombre": "Mediano", "descripcion": "Nunca rechaza una segunda cena."}
]

# CLASSES = [
#     "Guerrero", "Mago", "Druida", "Ladrón", "Paladín", "Bárbaro", "Clérigo", "Hechicero", "Monje", "Explorador"
# ]

CLASSES = [
    {"letra": "A", "nombre": "Guerrero", "descripcion": "Resuelve todo a golpes, incluso los acertijos."},
    {"letra": "B", "nombre": "Mago", "descripcion": "Hace magia... y desaparecer su dinero."},
    {"letra": "C", "nombre": "Druida", "descripcion": "Habla con plantas. Las plantas no responden."},
    {"letra": "D", "nombre": "Ladrón", "descripcion": "Tu bolsa no está segura cerca de él."},
    {"letra": "E", "nombre": "Paladín", "descripcion": "Justicia en armadura... y a veces en exceso."},
    {"letra": "F", "nombre": "Bárbaro", "descripcion": "Grita primero, pregunta después."},
    {"letra": "G", "nombre": "Clérigo", "descripcion": "Reza por ti... y por su suerte en los dados."},
    {"letra": "H", "nombre": "Hechicero", "descripcion": "Poder innato, excusas infinitas."},
    {"letra": "I", "nombre": "Monje", "descripcion": "Golpea rápido, medita lento."},
    {"letra": "J", "nombre": "Explorador", "descripcion": "Siempre perdido, pero con estilo."}
]


OBJETOS_TIENDA = [
    {"nombre": "Elixir de la Bruma", "emoji": "🏺", "precio": 200, "descripcion": "Mejora tu suerte en el duelo: si pierdes, tu fortuna no disminuye."},
    {"nombre": "Hongo del Abismo", "emoji": "🍄", "precio": 100, "descripcion": "Afecta a tu enemigo: si eres derrotado, ambos pierden §100 monedas."},
    {"nombre": "Pizza con yogur", "emoji": "🍕", "precio": 200, "descripcion": "Multiplica tu bolsa: si ganas el duelo, tus monedas se multiplican por tres."}
]
OBJETOS_ESPECIALES = [obj["nombre"] for obj in OBJETOS_TIENDA]
IMAGE_HEIGHT = 120
PRECIO_CAMBIO = 200


@bot.command(name="info")
async def info(ctx):
    mensaje = (
        "**Comandos principales:**\n"
        "`!razas` y `!clases` - Consulta las opciones disponibles.\n"
        "`!elegir <número de raza><letra de clase>` - Crea tu perfil eligiendo raza y clase.\n"
        "`!perfil` - Muestra tu perfil actual.\n"
        "`!duelo @usuario` - Reta a otro aventurero a un duelo.\n"
        f"`!cambiar_raza <número>` - Cambia tu raza por un precio.\n"
        f"`!cambiar_clase <letra>` - Cambia tu clase por un precio.\n"
        "`!tienda` - Muestra los objetos que puedes comprar al mercader.\n"
        "`!comprar <número>` - Compra un objeto de la tienda para tu inventario.\n"
        "`!top` - Muestra el top 5 de los jugadores con más monedas.\n"
        "\n"
        "**Reglas y mecánicas:**\n"
        f"- Cambiar de raza o clase cuesta {PRECIO_CAMBIO} monedas.\n"
        "- Los duelos se resuelven con dados. El ganador obtiene monedas del perdedor.\n"
        "- Si pierdes todas tus monedas, tu perfil será eliminado y deberás empezar de nuevo.\n"
        "- Los objetos de la tienda pueden alterar el resultado de los duelos.\n"
        "- Los objetos se usan automáticamente en los duelos si tienes alguno en tu inventario.\n"
        "- Si tienes más de un objeto especial en tu inventario, se usará uno de manera aleatoria en el duelo.\n"
        "- Solo puedes tener un ejemplar de cada objeto en tu inventario.**\n"
        "- Recuerda, NUNCA retar al bot.**\n"

    )
    await ctx.send(mensaje)

@bot.command(name="razas")
async def listar_razas(ctx):
    # razas_text = "\n".join([f"{i+1}. {raza}" for i, raza in enumerate(RACES)])
    # await ctx.send(
    #     f"Las razas disponibles son:\n\n{razas_text}\n"
    #     "\nElige sabiamente... o no, igual el destino te alcanzará."
    # )
    mensaje = "**Las razas disponibles son:**\n\n"
    for i, raza in enumerate(RACES, 1):
        mensaje += f"{i}. **{raza['nombre']}** — {raza['descripcion']}\n"
    await ctx.send(mensaje)

@bot.command(name="clases")
async def listar_clases(ctx):
    # letras = "ABCDEFGHIJ"
    # clases_text = "\n".join([f"{letras[i]}. {clase}" for i, clase in enumerate(CLASSES)])
    # await ctx.send(
    #     f"Las sendas del infortunio te ofrecen estas clases:\n\n{clases_text}\n"
    #     "\nRecuerda: ningún mago ha muerto de viejo, y ningún bárbaro ha muerto de sabio."
    # )
    mensaje = "**Las sendas del infortunio te ofrecen estas clases:**\n\n"
    for clase in CLASSES:
        mensaje += f"{clase['letra']}. **{clase['nombre']}** — {clase['descripcion']}\n"
    await ctx.send(mensaje)

@bot.command(name="elegir")
async def elegir(ctx, opcion: str):
    # Verifica si el usuario ya tiene un perfil creado
    user = await database.read_user(ctx.author.id)
    if user:
        await ctx.send("Ya tienes un perfil. Si quieres cambiar de raza o clase, usa `!cambiar_raza` o `!cambiar_clase`.")
        return

    # Usa regex para separar el número de raza (uno o más dígitos) y la letra de clase
    match = re.match(r"^(\d+)([A-Za-z])$", opcion)
    if not match:
        # Si el formato es incorrecto, muestra un mensaje de ayuda
        await ctx.send(
            "Formato incorrecto. Usa `!elegir <número de raza><letra de clase>`, por ejemplo: `!elegir 10H`.\n"
            "Consulta las razas con `!razas` y las clases con `!clases`."
        )
        return

    # Extrae el número de raza y la letra de clase del input del usuario
    raza_num = int(match.group(1))      # Número de raza (puede ser de más de un dígito)
    clase_letra = match.group(2).upper()  # Letra de clase, convertida a mayúscula


    try:
        raza_idx = raza_num - 1
        if raza_idx < 0 or raza_idx >= len(RACES):
            raise ValueError
    except ValueError:
        await ctx.send("Tu elección de raza es tan absurda como un dragón vegetariano. Usa `!razas` para ver las opciones.")
        return

    letras = "ABCDEFGHIJ"
    if clase_letra not in letras:
        await ctx.send("¿Clase secreta? No existe. Usa `!clases` para ver las opciones.")
        return
    clase_idx = letras.index(clase_letra)
    clase = CLASSES[clase_idx]
    raza = RACES[raza_idx]

    img_raza = redimensionar_por_alto(obtener_imagen_raza(raza["nombre"]), alto=IMAGE_HEIGHT)
    img_clase = redimensionar_por_alto(obtener_imagen_clase(clase["nombre"]), alto=IMAGE_HEIGHT)
    img_combinada = combinar_imagenes_misma_altura(img_raza, img_clase, alto=IMAGE_HEIGHT)
    await ctx.send(file=discord.File(img_combinada))

    username = ctx.author.name
    await database.create_user(ctx.author.id, username=username, race=raza, user_class=clase)
    await ctx.send(
        f"{ctx.author.mention}, los dioses te vigilan mientras eliges:\n"
        f"Raza: **{raza['nombre']}**\nClase: **{clase['nombre']}**\n"
        f"Se te ha otorgado un tributo celestial por **§1000** monedas\n"
        "Tu destino está sellado... por ahora."
    )

@bot.command(name="cambiar_raza")
async def cambiar_raza(ctx, numero: int):
    if numero < 1 or numero > len(RACES):
        await ctx.send(obtener_dialogo("error_razas"))
        return
    user = await database.read_user(ctx.author.id)
    if not user or not user.get("race") or not user.get("class"):
        await ctx.send("Primero debes forjar tu destino con !elegir.")
        return
    raza = RACES[numero - 1]
    if user.get("race") == raza:
        await ctx.send(obtener_dialogo("cambiar_raza_misma", user=ctx.author.mention))
        return
    coins = user.get("coins", 0)
    if coins < PRECIO_CAMBIO:
        await ctx.send(f"Tus bolsillos están tan vacíos como tu esperanza. Necesitas {PRECIO_CAMBIO} monedas para cambiar de raza.")
        return
    new_coins = coins - PRECIO_CAMBIO
    if new_coins <= 0:
        await database.delete_user(ctx.author.id)
        await ctx.send(obtener_dialogo("cambiar_raza_muerte", user=ctx.author.mention))
    else:
        await database.update_user(ctx.author.id, {"race": raza, "coins": new_coins})
        await ctx.send(obtener_dialogo("cambiar_raza_exito", user=ctx.author.mention, raza=raza["nombre"], coins=new_coins))
        imagen_raza = redimensionar_por_alto(obtener_imagen_raza(raza["nombre"]), alto=IMAGE_HEIGHT)
        await ctx.send(file=discord.File(imagen_raza))

@bot.command(name="cambiar_clase")
async def cambiar_clase(ctx, letra: str):
    letras = "ABCDEFGHIJ"
    letra = letra.upper()
    if letra not in letras:
        await ctx.send(obtener_dialogo("error_clases"))
        return
    user = await database.read_user(ctx.author.id)
    if not user or not user.get("race") or not user.get("class"):
        await ctx.send("Primero debes elegir tu destino con !elegir.")
        return
    clase = CLASSES[letras.index(letra)]
    if user.get("class") == clase:
        await ctx.send(obtener_dialogo("cambiar_clase_misma", user=ctx.author.mention))
        return
    coins = user.get("coins", 0)
    if coins < PRECIO_CAMBIO:
        await ctx.send(f"No tienes suficientes monedas. Necesitas {PRECIO_CAMBIO} monedas para cambiar de clase.")
        return
    new_coins = coins - PRECIO_CAMBIO
    if new_coins <= 0:
        await database.delete_user(ctx.author.id)
        await ctx.send(obtener_dialogo("cambiar_clase_muerte", user=ctx.author.mention))
    else:
        await database.update_user(ctx.author.id, {"class": clase, "coins": new_coins})
        await ctx.send(obtener_dialogo("cambiar_clase_exito", user=ctx.author.mention, clase=clase["nombre"], coins=new_coins))
        imagen_clase = redimensionar_por_alto(obtener_imagen_clase(clase["nombre"]), alto=IMAGE_HEIGHT)
        await ctx.send(file=discord.File(imagen_clase))

@bot.command(name="perfil")
async def perfil(ctx):
    user = await database.read_user(ctx.author.id)
    if not user:
        await ctx.send(obtener_dialogo("perfil_vacio", user=ctx.author.mention))
        return
    if user.get("coins", 0) <= 0:
        await database.delete_user(ctx.author.id)
        await ctx.send(
            f"{ctx.author.mention}, tu alma ha sido reclamada por la pobreza. "
            "Tu perfil ha sido eliminado. Usa `!elegir <número de raza><letra de clase>` para renacer."
        )
        return
    raza = user.get("race", "No elegida")
    clase = user.get("class", "No elegida")
    coins = user.get("coins", 0)
    inventory = user.get("inventory", [])

    if isinstance(clase, str):
        clase = next((c for c in CLASSES if c["nombre"] == clase), {"nombre": clase})

    # Añade emojis al inventario y muestra cada objeto en una línea
    if inventory:
        inventario_str = "\n" + "\n".join(
        f"- {next((obj['emoji'] for obj in OBJETOS_TIENDA if obj['nombre'] == item), '')} {item}"
        for item in inventory
        )
    else:
        inventario_str = obtener_dialogo(
            "perfil_inventario_vacio",
            user=ctx.author.mention,
            raza=raza["nombre"],
            clase=clase["nombre"],
            coins=coins
        )

    # Imágenes raza y clase
    imagen_raza = obtener_imagen_raza(raza["nombre"])
    imagen_clase = obtener_imagen_clase(clase["nombre"])
    ruta_combinada = combinar_imagenes_misma_altura(imagen_raza, imagen_clase, alto=IMAGE_HEIGHT)
    await ctx.send(file=discord.File(ruta_combinada))

    if inventory:
        await ctx.send(obtener_dialogo(
            "perfil",
            user=ctx.author.mention,
            raza=raza,
            clase=clase,
            coins=coins,
            inventario=inventario_str
        ))
    else:
        await ctx.send(inventario_str)

@bot.command(name="duelo")
async def duelo(ctx, oponente: discord.Member):

    retador = await database.read_user(ctx.author.id)
    rival = await database.read_user(oponente.id)

    if not retador:
        await ctx.send(
            f"No puedes desafiar a nadie, porque no eres más que un eco inexistente.\n"
            f"El tiempo de esconderse terminó. Crea tu personaje antes de enfrentar tu inevitable derrota.\n Usa `!elegir <número><letra>`"
        )
        return

    if oponente.id == bot.user.id:
        if retador and retador.get("coins", 0) >= 100:
            await ctx.send(f"{ctx.author.mention}, ¿Tu osadía es fascinante, aventurero, pero todo en este mundo obedece a mi voluntad.\nUn simple aventurero que cree poder dictar las reglas del mundo que yo mismo he tejido.\n¿Acaso no ves que cada piedra, cada sombra y cada monstruo obedece a mi voluntad?\nAprende, mortal, que desafiarme es invocar tu propia condena.")
            await database.update_user(ctx.author.id, {"coins": retador["coins"] - 200})
            await ctx.send("- Un hechizo cae sobre ti y tu fortuna se desvanece: **§200 monedas desaparecen de tu alforja**")

            retador_actualizado = await database.read_user(ctx.author.id)
            if retador_actualizado.get("coins", 0) <= 0:
                await database.delete_user(ctx.author.id)
                await ctx.send(
                    f"{ctx.author.mention} ha perdido toda su fortuna y su historia se disuelve en el olvido perpetuo.\n"
                    "Crea un nuevo personaje con `!elegir <número de raza><letra de clase>`."
                )
        return

    if not rival:
        await ctx.send(
            f"Tu rival debe tener su destino escrito en el grimorio. "
            f"{oponente.mention}, deja de esconderte y crea tu personaje antes de enfrentar tu inevitable derrota.\nRenace con `!elegir <número de raza><letra de clase>`"
        )
        return

    if oponente.id == retador["user_id"]:
        await ctx.send(f"¿Puede alguien ser más denso que un slime? No puedes batirte en duelo contigo mismo, aunque sería divertido verte perder. {oponente.mention}, busca un verdadero oponente.")
        return

    if retador.get("coins", 0) < 100 or rival.get("coins", 0) < 100:
        await ctx.send(
            "Ambos deben tener al menos §100 monedas para arriesgar en este duelo. "
            "Sin oro, solo les queda pelear por migajas... o por su dignidad."
        )
        return

    raza_retador = retador.get("race")
    raza_oponente = rival.get("race")

    # Imágenes duelo
    img_retador = redimensionar_por_alto(obtener_imagen_raza(raza_retador["nombre"]), alto=IMAGE_HEIGHT)
    img_versus = redimensionar_por_alto("assets/duelo_versus.png", alto=IMAGE_HEIGHT)
    img_oponente = redimensionar_por_alto(obtener_imagen_raza(raza_oponente["nombre"]), alto=IMAGE_HEIGHT)

    ruta_combinada = combinar_tres_horizontal(img_retador, img_versus, img_oponente, alto=IMAGE_HEIGHT)
    await ctx.send(file=discord.File(ruta_combinada))


    dado_jugador = random.randint(1, 20)
    dado_rival = random.randint(1, 20)

    # Aplica el objeto especial (si existe) y recibe el efecto y mensaje
    efecto, mensaje_objeto = await aplicar_objeto_duelo(
        ctx, retador, rival, dado_jugador, dado_rival, oponente
    )

    # Construye el resultado base
    resultado = (
        f"En la Arena del Azar, {ctx.author.mention} lanza su dado y obtiene **{dado_jugador}**.\n"
        f"{oponente.mention} responde con un giro dramático y saca **{dado_rival}**.\n"
    )

    if mensaje_objeto:
        resultado += mensaje_objeto + "\n"

    if dado_jugador > dado_rival:
        # El retador gana el duelo
        saldo_previo = retador["coins"]
        if efecto == "pizza_yogur":
            ganancia = 100 * 3
            saldo_final = saldo_previo + ganancia
            await database.update_user(ctx.author.id, {"coins": saldo_final})
            nuevo_saldo_oponente = rival["coins"] - 100
            await database.update_user(oponente.id, {"coins": nuevo_saldo_oponente})
        else:
            ganancia = 100
            saldo_final = saldo_previo + ganancia
            await database.update_user(ctx.author.id, {"coins": saldo_final})
            nuevo_saldo_oponente = rival["coins"] - ganancia
            await database.update_user(oponente.id, {"coins":  nuevo_saldo_oponente})
        # Construye y envía el mensaje de resultado (incluyendo mensaje_objeto si aplica)
        resultado += (
            f"¡{ctx.author.mention} aplasta a su rival y saquea §{ganancia} monedas de su bolsa! {oponente.mention}, siempre puedes vender tu dignidad para recuperar el oro perdido.\n"
        )
        rival_actualizado = await database.read_user(oponente.id)
        if rival_actualizado and rival_actualizado.get("coins", 0) <= 0:
            await database.delete_user(oponente.id)
            resultado += (
                f"\n{oponente.mention}, tus arcas se vaciaron en un suspiro, y tu nombre fue borrado de los pergaminos del tiempo.\n"
                "Deberás crear un nuevo perfil con `!elegir <número de raza><letra de clase>`."
    )


        await ctx.send(resultado)
        return
    elif dado_rival > dado_jugador:
        if efecto == "elixir_bruma":
            # El retador NO pierde monedas
            await database.update_user(ctx.author.id, {"coins": retador["coins"]})
            await database.update_user(oponente.id, {"coins": rival["coins"] + 100})
            #resultado += mensaje_objeto
            await ctx.send(resultado)
            return
        elif efecto == "hongo_abismo":
            coins_jugador = max(1, retador["coins"] - 100)
            coins_oponente = max(1, rival["coins"] - 100)
            # El retador pierde monedas normalmente
            await database.update_user(ctx.author.id, {"coins": coins_jugador})
            # El oponente pierde 100 monedas extra (pero if dado_jugador > enos de 1)
            await database.update_user(oponente.id, {"coins": coins_oponente})
            await ctx.send(resultado)
            return
        else:
            # Lógica normal de duelo
            await database.update_user(ctx.author.id, {"coins": retador["coins"] - 100})
            await database.update_user(oponente.id, {"coins": rival["coins"] + 100})
            nuevo_saldo = retador["coins"] - 100
            await database.update_user(ctx.author.id, {"coins": nuevo_saldo})
            await database.update_user(oponente.id, {"coins": rival["coins"] + 100})
            if nuevo_saldo <= 0:
                await database.delete_user(ctx.author.id)
                resultado += (
                    f"\n{ctx.author.mention}, tus arcas se vaciaron en un suspiro, y tu nombre fue borrado de los pergaminos del tiempo.\n"
                    "Deberá crear un nuevo perfil con `!elegir <número de raza><letra de clase>`."
                )
            else:
                resultado += (
                    f"¡{oponente.mention} se alza victorioso y roba §100 monedas! "
                    f"{ctx.author.mention}, quizás la suerte te sonría en tu próxima vida... o no."
                )
            await ctx.send(resultado)
            return
    else:
        # Empate
        resultado += (
            "¡Empate! Los dioses del azar se burlan de ambos y nadie gana ni pierde monedas. "
            "Quizás deberían dedicarse a la poesía."
        )

        await ctx.send(resultado)

@duelo.error
async def duelo_error(ctx, error):
    if isinstance(error, MemberNotFound):
        await ctx.send("¡Intentaste batirte en duelo con un fantasma! Ese usuario no existe en este servidor o no lo mencionaste correctamente. Usa `!duelo @usuario`.")
    else:
        print(error)
        await ctx.send("Algo salió mal en el duelo. Los dioses del código están confundidos.")


# Uso de objetos en duelo
async def aplicar_objeto_duelo(ctx, user, oponente_db, dado_user, dado_oponente, oponente_member):
    inventario = user.get("inventory", [])
    efecto = None
    mensaje = ""

    especiales = [nombre for nombre in OBJETOS_ESPECIALES if nombre in inventario]
    if not especiales:
        return None, ""

    objeto_usado = random.choice(especiales)

    # Elixir de la Bruma: solo se elimina si pierde
    if objeto_usado == "Elixir de la Bruma" and dado_user < dado_oponente:
        inventario.remove(objeto_usado)
        await database.update_user(ctx.author.id, {"inventory": inventario})
        efecto = "elixir_bruma"
        mensaje = obtener_dialogo("duelo_objeto_elixir_bruma", user=ctx.author.mention)
    # Hongo del Abismo: solo se elimina si pierde
    elif objeto_usado == "Hongo del Abismo" and dado_user < dado_oponente:
        inventario.remove(objeto_usado)
        await database.update_user(ctx.author.id, {"inventory": inventario})
        efecto = "hongo_abismo"
        mensaje = obtener_dialogo("duelo_objeto_hongo_abismo", user=ctx.author.mention, enemigo=oponente_member.mention)
    # Pizza con yogur: solo se elimina si gana
    elif objeto_usado == "Pizza con yogur" and dado_user > dado_oponente:
        inventario.remove(objeto_usado)
        await database.update_user(ctx.author.id, {"inventory": inventario})
        efecto = "pizza_yogur"
        mensaje = obtener_dialogo("duelo_objeto_pizza_yogur", user=ctx.author.mention)
    return efecto, mensaje


@bot.command(name="tienda")
async def mostrar_tienda(ctx):
    intro = obtener_dialogo("tienda_intro", user=ctx.author.mention)
    mensaje = f"{intro}\n\n"
    for i, obj in enumerate(OBJETOS_TIENDA, 1):
        mensaje += f"{i}. **{obj['emoji']} {obj['nombre']}** (§{obj['precio']}): {obj['descripcion']}\n"
    mensaje += "\nUsa `!comprar <número>` para adquirir un objeto."
    imagen_mercader = redimensionar_por_alto("assets/mercader.png", alto=IMAGE_HEIGHT)
    await ctx.send(file=discord.File(imagen_mercader))
    await ctx.send(mensaje)

@bot.command(name="comprar")
async def comprar_objeto(ctx, numero: int):
    user = await database.read_user(ctx.author.id)
    if not user:
        await ctx.send("Debes tener un perfil antes de comprar. Usa `!elegir <número de raza><letra de clase>` para crearlo.")
        return
    if numero < 1 or numero > len(OBJETOS_TIENDA):
        await ctx.send("Ese objeto no existe en la tienda. Usa `!tienda` para ver las opciones.")
        return
    objeto = OBJETOS_TIENDA[numero - 1]
    inventario = user.get("inventory", [])
    if objeto["nombre"] in inventario:
        imagen_mercader = redimensionar_por_alto("assets/mercader.png", alto=IMAGE_HEIGHT)
        await ctx.send(file=discord.File(imagen_mercader))
        await ctx.send(f"Ya tienes un **{objeto['emoji']} {objeto['nombre']}** en tu inventario. Apacigua tu codicia.")
        return
    coins = user.get("coins", 0)
    if coins < objeto["precio"]:
        imagen_mercader = redimensionar_por_alto("assets/mercader.png", alto=IMAGE_HEIGHT)
        await ctx.send(file=discord.File(imagen_mercader))
        await ctx.send(obtener_dialogo("compra_fallo", user=ctx.author.mention))
        return
    nuevo_inventario = inventario + [objeto["nombre"]]
    await database.update_user(ctx.author.id, {
        "coins": coins - objeto["precio"],
        "inventory": nuevo_inventario
    })
    imagen_mercader = redimensionar_por_alto("assets/mercader.png", alto=IMAGE_HEIGHT)
    await ctx.send(file=discord.File(imagen_mercader))
    await ctx.send(
        obtener_dialogo("compra_exito", user=ctx.author.mention, objeto=f"{objeto['emoji']} {objeto['nombre']}")
    )

@bot.command(name="top")
async def top(ctx, top: int = 3):
    # Obtén todos los usuarios de la base de datos
    usuarios = await database.get_all_users()  # Debes implementar este método si no existe
    if not usuarios:
        await ctx.send("No hay usuarios registrados aún.")
        return

    # Ordena por monedas descendente
    usuarios.sort(key=lambda u: u.get("coins", 0), reverse=True)

    # Agrupa usuarios por cantidad de monedas
    ranking = []
    last_coins = None
    current_group = []
    for user in usuarios:
        coins = user.get("coins", 0)
        if coins != last_coins:
            if current_group:
                ranking.append((last_coins, current_group))
            current_group = [user]
            last_coins = coins
        else:
            current_group.append(user)
    if current_group:
        ranking.append((last_coins, current_group))

    emojis = ["🥇", "🥈", "🥉"]

    # Muestra solo los primeros 'top' puestos
    mensaje = "**El Panteón de la Opulencia:**\n\n"
    puesto = 1
    for idx, (coins, group) in enumerate(ranking[:top], 1):
        nombres = ", ".join(u.get("username", "Desconocido") for u in group)
        if idx <= 3:
            mensaje += f"{emojis[idx - 1]} {nombres} — **§{coins}** monedas\n"
        else:
            mensaje += f"{idx}. {nombres} — **§{coins}** monedas\n"

    await ctx.send(mensaje)

bot.run(DISCORD_TOKEN)