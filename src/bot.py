import discord
from discord.ext import commands
from db import get_database
from config import Config
import random
from dialogs import obtener_dialogo



DISCORD_TOKEN = Config.DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Listas de razas y clases
RACES = [
    "Humano", "Elfo", "Orco", "Enano", "Gnomo", "Goblin", "Trol", "Dracónido", "Tiefling", "Mediano"
]
CLASSES = [
    "Guerrero", "Mago", "Druida", "Ladrón", "Paladín", "Bárbaro", "Clérigo", "Hechicero", "Monje", "Explorador"
]

# Conexión a db
database = get_database()

# Define los objetos especiales del mercader
OBJETOS_TIENDA = [
    {"nombre": "Elixir de la Bruma", "precio": 200, "descripcion": "Mejora tu suerte en el duelo: si pierdes, tu fortuna no disminuye."},
    {"nombre": "Hongo del Abismo", "precio": 100, "descripcion": "Afecta a tu enemigo: si eres derrotado, tu enemigo pierde §100 monedas."},
    {"nombre": "Pizza con yogur", "precio": 200, "descripcion": "Multiplica tu bolsa: si ganas el duelo, tus monedas se multiplican por tres."}
]

# Define el precio de cambiar raza o clase en una sola variable
PRECIO_CAMBIO = 200

OBJETOS_ESPECIALES = [
    "Elixir de la Bruma",
    "Hongo del Abismo",
    "Pizza con yogur"
]

@bot.command(name="info")
async def info(ctx):
    mensaje = (
        "**Comandos principales:**\n"
        "`!razas` y `!clases` - Consulta las opciones disponibles.\n"
        "`!elegir <número><letra>` - Crea tu perfil eligiendo raza y clase.\n"
        "`!perfil` - Muestra tu perfil actual.\n"
        "`!duelo @usuario` - Reta a otro jugador a un duelo.\n"
        f"`!cambiar_raza <número>` - Cambia tu raza por un precio.\n"
        f"`!cambiar_clase <letra>` - Cambia tu clase por un precio.\n"
        "`!tienda` - Muestra los objetos que puedes comprar al mercader.\n"
        "`!comprar <número>` - Compra un objeto de la tienda para tu inventario.\n"
        "\n"
        "**Reglas y mecánicas:**\n"
        f"- Cambiar de raza o clase cuesta {PRECIO_CAMBIO} monedas.\n"
        "- Los duelos se resuelven con dados. El ganador obtiene monedas del perdedor.\n"
        "- Si pierdes todas tus monedas, tu perfil será eliminado y deberás empezar de nuevo.\n"
        "- Los objetos de la tienda pueden alterar el resultado de los duelos.\n"
        "- Los objetos se usan automáticamente en los duelos si tienes alguno en tu inventario.\n"
        "- Si tienes más de un objeto especial en tu inventario, se usará uno de manera aleatoria en el duelo.\n"
    )
    await ctx.send(mensaje)

@bot.command(name="razas")
async def listar_razas(ctx):
    razas_text = "\n".join([f"{i+1}. {raza}" for i, raza in enumerate(RACES)])
    await ctx.send(
        f"En el gran libro de los condenados, las razas disponibles son:\n{razas_text}\n"
        "\nElige sabiamente... o no, igual el destino te alcanzará."
    )

@bot.command(name="clases")
async def listar_clases(ctx):
    letras = "ABCDEFGHIJ"
    clases_text = "\n".join([f"{letras[i]}. {clase}" for i, clase in enumerate(CLASSES)])
    await ctx.send(
        f"Las sendas del infortunio te ofrecen estas clases:\n{clases_text}\n"
        "\nRecuerda: ningún mago ha muerto de viejo, y ningún bárbaro ha muerto de sabio."
    )

