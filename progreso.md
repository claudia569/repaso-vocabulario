# Progreso — Repaso Programa Vocabulario (HTML para el site)

## 📌 ESTADO ACTUAL (última actualización: 12/08/2026) — LEER ESTO PRIMERO

**Tarea:** fichas HTML de repaso de vocabulario para publicar en el site del centro.
Carpeta independiente del proyecto de presentaciones (`Claudia Code`), aunque
se alimenta de sus pptx.

**Hecho y verificado con render real:**

| Entregable | Contenido |
|---|---|
| `Infantil.html` | 90 palabras · INF3 + INF4 + INF5, U1–U10 de cada curso |
| `Primaria.html` | 30 palabras · 1º EP, U1–U10 |

**Siguiente paso:** esperando dos decisiones de la usuaria (ver "Decisiones
abiertas" abajo). No hay nada a medio construir.

---

## Decisiones ya tomadas

| Pregunta | Respuesta |
|---|---|
| Estructura de la ficha | La de su imagen de referencia: Conciencia fonémica · Escritura · Definición · Dibujo · Sinónimos · Antónimos · Frase |
| Interacción | Cada bloque empieza tapado y se destapa al pulsarlo |
| Navegación | Índice lateral de palabras (buscador + agrupado por curso y unidad) + ficha |
| Alcance | Toda la programación, empezando por Infantil y subiendo |
| Contenido | Extraído de los pptx tipo A ya validados, no generado de nuevo |
| Articulemas | Set `ARTICULEMAS/` del proyecto (foto de boca con la letra debajo) |
| Sinónimos/antónimos | 3 + 3, cada uno con su pictograma |
| Formato de salida | Un archivo por etapa: Infantil · Primaria · ESO/CFGB |

| Alojamiento | GitHub Pages, repo público `claudia569/repaso-vocabulario` |
| Retoques de contenido | Capa `datos/correcciones.json` encima de lo extraído, en vez de editar los pptx por cada cambio |

## Publicación

- Repositorio: `https://github.com/claudia569/repaso-vocabulario` (público —
  `Programación de Vocabulario.xlsx` queda fuera por `.gitignore`).
- Subida hecha el 12/08/2026 (commit `72f4f22`). El push desde este entorno
  necesita `GIT_TERMINAL_PROMPT=1` y `-c credential.interactive=true`; sin eso
  falla con "Cannot prompt because user interactivity has been disabled".
  Windows ya guardó las credenciales, así que los siguientes push no deberían
  pedir nada.
- Pasos de publicación y de incrustación en Google Sites: `PUBLICAR.md`.
- Créditos de ARASAAC (CC BY-NC-SA) al pie de cada ficha y del índice:
  obligatorio desde que el material deja de estar solo en local.

## Decisiones abiertas (bloquean el siguiente paso)

1. **Activar GitHub Pages** en Settings → Pages (rama `main`, carpeta raíz).
   Pendiente de la usuaria; hasta entonces la URL pública no existe.
2. **Qué curso se completa a continuación.** Quedan ~1230 palabras de la
   programación sin power de origen.

## Detalles técnicos que conviene no volver a descubrir

- **Los articulemas de los pptx no se pueden reutilizar por hash**: se
  reescribieron al construir los powers y ya no coinciden byte a byte con
  `ARTICULEMAS/`. La secuencia de fonemas se deriva por reglas
  (`scripts/fonemas.py`) y **se valida contra el número real de articulemas de
  la slide 2**: coinciden en las 120 palabras extraídas, así que las reglas
  sirven también para las palabras que aún no tienen power.
- **INF 5 usa un set de articulemas distinto** (letra ortográfica C/Q/Z en vez
  del fonema). Da igual para este HTML, porque aquí siempre se pinta el set
  `ARTICULEMAS/`, no las imágenes del pptx.
- **La etiqueta del articulema es el fonema, no la letra de la palabra**:
  DEBAJO muestra "G" en la J, TRANQUILIDAD muestra "C" en el QUI. Es la
  convención del proyecto, pero en esta ficha se ve justo al lado del bloque
  *Escritura* — pendiente de que la usuaria diga si lo deja así.
- **Filtrar archivos por `"DIA" in nombre` se come palabras**: `ME-DIA-NO` se
  quedaba fuera. Usar `re.search(r"_DIA[1-4]_", nombre)`.
- **Sílabas añadidas por iniciativa propia** dentro de *Conciencia fonémica*
  (👏 TRAN · QUI · LI · DAD), a partir de la slide 3. No estaban en la imagen de
  referencia: si la usuaria las quiere fuera, se quitan en `generar_html.py`.
- **Sin screenshots desde el panel del navegador** en este entorno: se verifica
  con Chrome headless
  (`chrome.exe --headless=new --no-sandbox --screenshot=... --window-size=...`)
  y midiendo el DOM por JS. El recorte lateral que aparece en los screenshots
  headless a 420px es un artefacto: el DOM real da `scrollWidth == clientWidth`.
- **Servidor local de pruebas**: entrada `repaso-vocabulario` (puerto 8778) en
  `Claudia Code\.claude\launch.json`.

## Pendiente

- 5º EP: sus archivos no son tipo A (son Día 1–4), necesitan otro mapeo de
  slides para extraerlos.
- ~1230 palabras sin power de origen: hay que generar definición, sinónimos,
  antónimos, frase e imágenes (ARASAAC en Infantil y primeros cursos;
  Pixabay/Pexels a partir de 4º de Primaria).
- Etapa ESO/CFGB: aún no se genera ningún archivo (no hay datos).
