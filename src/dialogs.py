import random

DIALOGOS = {
    "cambiar_raza_exito": [
        "{user}, tras un oscuro ritual, ahora eres {raza}. Te quedan §{coins} monedas y una nueva identidad que pronto lamentarás.",
        "{user}, los dioses se burlan mientras cambias de piel y te conviertes en {raza}. Solo te quedan §{coins} monedas.",
        "{user}, tu alma ha sido retorcida y renaces como {raza}. ¿Valió la pena perder §200 monedas?"
    ],
    "cambiar_raza_muerte": [
        "{user}, el ritual para cambiar de raza ha drenado tus últimas monedas y tu alma. Has muerto y tu existencia ha sido borrada. Usa !elegir para renacer... si te atreves.",
        "{user}, tu ambición te ha llevado a la tumba. Sin monedas, sin futuro. Solo te queda empezar de nuevo con !elegir.",
        "{user}, el precio de la transformación fue tu vida. Renace si tienes el valor."
    ],
    "cambiar_clase_exito": [
        "{user}, tras un entrenamiento mortal, ahora eres {clase}. Te quedan §{coins} monedas y una nueva profesión que probablemente te mate más rápido.",
        "{user}, cambias de clase como quien cambia de tumba. Ahora eres {clase} y te quedan §{coins} monedas.",
        "{user}, tu destino da un giro oscuro: eres {clase}. ¿Sobrevivirás esta vez?"
    ],
    "cambiar_clase_muerte": [
        "{user}, tu intento de cambiar de clase ha vaciado tus arcas y tu existencia. Has muerto y deberás crear un nuevo perfil con !elegir.",
        "{user}, la avaricia te llevó a la ruina. Sin monedas, sin clase, sin vida.",
        "{user}, tu historia termina aquí... pero puedes renacer con !elegir."
    ],
    "duelo_inicio": [
        "{retador} desafía a {oponente} a un duelo mortal. Los dados decidirán quién ríe y quién será olvidado.",
        "En la arena de la desesperación, {retador} mira a {oponente} y lanza el guante. ¿Quién sobrevivirá?",
        "{retador} y {oponente} se enfrentan bajo la mirada burlona de los dioses. Que los dados hablen."
    ],
    "duelo_gana_retador": [
        "¡{retador} aplasta a {oponente} y saquea 100 monedas de su bolsa! {oponente}, siempre puedes vender tu dignidad para recuperar el oro perdido.",
        "La suerte sonríe a {retador}, que se lleva 100 monedas y deja a {oponente} contando sus cicatrices.",
        "{retador} celebra la victoria mientras {oponente} lamenta su existencia y su pobreza."
    ],
    "duelo_gana_oponente": [
        "¡{oponente} se alza victorioso y roba 100 monedas! {retador}, quizás la suerte te sonría en tu próxima vida... o no.",
        "{oponente} ríe mientras recoge las monedas de {retador}, que ahora debe replantearse sus decisiones.",
        "El destino favorece a {oponente}, que se lleva el oro y deja a {retador} en la miseria."
    ],
    "duelo_empate": [
        "¡Empate! Los dioses del azar se burlan de ambos y nadie gana ni pierde monedas. Quizás deberían dedicarse a la poesía.",
        "Ambos caen en la mediocridad: empate. Las monedas siguen en sus bolsillos, pero la vergüenza es compartida.",
        "El duelo termina sin gloria ni oro. ¿Para esto vinieron al mundo?"
    ],
    "duelo_muerte": [
        "{muerto} ha perdido todas sus monedas y su alma ha sido reclamada. Deberá forjar un nuevo destino con !elegir.",
        "El precio de la derrota fue la vida: {muerto} desaparece del mundo de los vivos. Solo queda renacer.",
        "Sin monedas, sin alma, sin futuro. {muerto} debe empezar de nuevo si quiere volver a sufrir."
    ],
    "perfil_vacio": [
        "Tu existencia es tan vacía como tu perfil. Usa !elegir para comenzar tu trágica aventura.",
        "No tienes historia, no tienes gloria. Usa !elegir y acepta tu destino.",
        "Eres un alma errante sin propósito. Crea tu perfil con !elegir y abraza el sufrimiento."
    ],
    "perfil": [
        "**Perfil de {user}**\nRaza: **{raza}**\nClase: **{clase}**\nMonedas: **§{coins}**\nInventario: {inventario}",
        "{user}, tu miserable existencia es:\nRaza: {raza}\nClase: {clase}\nMonedas: §{coins}\nInventario: {inventario}",
        "Los dioses se apiadan de ti, {user}:\nRaza: {raza}\nClase: {clase}\nMonedas: §{coins}\nInventario: {inventario}"
    ],
    "elegir_exito": [
        "{user}, los dioses se ríen mientras eliges:\nRaza: **{raza}**\nClase: **{clase}**\nTu destino está sellado... por ahora.",
        "{user}, has sellado tu destino: {raza} y {clase}. Que la tragedia comience.",
        "{user}, tu historia comienza con una mala decisión: {raza} y {clase}."
    ],
    "elegir_cambio": [
        "{user}, has cambiado tu senda a:\nRaza: **{raza}**\nClase: **{clase}**\n¿Crees que así evitarás la tragedia? Ingenuo.",
        "{user}, intentas burlar al destino cambiando de raza y clase. No funcionará.",
        "{user}, tu nueva vida será tan desafortunada como la anterior."
    ],
    "error_razas": [
        "Ese número de raza no existe en este plano. Usa !razas para ver las opciones.",
        "Intentas elegir una raza que ni los dioses conocen. Usa !razas.",
        "Tu elección de raza es tan válida como un dragón vegetariano. Usa !razas."
    ],
    "error_clases": [
        "Esa letra de clase solo existe en las pesadillas de los bardos. Usa !clases para ver las opciones.",
        "¿Clase secreta? No existe. Usa !clases.",
        "Intentas elegir una clase prohibida. Usa !clases."
    ],
    "cambiar_raza_misma": [
        "{user}, ¿crees que cambiar a la misma raza te hará más interesante? Los dioses bostezan ante tu falta de imaginación.",
        "{user}, intentas cambiar a la raza que ya tienes. El universo se ríe de tu redundancia.",
        "{user}, cambiar a la misma raza es como pedirle a la muerte una segunda oportunidad... y que te la niegue."
    ],
}

def obtener_dialogo(clave, **kwargs):
    frases = DIALOGOS.get(clave, ["..."])
    frase = random.choice(frases)
    return frase.format(**kwargs)