# -*- coding: utf-8 -*-
"""Genera index.html del E-Book 'Sanando la desconexión emocional en pareja' (Johanna Daza)."""
import html, re, json

TITLE = "Sanando la desconexión emocional en pareja"
E = html.escape

# ------------------------------------------------------------------ imágenes de banco (placeholders)
STOCK = []
CLIENT = []
CAM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 8a2 2 0 0 1 2-2h2l1.5-2h7L17 6h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="13" r="3.6"/></svg>'

def ph(desc, search, style="", cls="", client=False):
    if client:
        n = len(CLIENT) + 1
        CLIENT.append((n, desc, search))
        src, lab, em = f"assets/client/foto-{n:02d}.jpg", f"Foto de Johanna {n:02d}", E(search)
    else:
        n = len(STOCK) + 1
        STOCK.append((n, desc, search))
        src, lab, em = f"assets/stock/img-{n:02d}.jpg", f"Imagen de banco {n:02d}", "Buscar: " + E(search)
    return (f'<figure class="ph {cls}" style="{style}"><img src="{src}" alt="{E(desc)}" onerror="this.remove()">'
            f'<div class="ph-in">{CAM}<b>{lab}</b><span>{E(desc)}</span><em>{em}</em></div></figure>')

# ------------------------------------------------------------------ contenido
CAUSAS = [
 ("Maltrato físico o emocional", None,
  "Los golpes, empujones, jalones, forzar contacto físico, así como los gritos, burlas, humillaciones, ofensas, chantajes, castigos emocionales o ignorar a la pareja no solo hieren: desorganizan la capacidad de vincularse. El maltrato desregula el sistema nervioso, altera la percepción de seguridad en el vínculo y genera distancia afectiva, incluso cuando la persona intenta seguir conectada.",
  "Él se burla cuando ella expresa algo. Ella deja de hablar."),
 ("Promesas incumplidas", None,
  "Prometer y no cumplir erosiona la confianza, que es el pegamento emocional de la relación. La pareja empieza a sentir que no puede contar con el otro. Se instala la duda, la frustración y la sensación de abandono. La palabra pierde valor y con ella, el vínculo.",
  "Ella promete: “mañana lo hacemos” y nunca pasa. Él deja de creer."),
 ("Resentimiento", None,
  "Es una herida no atendida que se forma cuando hay dolor repetido sin reparación. Genera frialdad, indiferencia y distancia emocional.",
  "Él llega tarde otra vez. Ella dice: “tranquilo, ya estoy acostumbrada”."),
 ("Invalidación de los sentimientos", "Es decir, minimizar o ignorar las emociones del otro.",
  "La persona percibe que sentir está mal. Se retrae, deja de compartir y se vuelve emocionalmente inaccesible. Se instala un clima de soledad dentro de la relación.",
  "Uno dice: “me dolió”. El otro responde: “exageras”."),
 ("Victimización constante", "Lo cual significa no reconocer las propias responsabilidades y culpabilizar al otro.",
  "Cuando uno siempre es la víctima, el otro siempre es el culpable. Se bloquea la responsabilidad afectiva. La conversación se vuelve imposible. La pareja se cansa de cargar con culpas que no le corresponden y se desconecta.",
  "Ella quiere hablar de un problema. Él dice: “ya vas a empezar a atacarme, siempre soy el malo”."),
 ("Monotonía", "Hacer siempre lo mismo.",
  "No es solo “hacer siempre lo mismo”, sino dejar de poner intención y novedad en el vínculo. Cuando esto ocurre, la pareja entra en piloto automático y la desconexión emocional se vuelve inevitable: menos curiosidad, menos sorpresa, menos deseo, menos elección consciente.",
  "Uno o los dos sienten que todos los días son iguales. Cero sorpresas ni chispa."),
 ("Asumir lo que el otro piensa o siente", None,
  "Cuando inferimos en lugar de indagar, se generan malentendidos y expectativas irreales. La pareja deja de preguntar y comienza a interpretar. Poco a poco, la relación se llena de suposiciones en lugar de verdades.",
  "Ella cree que él está molesto. Él cree que ella no quiere hablar. Nadie pregunta."),
 ("Estrés sostenido", None,
  "El estrés sostenido consume la energía emocional disponible. La persona entra en “modo supervivencia”. Se vuelve irritable, distante o desconectada tanto de la pareja como de sí mismo.",
  "Ella llega agotada. Él intenta hablar. Ella responde de manera fría y evitativa porque está cansada."),
 ("Heridas del pasado", None,
  "Los traumas no sanados suelen influir en el presente. La pareja reacciona desde el miedo y activa mecanismos de defensa, como evitar, alejarse o controlar. En estos casos, la desconexión emocional puede ser una forma de protegerse del dolor no gestionado.",
  "Él tarda en responder. Ella siente abandono."),
 ("La falta de tiempo de calidad", None,
  "Cuando no hay espacios reales para encontrarse, el otro empieza a sentirse acompañado solo en lo funcional. Con el tiempo, esta ausencia de presencia afectiva genera distancia, irritabilidad y la dolorosa sensación de que el otro está… pero no está para mí.",
  "Conviven, pero no conversan ni hay momentos para ellos."),
 ("Exceso de tecnología", None,
  "Cuando el celular se convierte en un tercero en la relación, se reduce el contacto visual, la escucha y la presencia. La pareja siente que “estás, pero no estás” e incluso puede interpretar esa ausencia como desinterés, lo que erosiona la sensación de prioridad y pertenencia.",
  "Uno habla. El otro mira el celular."),
 ("Vivir solo el rol de papá o trabajador", None,
  "Cuando la identidad se reduce a un rol, la pareja queda en segundo plano. Se descuida el rol de amante, compañero y cómplice. La relación se vuelve funcional, no afectiva, donde se coordina, pero no se conecta. Con el tiempo, esta dinámica genera distancia, resentimiento silencioso y la sensación de que la pareja existe solo como equipo parental.",
  "Solo hablan de trabajo o de hijos. Nunca de ellos."),
 ("No hacer sentir amado al otro", None,
  "Cuando no se expresa de ninguna manera el amor: contacto, miradas, palabras, detalles, acciones o abrazos, la persona afectada empieza a sentirse invisible, poco importante o emocionalmente solo.",
  "Al llegar y al salir, él pasa por su lado sin tocarla; ella tampoco se acerca."),
]