@bot.command(name="elegir")
async def elegir(ctx, opcion: str):
    user = await database.read_user(ctx.author.id)
    if user:
        await ctx.send("Ya tienes un perfil. Si quieres cambiar de raza o clase, usa `!cambiar_raza` o `!cambiar_clase`.")
        return
    if len(opcion) < 2:
        await ctx.send("¿Intentas engañar al destino? Usa el formato correcto, mortal: `!elegir 1C`.")
        return

    raza_idx = opcion[0]
    clase_letra = opcion[1].upper()

    try:
        raza_idx = int(raza_idx) - 1
        if raza_idx < 0 or raza_idx >= len(RACES):
            raise ValueError
    except ValueError:
        await ctx.send("Tu elección de raza es tan válida como un dragón vegetariano. Usa `!razas` para ver las opciones.")
        return

    letras = "ABCDEFGHIJ"
    if clase_letra not in letras:
        await ctx.send("¿Clase secreta? No existe. Usa `!clases` para ver las opciones.")
        return
    clase_idx = letras.index(clase_letra)
    clase = CLASSES[clase_idx]
    raza = RACES[raza_idx]

    username = ctx.author.name
    await database.create_user(ctx.author.id, username=username, race=raza, user_class=clase)
    await ctx.send(
        f"{ctx.author.mention}, los dioses te vigilan mientras eliges:\n"
        f"Raza: **{raza}**\nClase: **{clase}**\n"
        f"Se te otorga un tributo celestial por **§1000** monedas"
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
        await ctx.send(obtener_dialogo("cambiar_raza_exito", user=ctx.author.mention, raza=raza, coins=new_coins))

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
        await ctx.send(obtener_dialogo("cambiar_clase_exito", user=ctx.author.mention, clase=clase, coins=new_coins))

@bot.command(name="perfil")
async def mostrar_perfil(ctx):
    user = await database.read_user(ctx.author.id)
    if not user:
        await ctx.send(obtener_dialogo("perfil_vacio"))
        return
    raza = user.get("race", "No elegida")
    clase = user.get("class", "No elegida")
    coins = user.get("coins", 0)
    inventory = user.get("inventory", [])
    inventario_str = ', '.join(inventory) if inventory else obtener_dialogo(
        "perfil_inventario_vacio",
        user=ctx.author.mention,
        raza=raza,
        clase=clase,
        coins=coins
    )

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
    if oponente.id == ctx.author.id:
        await ctx.send("¿Te has mirado al espejo últimamente? No puedes batirte en duelo contigo mismo, aunque sería divertido verte perder.")
        return

    jugador = await database.read_user(ctx.author.id)
    rival = await database.read_user(oponente.id)

    if not jugador or not rival:
        await ctx.send(
            f"Ambos aventureros deben tener un destino escrito en el grimorio (`!elegir`). "
            f"{oponente.mention}, deja de esconderte y crea tu personaje antes de enfrentar tu inevitable derrota."
        )
        return

    if jugador.get("coins", 0) < 100 or rival.get("coins", 0) < 100:
        await ctx.send(
            "Ambos deben tener al menos §100 monedas para arriesgar en este duelo. "
            "Sin oro, solo les queda pelear por migajas... o por su dignidad."
        )
        return

    dado_jugador = random.randint(1, 20)
    dado_rival = random.randint(1, 20)

    # Aplica el objeto especial (si existe) y recibe el efecto y mensaje
    efecto, mensaje_objeto = await aplicar_objeto_duelo(
        ctx, jugador, rival, dado_jugador, dado_rival
    )

    # Construye el resultado base
    resultado = (
        f"En la Arena del Azar, {ctx.author.mention} lanza su dado y obtiene **{dado_jugador}**.\n"
        f"{oponente.mention} responde con un giro dramático y saca **{dado_rival}**.\n"
    )

    if mensaje_objeto:
        resultado += mensaje_objeto + "\n"

    if dado_jugador > dado_rival:
        if efecto == "pizza_yogur":
            pass
        await database.update_user(ctx.author.id, {"coins": jugador["coins"] + 100})
        await database.update_user(oponente.id, {"coins": rival["coins"] - 100})
        # ¿Oponente murió?
        if rival["coins"] - 100 <= 0:
            await database.delete_user(oponente.id)
            resultado += (
                f"\n{oponente.mention} ha perdido todas sus monedas y su alma ha sido reclamada. "
                "Deberá forjar un nuevo destino con `!elegir`."
            )
        else:
            resultado += (
                f"¡{ctx.author.mention} aplasta a su rival y saquea §100 monedas de su bolsa! "
                f"{oponente.mention}, siempre puedes vender tu dignidad para recuperar el oro perdido."
            )
    elif dado_rival > dado_jugador:
        if efecto == "elixir_bruma":
            # No restes monedas al jugador
            await database.update_user(oponente.id, {"coins": rival["coins"] + 100})
            resultado += f"{ctx.author.mention} usó el Elixir de la Bruma y no pierde monedas.\n"
        elif efecto == "hongo_abismo":
            # Ya se descontaron monedas al rival en la función
            await database.update_user(ctx.author.id, {"coins": jugador["coins"] - 100})
            resultado += f"{ctx.author.mention} usó el Hongo del Abismo.\n{oponente.mention} pierde §100 monedas aunque haya ganado.\n"
        else:
            await database.update_user(ctx.author.id, {"coins": jugador["coins"] - 100})
            await database.update_user(oponente.id, {"coins": rival["coins"] + 100})
        # ¿Jugador muerto?
        if jugador["coins"] - 100 <= 0:
            await database.delete_user(ctx.author.id)
            resultado += (
                f"\n{ctx.author.mention} ha perdido todas sus monedas y ha sido borrado de la historia. "
                "Deberá crear un nuevo perfil con `!elegir`."
            )
        else:
            resultado += (
                f"¡{oponente.mention} se alza victorioso y roba §100 monedas! "
                f"{ctx.author.mention}, quizás la suerte te sonría en tu próxima vida... o no."
            )
    else:
        # Empate
        resultado += (
            "¡Empate! Los dioses del azar se burlan de ambos y nadie gana ni pierde monedas. "
            "Quizás deberían dedicarse a la poesía."
        )

    await ctx.send(resultado)

@bot.command(name="tienda")
async def mostrar_tienda(ctx):
    intro = obtener_dialogo("tienda_intro")
    mensaje = f"{intro}\n\n"
    for i, obj in enumerate(OBJETOS_TIENDA, 1):
        mensaje += f"{i}. **{obj['nombre']}** (§{obj['precio']}): {obj['descripcion']}\n"
    mensaje += "\nUsa `!comprar <número>` para adquirir un objeto."
    await ctx.send(mensaje)

@bot.command(name="comprar")
async def comprar_objeto(ctx, numero: int):
    user = await database.read_user(ctx.author.id)
    if not user:
        await ctx.send("Debes tener un perfil antes de comprar. Usa `!elegir` para crearlo.")
        return
    if numero < 1 or numero > len(OBJETOS_TIENDA):
        await ctx.send("Ese objeto no existe en la tienda. Usa `!tienda` para ver las opciones.")
        return
    objeto = OBJETOS_TIENDA[numero - 1]
    coins = user.get("coins", 0)
    if coins < objeto["precio"]:
        await ctx.send(obtener_dialogo("compra_fallo"))
        return
    nuevo_inventario = user.get("inventory", []) + [objeto["nombre"]]
    await database.update_user(ctx.author.id, {
        "coins": coins - objeto["precio"],
        "inventory": nuevo_inventario
    })
    await ctx.send(obtener_dialogo("compra_exito", objeto=objeto["nombre"]))

# Uso de objetos en duelo
async def aplicar_objeto_duelo(ctx, user, oponente, dado_user, dado_oponente):
    inventario = user.get("inventory", [])
    efecto = None
    mensaje = ""

    especiales = [nombre for nombre in OBJETOS_ESPECIALES if nombre in inventario]
    if especiales:
        objeto_usado = random.choice(especiales)
        inventario.remove(objeto_usado)
        await database.update_user(ctx.author.id, {"inventory": inventario})
    else:
        return None, ""

    if objeto_usado == "Elixir de la Bruma" and dado_user < dado_oponente:
        efecto = "elixir_bruma"
        mensaje = obtener_dialogo("duelo_objeto_elixir_bruma", user=ctx.author.mention)
    elif objeto_usado == "Hongo del Abismo" and dado_user < dado_oponente:
        efecto = "hongo_abismo"
        rival_coins = oponente.get("coins", 0)
        new_rival_coins = max(1, rival_coins - 100)
        await database.update_user(oponente["user_id"], {"coins": new_rival_coins})
        mensaje = obtener_dialogo("duelo_objeto_hongo_abismo", user=ctx.author.mention, enemigo=oponente.mention)
    elif objeto_usado == "Pizza con yogur" and dado_user > dado_oponente:
        efecto = "pizza_yogur"
        coins = user.get("coins", 0)
        await database.update_user(ctx.author.id, {"coins": coins * 3})
        mensaje = obtener_dialogo("duelo_objeto_pizza_yogur", user=ctx.author.mention)
    return efecto, mensaje


bot.run(DISCORD_TOKEN)