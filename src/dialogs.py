import random

DIALOGOS = {
    "cambiar_raza_exito": [
        "{user}, tras un oscuro ritual, ahora eres {raza}.\nTe quedan **§{coins}** monedas y una nueva identidad que pronto lamentarás.",
        "{user}, los dioses se burlan mientras cambias de piel y te conviertes en {raza}.\nSolo te quedan **§{coins}** monedas.",
        "{user}, tu alma ha sido retorcida y renaces como {raza}.\n¿Valió la pena perder **§200** monedas?"
    ],
    "cambiar_raza_muerte": [
        "{user}, el ritual para cambiar de raza ha drenado tus últimas monedas y tu alma.\nHas muerto y tu existencia ha sido borrada.\nUsa !elegir para renacer... si te atreves.",
        "{user}, tu ambición te ha llevado a la tumba.\nSin monedas, sin futuro.\nSolo te queda empezar de nuevo con !elegir.",
        "{user}, el precio de la transformación fue tu vida.\nRenace si tienes el valor."
    ],
    "cambiar_raza_misma": [
        "{user}, ¿crees que cambiar a la misma raza te hará más interesante?\nLos dioses bostezan ante tu falta de imaginación.",
        "{user}, intentas cambiar a la raza que ya tienes.\nEl universo se ríe de tu redundancia.",
        "{user}, cambiar a la misma raza es como pedirle a la muerte una segunda oportunidad...\ny que te la niegue."
    ],
    "cambiar_clase_exito": [
        "{user}, tras un entrenamiento mortal, ahora eres {clase}.\nTe quedan **§{coins}** monedas y una nueva profesión que probablemente te mate más rápido.",
        "{user}, cambias de clase como quien cambia de tumba.\nAhora eres {clase} y te quedan **§{coins}** monedas.",
        "{user}, tu destino da un giro oscuro: eres {clase}.\n¿Sobrevivirás esta vez?",
        "{user}, has cambiado tu senda a {clase}.\n¿Crees que así evitarás la tragedia? ¡Qué ingenuidad!."
    ],
    "cambiar_clase_muerte": [
        "{user}, tu intento de cambiar de clase ha vaciado tus arcas y tu existencia.\nHas muerto y deberás crear un nuevo perfil con !elegir.",
        "{user}, la avaricia te llevó a la ruina.\nSin monedas, sin clase, sin vida.",
        "{user}, tu historia termina aquí...\npero puedes renacer con !elegir."
    ],
    "cambiar_clase_misma": [
        "{user}, ya tienes esa clase.\n¿Esperabas que algo cambiara? Solo tu decepción lo hará.",
        "{user}, cambiar a la misma clase es tan útil como un mago sin hechizos.",
        "{user}, los dioses te observan y deciden ignorar tu intento de cambio redundante.",
        "{user}, tu intento de cambiar de clase es tan emocionante como ver crecer el moho en una mazmorra.",
        "{user}, la monotonía te consume:\nsigues siendo la misma clase, y los bardos ni siquiera lo cantarán."
    ],
    "duelo_inicio": [
        "{retador} desafía a {oponente} a un duelo mortal.\nLos dados decidirán quién ríe y quién será olvidado.",
        "En la arena de la desesperación, {retador} mira a {oponente} y lanza el guante.\n¿Quién sobrevivirá?",
        "{retador} y {oponente} se enfrentan bajo la mirada burlona de los dioses.\nQue los dados hablen."
    ],
    "duelo_gana_retador": [
        "¡{retador} aplasta a {oponente} y saquea 100 monedas de su bolsa!\n{oponente}, siempre puedes vender tu dignidad para recuperar el oro perdido.",
        "La suerte sonríe a {retador}, que se lleva 100 monedas\ny deja a {oponente} contando sus cicatrices.",
        "{retador} celebra la victoria mientras {oponente} lamenta su existencia y su pobreza."
    ],
    "duelo_gana_oponente": [
        "¡{oponente} se alza victorioso y roba 100 monedas!\n{retador}, quizás la suerte te sonría en tu próxima vida... o no.",
        "{oponente} ríe mientras recoge las monedas de {retador},\nque ahora debe replantearse sus decisiones.",
        "El destino favorece a {oponente}, que se lleva el oro\ny deja a {retador} en la miseria."
    ],
    "duelo_empate": [
        "¡Empate! Los dioses del azar se burlan de ambos\ny nadie gana ni pierde monedas.\nQuizás deberían dedicarse a la poesía.",
        "Ambos caen en la mediocridad: empate.\nLas monedas siguen en sus bolsillos, pero la vergüenza es compartida.",
        "El duelo termina sin gloria ni oro.\n¿Para esto vinieron al mundo?"
    ],
    "duelo_muerte": [
        "{muerto} ha perdido todas sus monedas y su alma ha sido reclamada.\nDeberá forjar un nuevo destino con !elegir.",
        "El precio de la derrota fue la vida:\n{muerto} desaparece del mundo de los vivos.\nSolo queda renacer.",
        "Sin monedas, sin alma, sin futuro.\n{muerto} debe empezar de nuevo si quiere volver a sufrir."
    ],
    "perfil_vacio": [
        "Tu existencia es tan vacía como tu perfil.\nUsa !elegir para comenzar tu trágica aventura.",
        "No tienes historia, no tienes gloria.\nUsa !elegir y acepta tu destino.",
        "Eres un alma errante sin propósito.\nCrea tu perfil con !elegir y abraza el sufrimiento."
    ],
    "perfil": [
        "Eres un **{raza}** y formas parte del gremio de los **{clase}**.\nEn tu bolsa guardas **§{coins}** monedas\nInventario: {inventario}.",
        "{user}, tu linaje es **{raza}** y perteneces al gremio de los **{clase}**.\nTus riquezas suman **§{coins}** monedas\nInventario: {inventario}.",
        "Como buen **{raza}** del gremio de los **{clase}**, llevas **§{coins}** monedas en la bolsa.\nInventario: {inventario}."
    ],
    "perfil_inventario_vacio": [
        "Eres un **{raza}** del gremio de los **{clase}**.\nEn tu bolsa guardas **§{coins}** monedas,\npero tu inventario está tan vacío como tus esperanzas.",
        "{user}, tu linaje es **{raza}** y perteneces al gremio de los **{clase}**.\nTus riquezas suman **§{coins}** monedas,\npero tu inventario no tiene nada digno de mencionar.",
        "Como buen **{raza}** del gremio de los **{clase}**, llevas **§{coins}** monedas en la bolsa,\ny un inventario tan vacío que hasta los ladrones lo ignoran."
    ],
    "elegir_exito": [
        "{user}, los dioses se ríen mientras eliges:\nRaza: **{raza}**\nClase: **{clase}**\nTu destino está sellado... por ahora.",
        "{user}, has sellado tu destino:\n{raza} y {clase}.\nQue la tragedia comience.",
        "{user}, tu historia comienza con una mala decisión:\n{raza} y {clase}."
    ],
    "elegir_cambio": [
        "{user}, has cambiado tu senda a:\nRaza: **{raza}**\nClase: **{clase}**\n¿Crees que así evitarás la tragedia? Ingenuo.",
        "{user}, intentas burlar al destino cambiando de raza y clase.\nNo funcionará.",
        "{user}, tu nueva vida será tan desafortunada como la anterior."
    ],
    "error_razas": [
        "Ese número de raza no existe en este plano.\nUsa !razas para ver las opciones.",
        "Intentas elegir una raza que ni los dioses conocen.\nUsa !razas.",
        "Tu elección de raza es tan válida como un dragón vegetariano.\nUsa !razas."
    ],
    "error_clases": [
        "Esa letra de clase solo existe en las pesadillas de los bardos.\nUsa !clases para ver las opciones.",
        "¿Clase secreta? No existe.\nUsa !clases.",
        "Intentas elegir una clase prohibida.\nUsa !clases."
    ],
}

def obtener_dialogo(clave, **kwargs):
    frases = DIALOGOS.get(clave, ["..."])
    frase = random.choice(frases)
    return frase.format(**kwargs)