SINTOMAS = [
 ("Sentirse solo incluso estando juntos", "Hay presencia física, pero no emocional. La persona experimenta una sensación interna de desconexión, como si el otro no estuviera disponible para escuchar, acompañar o sostener."),
 ("Puede haber irritabilidad o apatía constante", "Aparecen reacciones emocionales desproporcionadas o una falta de interés general hacia la relación."),
 ("Conductas de desconfianza", "Surgen dudas, sospechas o interpretaciones negativas sobre las acciones del otro. La seguridad emocional se debilita y puede aumentar la vigilancia o la necesidad de control."),
 ("Más conductas de individualismo que de colectivismo", "Cada uno empieza a priorizar sus actividades, decisiones y necesidades por encima del vínculo. Se pierde la sensación de equipo y disminuye la construcción conjunta."),
 ("Conversaciones superficiales o dirigidas solo a las responsabilidades del hogar, los hijos o el negocio", "La comunicación se limita a temas prácticos o logísticos. No hay intercambio emocional, vulnerabilidad ni conversaciones que profundicen en el estado interno de cada uno."),
 ("Poca o nula expresión de afecto", "Se observa una disminución evidente de gestos afectivos: el contacto físico se reduce, las miradas pierden calidez y las palabras cariñosas van desapareciendo. La relación se vuelve emocionalmente plana."),
]

CONSEC = [
 ("Sentirse rechazado", "Cuando hay desconexión emocional la persona puede sentirse: no deseada, no mirada, no tomada en cuenta o desplazada. Incluso puede dudar de su valor o de su atractivo."),
 ("Sensación de vacío o tristeza", "Ante la desconexión emocional la persona puede experimentar una sensación de duelo o pérdida, lo cual genera una profunda sensación de tristeza."),
 ("Sentirse solo o abandonado", "Cuando hay desconexión emocional, uno o ambos miembros pueden sentir que el otro se fue, lo abandonó, no está emocionalmente ni es un lugar seguro. Es vivir una soledad acompañada: se vive al lado de alguien que ya no está emocionalmente presente."),
 ("Querer huir o sentirse muy ansioso", "La desconexión emocional suele ser tan dolorosa que el que lo siente puede querer huir o volverse muy ansioso por los miedos que se detonan a partir de allí."),
 ("Insomnio", "Si hay desconexión emocional, hay un malestar que puede hacer que la persona no logre conciliar el sueño ni descansar por pensar en aquello que le duele, le angustia o le molesta."),
 ("Rumiación", "Producto del malestar de la desconexión emocional se puede activar la rumiación (pensar repetitivamente en algo sin avanzar y con dificultad para parar dichos pensamientos). La persona queda atrapada en un ciclo mental que busca desesperadamente sentido y claridad, aunque no lo logre."),
]

TEST1 = [
 ("Maltrato emocional o físico", ["¿Alguno de los dos usa gritos, burlas, humillaciones, ofensas, indiferencia o castigos emocionales?", "¿Hay presencia de golpes, empujones, jalones o forzar contacto físico?"]),
 ("Promesas incumplidas", ["¿El otro promete cosas que no cumple o incluso tú mismo?", "¿Hay desconfianza de la palabra del otro?"]),
 ("Resentimiento acumulado", ["¿Hay heridas repetidas que nunca se hablaron ni repararon?", "¿Alguno responde ante determinadas situaciones con frialdad, indiferencia o distancia?"]),
 ("Invalidación emocional", ["¿Alguno minimiza lo que el otro siente (“exageras”, “no es para tanto”)?", "¿Alguno ignora las emociones del otro?", "¿Alguno dejó de compartir emociones por miedo a ser invalidado?"]),
 ("Victimización constante", ["¿Alguno se coloca constantemente en la posición de víctima y culpa al otro de todo?", "¿Las conversaciones se vuelven imposibles porque alguno o ambos no asumen responsabilidades?"]),
 ("Monotonía y piloto automático", ["¿Sienten que todos los días son iguales y sin intención afectiva?", "¿La relación perdió novedad, chispa o curiosidad?"]),
 ("Suponer en vez de preguntar", ["¿Interpretan lo que el otro siente sin verificarlo?", "¿Se generan malentendidos porque alguno no pregunta directamente?"]),
 ("Estrés sostenido", ["¿Alguno está tan agotado que responde frío, distante o irritable?", "¿El cansancio está ocupando el espacio emocional de la relación?"]),
 ("Heridas del pasado", ["¿Reaccionan desde miedos antiguos (abandono, traición, rechazo)?", "¿Situaciones pequeñas activan emociones muy intensas?"]),
 ("Falta de tiempo de calidad", ["¿Conviven, pero conversan poco?", "¿Les faltan compartir momentos a solas de calidad (de real conexión)?", "¿Sienten que están juntos solo en lo funcional?"]),
 ("Exceso de tecnología", ["¿El celular interrumpe conversaciones, miradas o momentos importantes?", "¿Alguno siente que el otro “está, pero no está”?"]),
 ("Vivir solo el rol de papá o trabajador", ["¿Solo hablan de hijos, trabajo o pendientes?", "¿El rol de pareja quedó relegado o desapareció?"]),
 ("No hacer sentir amado al otro", ["¿Han desaparecido las miradas, el contacto, los detalles, las acciones amorosas o las palabras afectivas?", "¿Alguno se siente invisible, poco importante o emocionalmente solo?"]),
]

TEST2 = [
 ("Poca o nula expresión de afecto", ["¿Han disminuido los gestos afectivos como miradas cálidas, contacto físico o palabras cariñosas?"]),
 ("Sentirse solo incluso estando juntos", ["¿Alguno se siente emocionalmente solo aunque compartan espacio o actividades?"]),
 ("Irritabilidad o apatía constante", ["¿Hay irritación frecuente o falta de interés hacia la relación de forma sostenida?"]),
 ("Conductas de desconfianza", ["¿Han aparecido dudas, sospechas o interpretaciones negativas sobre el otro?"]),
 ("Más individualismo que colectivismo", ["¿Cada uno prioriza sus actividades y decisiones por encima del “nosotros”?"]),
 ("Conversaciones superficiales o solo logísticas", ["¿Las conversaciones se limitan a responsabilidades, pendientes o temas prácticos, sin profundidad emocional?"]),
]

TEST3 = [
 ("Sensación de desconexión emocional", ["¿Identificas si hay desconexión emocional?", "¿Qué has sentido a raíz de la desconexión: sensación de rechazo, sensación de tristeza, insomnio, rumiación, ansiedad, ganas de huir o sensación de abandono?"]),
 ("Mapa de conductas", ["¿Qué haces cuando sientes la desconexión emocional: te alejas o buscas excesivamente?", "¿Ante la desconexión haces reclamos agresivamente o te apagas y buscas complacer y ceder?", "¿Has conversado asertivamente sobre la desconexión emocional?"]),
 ("Línea del tiempo de desconexión emocional", ["¿Cuándo comenzó la desconexión emocional?", "¿Qué eventos intensificaron la desconexión emocional?", "¿Qué intentos de reparación hubo?"]),
 ("Momentos de conexión", ["¿Qué momentos de conexión recuerdas?", "¿Qué los mantenía conectados antes?"]),
]

EJEMPLOS = [
 "Uno intenta hablar y el otro responde con distracción, monosílabos o distancia. La sensación dominante es de soledad dentro del vínculo.",
 "Cualquier comentario cotidiano genera molestia o indiferencia. Las reacciones son desproporcionadas o ausentes, creando un clima emocional incómodo.",
 "Cada uno prioriza sus actividades y decisiones sin considerar para nada al otro. Las agendas se separan, no hay tiempo para ambos y la sensación de equipo desaparece.",
 "El contacto físico disminuye, las miradas pierden calidez y las palabras afectivas desaparecen. La relación se siente fría y distante.",
 "La comunicación se reduce a trabajo, pagos, hijos o responsabilidades del hogar. No hay intercambio emocional ni exploración del mundo interno del otro. Todo se vuelve práctico y funcional.",
]

HERR_A = [
 "Lo más importante es identificar qué nos desconecta y cómo nos sentimos con eso.",
 "Diseñar conversaciones donde practiquemos la escucha empática y asertiva. Lo cual implica poner atención plena, sin planear respuestas, sin interrumpir, sin decir sarcasmos, sin defenderse, solo con la intención de entender antes de querer ser entendido.",
 "Hablar sin acusar, más bien haciendo peticiones claras.",
 "Es importante entender que la reconexión emocional será un proceso de compromiso diario en el que nos recuperaremos con pequeños actos consistentes.",
]
HERR_B = [
 ("Maltrato", "Si denotan que en la relación hay maltrato de algún tipo, es importante: establecer límites; plantear conductas negociables y no negociables; crear pautas de seguridad claras para detener cualquier tipo de agresión; trabajar en la gestión emocional de cada uno y muchas veces es necesario hacer terapia individual y de pareja."),
 ("Promesas incumplidas", "Ante la confianza rota por promesas incumplidas, es vital: restaurar la coherencia planteándose pequeñas promesas que sí se cumplan; hacer de un hábito: la previa comunicación, la restauración y la negociación para garantizar el cumplimiento de las promesas establecidas; y practicar la responsabilidad y el respeto por tu palabra."),
 ("Resentimiento", "Cuando el resentimiento es el protagonista, se debe abrir el espacio para la reparación emocional. En tanto, herramientas como: tener conversaciones donde se nombre la herida, se hable del impacto de la misma y se acuerden cambios, son muy importantes, así como escribir cartas sobre todo lo que dolió, practicar el perdón hacia el otro y el auto-perdón de ser necesario. Evidentemente la otra persona debe no solo pedir perdón, sino garantizar cuidar al otro y hacer cambios perdurables en el tiempo."),
 ("Invalidación emocional", "Cuando la invalidación emocional es lo que nos desconecta, se deben aplicar técnicas para restaurar la legitimidad del sentir en el otro. Prácticas como: escuchar empáticamente y acompañar la emoción del otro sin juzgar, minimizar, interrumpir ni corregir. Decir frases como “te entiendo”, “te comprendo” y “cómo puedo ayudarte”."),
 ("Victimización constante", "Si es la victimización constante lo que nos ha desconectado, el objetivo es activar la responsabilidad afectiva. Identificar en qué situaciones específicas alguno o ambos culpan al otro de todo y no asumen su cuota de responsabilidad. Es crucial desarrollar el hábito de responsabilidad compartida, donde cada cual revisa cómo contribuyó al conflicto, es decir qué parte de responsabilidad corresponde a cada uno. Todo lo anterior para abrazar el aprendizaje, marcar pautas y seguir adelante."),
 ("Monotonía", "Ante la monotonía, que es tan común en pareja, se debe reactivar la novedad. Para ello, se debe conscientemente introducir pequeños cambios cada semana (gestos, mensajes, invitaciones); visitar lugares nuevos, crear proyectos y metas siendo un equipo, hacer actividades educativas o recreativas juntos, en fin, tener la intención y el hábito de no dejar de sorprenderse, conocerse y elegirse."),
 ("Suponer en vez de preguntar", "Una clave de oro en pareja debe ser: “antes de asumir algo, voy a preguntar”, dicho en otras palabras, antes de hacernos películas catastróficas y negativas en la cabeza se debe conversar con el otro para validar, clarificar, entender y comprender mejor. Lo anterior siempre debe hacerse desde la mejor actitud y no de forma acusadora ni reactiva."),
 ("Estrés sostenido", "Gestionar el estrés cotidiano hará que se tenga más energía vital disponible para invertir en la pareja. Hay que expresar al otro cuando estamos estresados pero a su vez buscar la manera de regularnos (estirarse, ejercitarse, hablar, caminar, delegar, coordinar, buscar ayuda profesional…)."),
 ("Heridas del pasado", "Sanar las heridas del pasado es un acto de responsabilidad contigo y con el otro. Hay que observar esos gatillos emocionales, situaciones pasadas dolorosas no superadas o patrones que estés repitiendo, ya que ese es el primer paso para levantar la mano y decir: “necesito ayuda profesional” y para conscientemente dejar de trasladar tus heridas al vínculo actual. Además de reconocerlas, hay que comunicarlas y crear nuevas experiencias en conjunto."),
 ("Tiempo de calidad", "El tiempo de calidad es un alimento que nutre el vínculo. Y en ese sentido, más que cantidad importa la calidad, el estar realmente presente para el otro cuando estamos juntos. Trata de no ser compañeros de hogar simplemente sino de compartir, conectar, conversar profundamente, disfrutar momentos juntos, regalarnos una cita semanal fuera de casa, mandarnos mensajes con lindas frases diariamente, hacer caminatas nocturnas, charlar de nosotros mismos antes de dormir o compartir el café de las mañanas. Se trata de abrir los espacios y hacer que las cosas sucedan."),
 ("Exceso de tecnología", "Vivimos en un mundo donde el exceso de tecnología está a la orden del día. Y muchas veces, eso más que unir a la pareja, los puede desconectar. Siendo así, se debe recuperar la atención y la presencia. En tanto, son vitales acciones como: no usar los teléfonos durante las comidas, momentos o conversaciones importantes; establecer momentos al día donde no esté presente el teléfono y solo sea un instante nuestro; ganar terreno respecto a mirarnos, abrazarnos y tocarnos más; y usar la tecnología como aliada para conectar cuando no esté con mi pareja con un mensaje, música o video afectivo."),
 ("Rol de papá o trabajador", "La falta de equilibrio entre los roles de un ser humano puede sabotear una relación. A menudo escucho en consulta que el rol de pareja se desdibuja o desmejora por solo vivir el rol de padre o trabajador. Si queremos que esto se solucione, debemos entender que tener un vínculo de pareja sano implica tiempo y dedicación. Hay que establecer límites entre cada rol y hacer un plan para de nuevo habitar la vida de pareja con acciones como: planear salidas a solas; tener conversaciones diarias sobre nosotros como seres humanos más allá de ser papás o profesionales; establecer aventuras y proyectos juntos; recuperar el erotismo y la sexualidad."),
 ("No sentirse amado", "Otro tema recurrente del que se quejan en consulta es “no me siento amado”, y es que no conocer el lenguaje del amor del otro, generalmente genera conflicto. Entonces, hay que hacer un trabajo para identificar qué hace sentir amado al otro para poder expresar el amor al otro desde su lenguaje. En este punto yo recomiendo a las parejas con las que trabajo que lean el libro: <i>Los Cinco Lenguajes del Amor</i>, cuyo autor es Gary Chapman."),
]
HERR_C = [
 "Estar conectados emocionalmente implica cultivar diariamente intimidad, cercanía y complicidad. Para ello, menos es más. Porque los pequeños gestos constantes construyen grandes y sólidos resultados.",
 "Tener conversaciones constantes también nos permitirá chequear cómo estamos, qué nos falta, qué va maravillosamente bien, qué nos agradecemos y cómo nos hacemos cargo de las debilidades.",
 "Recuperar la conexión emocional es el primer paso para reavivar el erotismo y mejorar la sexualidad.",
]

# ------------------------------------------------------------------ piezas
pages = []   # cada item: dict(key, cls, body, section, dark, nofoot)

def add(body, key=None, cls="", section="", dark=False, nofoot=False):
    pages.append(dict(key=key, cls=cls, body=body, section=section, dark=dark, nofoot=nofoot))

def card(i, t, sub, p, ex=None, plain=False):
    s = f'<div class="sub">{E(sub)}</div>' if sub else ""
    e = f'<div class="ex"><b>Ejemplo</b><span>{E(ex)}</span></div>' if ex else ""
    no = "" if plain else f'<div class="no">{i:02d}</div>'
    return f'<div class="card">{no}<div><h3>{E(t)}</h3>{s}<p>{E(p)}</p>{e}</div></div>'

def cards(items, start=1, plain=False, examples=True):
    out = []
    for k, it in enumerate(items):
        if examples:
            t, sub, p, ex = it
            out.append(card(start + k, t, sub, p, ex, plain))
        else:
            t, p = it
            out.append(card(start + k, t, None, p, None, plain))
    return '<div class="cards">' + "".join(out) + '</div>'

def band(txt, dk=False):
    return f'<div class="band{" dk" if dk else ""}">{txt}</div>'

def opener(num, cap, img_html, title, sub=None, h=330):
    s = f'<div class="sub">{sub}</div>' if sub else ""
    return (f'<div class="opener-img" style="height:{h}px">{img_html}<div class="num">{num}</div><div class="cap">{cap}</div></div>'
            f'<div class="chead"><h2>{title}</h2>{s}</div>')

def photo(url, pos="center"):
    return f'<div class="photo-bg" style="position:absolute;inset:0;background-image:url({url});background-position:{pos}"></div>'

def phfull(desc, search, cls=""):
    return ph(desc, search, "position:absolute;inset:0", cls)

def test_groups(groups, start=1):
    out = []
    for gi, (g, qs) in enumerate(groups, start):
        rows = "".join(
            f'<div class="q"><div class="qt">{E(q)}</div><div class="yn"><label><input type="checkbox">SÍ</label><label><input type="checkbox">NO</label></div></div>'
            for q in qs)
        out.append(f'<div class="tg"><h4><i>{gi}</i>{E(g)}</h4>{rows}</div>')
    return "".join(out)

def reflect_groups(groups, start=1):
    out = []
    for gi, (g, qs) in enumerate(groups, start):
        rows = "".join(f'<div class="rq"><div class="qt">{E(q)}</div><div class="ln"></div><div class="ln"></div></div>' for q in qs)
        out.append(f'<div class="tg"><h4><i>{gi}</i>{E(g)}</h4>{rows}</div>')
    return "".join(out)

# ============ 1 PORTADA
add('<div class="bg"></div><div class="ct"><span class="s1">Sanando</span>'
    '<h1><span>la <s>Desconexión</s></span><br><span>emocional</span></h1><span class="s2">en pareja</span></div>'
    '<div class="tag">E-Book</div><img class="logo" src="assets/logo/johanna-blanco.png" alt="Johanna Daza">',
    key="cover", cls="cover dark", nofoot=True, dark=True)

# ============ 2 BIO
add('<div class="photo">' + ph("Retrato de Johanna Daza (vertical, fondo neutro, mirada cálida)", "retrato profesional de Johanna · reemplazar", "position:absolute;inset:0", "dk", client=True) + '</div>'
    '<div class="draft" style="left:370px;top:34px">Texto de relleno · editar</div>'
    '<div class="col"><span class="script">Conoce a la autora</span><h2>Johanna<br>Daza</h2>'
    '<div class="role">Asesora clínica de pareja</div>'
    '<p class="lead" style="font-size:17px">“Acompaño a las parejas a volver a mirarse, a hablarse y a elegirse, aun cuando el camino parezca largo.”</p>'
    '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Johanna es asesora clínica de pareja con formación en terapia vincular y una vocación clara: ofrecer herramientas humanas, claras y accesibles para quienes quieren reparar su relación.</p>'
    '<p>Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>'
    '<div class="stats"><div class="stat"><b>+10</b><span>años de experiencia</span></div><div class="stat"><b>+500</b><span>parejas acompañadas</span></div><div class="stat"><b>100%</b><span>enfoque humano</span></div></div>'
    '<img class="sign" src="assets/logo/johanna-color.png" alt="Johanna Daza"></div>',
    key="bio", cls="bio", section="")

# ============ 3 ÍNDICE (se completa luego)
add("{{TOC}}", key="toc", cls="toc", section="Contenido")

# ============ 4 INTRO
add('<div class="pad">'
    + ph("Pareja conversando frente a frente en una mesa, luz cálida de tarde", "couple talking at table warm light, couple coffee conversation", "height:300px;margin:-76px -92px 30px;flex:none")
    + '<span class="script" style="font-size:34px;line-height:1">Bienvenidos</span>'
    '<h2 style="font:800 44px/1.05 var(--sans);margin:2px 0 18px">Iniciemos…</h2>'
    '<p class="lead" style="margin-bottom:14px">Como asesora clínica de pareja, he mirado que el desafío más frecuente y también el más silencioso en las relaciones es la desconexión emocional.</p>'
    '<p>No aparece de golpe: se instala poco a poco, en gestos que dejan de ocurrir, en conversaciones que ya no suceden, en miradas que se vuelven escasas. Cuando no se atiende a tiempo, esta desconexión puede profundizarse hasta convertirse en una ruptura definitiva, aun entre personas que se aman.</p>'
    '<p>Este Ebook nace de mi experiencia acompañando a parejas en procesos terapéuticos y del profundo deseo de ofrecer una guía clara, humana y accesible sobre esta problemática. Aquí encontrarás una explicación sencilla de qué es la desconexión emocional, por qué ocurre, cuáles son sus síntomas, qué consecuencias tiene y qué herramientas básicas existen para comenzar a abordarla.</p>'
    '<p>A lo largo del texto encontrarás mini test, ejemplos prácticos y reflexiones guiadas que te permitirán identificar tu propio estado emocional dentro del vínculo, comprender el de tu pareja y comenzar a reconstruir la conexión afectiva desde un lugar más consciente y compasivo.</p>'
    '<p style="margin:0">Mi intención es que este documento sea un espacio amoroso, seguro, un punto de partida y una compañía en el camino hacia relaciones más presentes, más honestas y más conectadas.</p>'
    '</div>', key="intro", section="Bienvenida")

# ============ 5 CITA
add('<div class="bg"></div><div class="qt"><span class="script">Antes de empezar…</span>'
    '<h2>La conexión comienza cuando alguien se atreve a hablar…</h2><div class="s">…y alguien decide escuchar.</div></div>'
    '<img class="logo" src="assets/logo/johanna-blanco.png" alt="Johanna Daza">',
    key="quote", cls="quote dark", dark=True, nofoot=True)

# ============ 6 CAP 1
add('<div class="pad">'
    + opener("01", "Capítulo uno",
             '<div class="photo-bg" style="position:absolute;inset:0;background-image:url(assets/img/pareja-glitch.jpg);background-position:center 34%"></div>',
             "¿Qué es la <s>desconexión</s> emocional?", h=400)
    + '<p class="lead" style="font-size:20px;margin-bottom:20px">La desconexión emocional es un proceso gradual en el que uno o ambos miembros de la pareja se distancian y dejan de estar presente emocionalmente en la relación.</p>'
    '<p style="margin-bottom:16px">La persona está físicamente, pero puede no estar disponible, conectada ni involucrada a nivel afectivo.</p>'
    '<div class="estar">'
    '<div class="it yes"><div class="ic">✓</div><div>Presente físicamente<small>Comparten casa, mesa y agenda</small></div></div>'
    '<div class="it no"><div class="ic">✕</div><div>Disponible emocionalmente<small>Para escuchar y sostener</small></div></div>'
    '<div class="it no"><div class="ic">✕</div><div>Conectada afectivamente<small>Mirada, contacto, cercanía</small></div></div>'
    '<div class="it no"><div class="ic">✕</div><div>Involucrada en el vínculo<small>A nivel afectivo</small></div></div>'
    '</div>'
    + band("Entender la desconexión es el primer paso para revertirla: necesitas ver el mapa antes de tomar la ruta")
    + '</div>', key="cap1", section="01 · Qué es")

# ============ CAP 2 (causas)
cs = CAUSAS
add('<div class="pad">'
    + opener("02", "Capítulo dos", ph("Pareja sentada en extremos opuestos del sofá, ambos con la mirada perdida", "couple sitting apart on couch, emotional distance couple, sad couple sofa", "position:absolute;inset:0", "dk"),
             "¿Por qué ocurre la desconexión emocional?", "Trece causas frecuentes, con un ejemplo cotidiano de cada una.", h=320)
    + cards(cs[0:2], 1) + '</div>', key="cap2", section="02 · Por qué ocurre")
add('<div class="pad">' + ph("Persona de espaldas mirando por la ventana, gesto pensativo y triste", "woman looking out window sad, lonely person window", "", "banner")
    + cards(cs[2:5], 3) + '</div>', section="02 · Por qué ocurre")
add('<div class="pad">' + ph("Pareja en la mesa del desayuno, cada uno en su mundo, rutina gris", "couple breakfast table routine bored, couple tired kitchen", "", "banner")
    + cards(cs[5:8], 6) + '</div>', section="02 · Por qué ocurre")
add('<div class="pad">' + ph("Pareja en la cama o sofá, cada uno mirando su celular", "couple on phones in bed, phone addiction couple, couple ignoring each other smartphone", "", "banner")
    + cards(cs[8:11], 9) + '</div>', section="02 · Por qué ocurre")
add('<div class="pad">' + ph("Padres agotados con niños y trabajo; la pareja queda en segundo plano", "parents tired kids work home, busy couple family routine", "height:300px", "banner")
    + cards(cs[11:13], 12) + band("Identificar la verdadera brecha te ayudará a no luchar contra fantasmas ni a imaginar escenarios que no existen.") + '</div>',
    section="02 · Por qué ocurre")

# ============ TEST 1
INST1 = '<p class="inst">Responde <b>sí</b> o <b>no</b> a cada afirmación. Cada “sí” indica una <b>posible causa</b> de desconexión emocional.</p>'
add('<div class="pad test"><span class="tab">Mini Test 1</span><h2>¿Qué está desconectando emocionalmente a nuestra pareja?</h2>' + INST1 + test_groups(TEST1[0:4], 1) + '</div>',
    key="t1", section="Mini Test 1")
add('<div class="pad test">' + test_groups(TEST1[4:9], 5) + '</div>', section="Mini Test 1")
add('<div class="pad test">' + test_groups(TEST1[9:13], 10)
    + '<div class="score">Total de “sí”: <span></span></div><div class="sp"></div>'
    + band("Cuando sabes qué está fallando, puedes comenzar a repararlo y abrir la puerta para los pasos siguientes.") + '</div>', section="Mini Test 1")

# ============ CAP 3 síntomas
add('<div class="pad">'
    + opener("03", "Capítulo tres", '<div class="photo-bg" style="position:absolute;inset:0;background-image:url(assets/img/manos-cables.jpg);background-position:center 40%"></div>',
             "¿Cómo saber que estamos desconectados o nos estamos desconectando?", h=330)
    + cards(SINTOMAS[0:3], 1, examples=False) + '</div>', key="cap3", section="03 · Cómo saber")
add('<div class="pad">' + cards(SINTOMAS[3:6], 4, examples=False) + '<div class="sp"></div>'
    + ph("Manos de pareja que casi se tocan sobre una mesa, sin llegar a unirse", "hands almost touching table, couple hands distance", "height:300px;flex:none;border-radius:6px;margin-bottom:22px", "")
    + band("La distancia se acorta cuando volvemos a mirarnos con intención.") + '</div>', section="03 · Cómo saber")
add('<div class="pad test compact"><span class="tab">Mini Test 2</span><h2>¿Estamos desconectados emocionalmente?</h2>'
    '<p class="inst">Responde <b>sí</b> o <b>no</b> a cada afirmación. Cada “sí” indica un <b>posible síntoma</b> de desconexión emocional.</p>'
    + test_groups(TEST2, 1) + '<div class="score">Total de “sí”: <span></span></div><div class="sp" style="height:28px"></div>'
    + band("Detener la distancia significa poner pausa al patrón que los está separando. Se trata de hacer consciente qué comportamientos alimentan la desconexión y hacernos cargo de ello.") + '</div>',
    key="t2", section="Mini Test 2")

# ============ CAP 4 consecuencias
add('<div class="pad">'
    + opener("04", "Capítulo cuatro", '<div class="photo-bg" style="position:absolute;inset:0;background-image:url(assets/img/corazon-alto.jpg);background-position:center 62%"></div>',
             "¿Qué puede ocurrir en uno o ambos miembros de la pareja a raíz de la desconexión emocional?", h=300)
    + cards(CONSEC[0:3], 1, examples=False) + '</div>', key="cap4", section="04 · Qué puede ocurrir")
add('<div class="pad">' + cards(CONSEC[3:6], 4, examples=False) + '<div class="sp"></div>'
    + ph("Persona despierta de noche en la cama, mirando el techo, luz azul tenue", "insomnia night bed awake, woman awake at night overthinking", "height:290px;flex:none;border-radius:6px;margin-bottom:22px", "dk")
    + band("La reconexión empieza el día en que decidimos elegirnos de nuevo.") + '</div>', section="04 · Qué puede ocurrir")

# ============ TEST FINAL
add('<div class="pad test"><span class="tab">Mini Test final</span><h2>¿Cómo vivo la desconexión emocional?</h2>'
    '<p class="inst">Tómate un momento, respira y responde con honestidad. Aquí no hay respuestas correctas: <b>hay respuestas tuyas</b>.</p>'
    + reflect_groups(TEST3[0:2], 1) + '</div>', key="t3", section="Mini Test final")
add('<div class="pad test">' + reflect_groups(TEST3[2:4], 3) + '<div class="sp" style="height:22px"></div>'
    + band("La desconexión emocional puede entenderse como un proceso dinámico que, aunque duela, también abre la puerta a la reparación. No es necesariamente un fracaso ni una sentencia definitiva.") + '</div>', section="Mini Test final")

# ============ CAP 5 ejemplos
ej = "".join(f'<div class="card" style="grid-template-columns:96px 1fr"><div class="no" style="font-size:12px;letter-spacing:.2em;-webkit-text-stroke:0;color:var(--coral-d);font-weight:800;text-transform:uppercase;padding-top:5px">Escena {i}</div><div><p style="margin:0">{E(t)}</p></div></div>' for i, t in enumerate(EJEMPLOS, 1))
add('<div class="pad">'
    + opener("05", "Capítulo cinco", ph("Pareja en la sala; uno habla, el otro mira el celular y evita el contacto visual", "couple living room distracted phone, couple not listening", "position:absolute;inset:0", "dk"),
             "Ejemplos prácticos de desconexión emocional", "Cinco escenas cotidianas que quizás te resulten familiares.", h=250)
    + '<div class="cards">' + ej + '</div><div class="sp"></div>'
    + band("La clave es detener el “piloto automático emocional” y recuperar la presencia.") + '</div>', key="cap5", section="05 · Ejemplos")

# ============ CAP 6 herramientas
def tool_big(t): return f'<div class="tool big"><p>{E(t)}</p></div>'
def tool(tag, p, n): return f'<div class="tool"><div class="tag"><small>Herramienta {n:02d}</small>{E(tag)}</div><p>{p}</p></div>'
A = "".join(tool_big(t) for t in HERR_A)
add('<div class="pad">'
    + opener("06", "Capítulo seis", ph("Pareja caminando de la mano al atardecer, ligeros y sonrientes", "couple walking holding hands sunset, couple reconnecting", "position:absolute;inset:0", ""),
             "Herramientas básicas", "Primeros pasos para comenzar a reconectar.", h=360)
    + '<div class="cards plain" style="margin-top:4px">' + A + '</div></div>', key="cap6", section="06 · Herramientas")

def tools_page(items, start, head=True):
    h = ('<div class="parts"><i>Según lo que nos desconecta</i></div><div style="height:6px"></div>' if head else "")
    return '<div class="pad">' + h + "".join(tool(t, p, start + k) for k, (t, p) in enumerate(items)) + '</div>'
add(tools_page(HERR_B[0:4], 1), section="06 · Herramientas")
add(tools_page(HERR_B[4:8], 5, False), section="06 · Herramientas")
add(tools_page(HERR_B[8:11], 9, False), section="06 · Herramientas")
add(tools_page(HERR_B[11:13], 12, False).replace('</div></div>\n','') if False else tools_page(HERR_B[11:13], 12, False)[:-6]
    + '<div class="sp"></div>' + ph("Pareja leyendo juntos un libro en el sofá, cercanos y relajados", "couple reading book together sofa, couple cozy reading", "height:300px;flex:none;border-radius:6px", "") + '</div>',
    section="06 · Herramientas")
C = "".join(tool_big(t) for t in HERR_C)
add('<div class="pad"><div class="parts"><i>Para sostener la conexión</i></div><div style="height:6px"></div><div class="cards plain">' + C + '</div><div class="sp"></div>'
    + ph("Pareja abrazada, frente con frente, ojos cerrados, momento íntimo", "couple embrace forehead touch, couple intimacy tender", "height:320px;flex:none;border-radius:6px;margin-bottom:22px", "")
    + band("La distancia no crece sola: se alimenta. Pero también puede detenerse con una decisión consciente.") + '</div>', section="06 · Herramientas")

# ============ MENSAJE FINAL
add('<div class="pad mf"><span class="script" style="font-size:34px;line-height:1">Para cerrar</span>'
    '<h2 style="font:800 44px/1.05 var(--sans);margin:2px 0 20px">Mensaje final…</h2>'
    '<p class="lead" style="font-size:18px">A lo largo de este Ebook recorrimos un camino que nos permitió comprender que la desconexión emocional es un proceso gradual y doloroso, del cual solo podemos salvarnos cuando identificamos sus raíces con honestidad, responsabilidad y valentía.</p>'
    '<p>Hacernos cargo de lo que nos corresponde es el primer paso para acercarnos, mirarnos, reconocernos, elegirnos y comenzar a restaurar el vínculo.</p>'
    '<p>La distancia en pareja puede despertar rechazo, ansiedad, tristeza o abandono. Y, como vimos, existen dinámicas que vuelven la relación un espacio inseguro, frío y distante: el maltrato, las promesas incumplidas, la invalidación emocional, las heridas pasadas, el estrés sostenido y la monotonía, son algunas de ellas. Reconocerlas es fundamental para detener el daño y abrir la puerta a la reparación.</p>'
    + ph("Pareja mirándose a los ojos con ternura, luz suave", "couple looking at each other tenderly, couple love warm light", "height:330px;flex:none;border-radius:6px;margin-top:14px", "")
    + '</div>', key="final", section="Mensaje final")
add('<div class="pad mf"><p style="margin-bottom:8px">Mi intención es que este Ebook te haya permitido identificar:</p>'
    '<ul class="ck"><li>Qué dinámicas deterioran la relación;</li><li>Qué síntomas de desconexión emocional están presentes;</li><li>Cómo nos afecta la distancia afectiva; y</li><li>Qué herramientas básicas podemos comenzar a aplicar según su caso particular.</li></ul>'
    '<p>Algunas de las prácticas que exploraste aquí: la escucha empática, la comunicación asertiva, las peticiones claras, la validación emocional, la novedad, el tiempo de calidad y la expresión del amor según el lenguaje afectivo del otro, no son soluciones mágicas, son actos conscientes, diarios y constantes que, sostenidos en el tiempo, pueden transformar profundamente la relación.</p>'
    '<p>Hoy los invito a soltar las culpas y ponerse manos a la obra. Cada uno debe asumir su parte y emprender el cambio desde la presencia, la intención y la elección diaria.</p>'
    + '<div class="sp" style="height:6px"></div>' + band("El amor es sentimiento, sí, pero también es acción.").replace('class="band"','class="band" style="margin-top:14px"') + '<div class="sp" style="height:26px"></div>'
    '<div class="thanks"><p>Gracias por llegar hasta aquí y por confiar en mi trabajo. Y gracias, especialmente, a cada pareja que he acompañado en consulta: ustedes inspiran cada palabra de este Ebook.</p>'
    '<img src="assets/logo/johanna-negro.png" alt="Johanna Daza"></div></div>', section="Mensaje final")

# ============ SOBRE / OTRO EBOOK
add('<div class="draft" style="right:92px;top:30px">Texto de relleno · editar</div>'
    '<div class="pad about"><span class="script" style="font-size:32px;line-height:1">Quién soy</span><h2>Johanna Daza</h2>'
    '<div class="who">' + ph("Retrato de Johanna", "segundo retrato (más cerrado)", "", "dk sm", client=True) +
    '<div><p>Soy asesora clínica de pareja. Acompaño a personas y parejas que desean comprender su historia, sanar sus heridas y construir vínculos más presentes, honestos y conectados.</p>'
    '<p style="margin:0">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mi trabajo une la experiencia en consulta con herramientas simples que cualquiera puede empezar a practicar hoy.</p></div></div>'
    '<div class="contact"><div><b>Instagram</b>@usuario</div><div><b>Sitio web</b>www.tusitio.com</div><div><b>Escríbeme</b>correo@ejemplo.com</div></div>'
    '<div class="next">' + ph("Portada del próximo E-Book", "diseño de portada del segundo E-Book", "", "dk sm", client=True) +
    '<div><span class="eyebrow">Hay otro E-Book</span><h3>[Título del segundo E-Book]</h3>'
    '<p>Una guía para seguir profundizando en el camino de la reconexión. Texto de relleno: aquí irá una breve descripción del segundo E-Book y a quién está dirigido.</p><span class="cta">Conócelo aquí</span></div></div>'
    '</div>', key="about", section="Sobre la autora")

# ============ CONTRAPORTADA
add('<div class="bg"></div><div class="bt"><h2>La conexión comienza cuando alguien se atreve a hablar…</h2><span class="s">…y alguien decide escuchar.</span></div>'
    '<img class="logo" src="assets/logo/johanna-blanco.png" alt="Johanna Daza">', key="backcover", cls="back dark", dark=True, nofoot=True)

# ------------------------------------------------------------------ Índice
pgnum = {p["key"]: i + 1 for i, p in enumerate(pages) if p["key"]}
toc = [("", "Sobre la autora", "bio"), ("", "Iniciemos…", "intro"),
       ("01", "¿Qué es la desconexión emocional?", "cap1"),
       ("02", "¿Por qué ocurre la desconexión emocional?", "cap2"), ("-", "Mini Test 1 · ¿Qué nos está desconectando?", "t1"),
       ("03", "¿Cómo saber que estamos desconectados?", "cap3"), ("-", "Mini Test 2 · ¿Estamos desconectados?", "t2"),
       ("04", "¿Qué puede ocurrir a raíz de la desconexión?", "cap4"), ("-", "Mini Test final · ¿Cómo vivo la desconexión?", "t3"),
       ("05", "Ejemplos prácticos de desconexión emocional", "cap5"),
       ("06", "Herramientas básicas", "cap6"),
       ("", "Mensaje final", "final"), ("", "Quién soy y el próximo E-Book", "about")]
lis = "".join(f'<li class="{"sub" if n=="-" else ""}"><span class="no">{n if n!="-" else ""}</span><span class="tt">{E(t)}</span><span class="pg">{pgnum[k]}</span></li>' for n, t, k in toc)
toc_html = ('<div class="pad"><span class="script">Lo que vas a encontrar</span><h2>Contenido</h2><ol>' + lis + '</ol><div class="toc-img"></div></div>')
for p in pages:
    if p["body"] == "{{TOC}}": p["body"] = toc_html

# ------------------------------------------------------------------ Ensamble
out = []
for i, p in enumerate(pages, 1):
    side = "odd" if i % 2 else "even"
    run = foot = ""
    if not p["nofoot"]:
        run = f'<div class="run"><span>{E(TITLE)}</span><b>{E(p["section"])}</b></div>' if p["section"] and p["cls"].split()[0:1] != ["quote"] else ""
        foot = f'<div class="foot"><span class="n">{i}</span><span class="t">Johanna Daza · E-Book</span></div>'
    if p["cls"].startswith("cover") or p["cls"].startswith("back"): run = ""
    out.append(f'<section class="page {side} {p["cls"]}" id="p{i}" data-n="{i}">{run}{p["body"]}{foot}</section>')

doc = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE} — Johanna Daza · E-Book (v1)</title>
<link rel="stylesheet" href="css/style.css">
</head><body>
<main class="book">
{chr(10).join(out)}
</main>
<script src="js/view.js"></script>
</body></html>'''
open("index.html", "w", encoding="utf-8").write(doc)

# lista de imágenes pendientes
md = ["# Imágenes de banco pendientes (placeholders)\n",
      "Guardar cada imagen con el nombre indicado en `assets/stock/` (JPG, ~1600 px de ancho mínimo). El E-Book la toma automáticamente.\n",
      "| # | Archivo | Descripción | Términos de búsqueda (Unsplash / Pexels / Freepik) |", "|---|---|---|---|"]
for n, d, s in STOCK:
    md.append(f"| {n:02d} | `assets/stock/img-{n:02d}.jpg` | {d} | {s} |")
md += ["", "# Fotos de Johanna / cliente pendientes", "", "Guardar en `assets/client/` con el nombre indicado.", "", "| # | Archivo | Descripción | Notas |", "|---|---|---|---|"]
for n, d, s_ in CLIENT:
    md.append(f"| {n:02d} | `assets/client/foto-{n:02d}.jpg` | {d} | {s_} |")
open("IMAGENES_PENDIENTES.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print(len(pages), "páginas;", len(STOCK), "placeholders")
