# Repaso Programa Vocabulario

Fichas de repaso de vocabulario en HTML, para publicar en el site del centro.
Cada palabra se presenta con la misma estructura de siete bloques, y **cada
bloque empieza tapado y se destapa al pulsarlo**.

```
┌───────────────────────────────┬──────────────┐
│ Conciencia fonémica           │ Escritura    │
├───────────────────────────────┼──────────────┤
│ Definición                    │ Dibujo       │
├───────────────┬───────────────┼──────────────┤
│ Sinónimos     │ Antónimos     │ Frase        │
└───────────────┴───────────────┴──────────────┘
```

## Archivos

| Archivo | Qué es |
|---|---|
| `Infantil.html` | 90 palabras (Infantil 3, 4 y 5 años · U1–U10 de cada curso) |
| `Primaria.html` | 30 palabras (1º Primaria · U1–U10) |
| `datos/*.json` | Contenido de cada curso: palabra, fonemas, sílabas, definición, sinónimos, antónimos, frase e imágenes |
| `assets/articulemas/` | Los 25 articulemas del set del proyecto, en WebP |
| `assets/img/<CURSO>/` | Imágenes de cada palabra (dibujo, frase, 3 sinónimos, 3 antónimos) |
| `scripts/extraer_pptx.py` | Vuelca el contenido de los powers tipo A a `datos/*.json` + imágenes |
| `scripts/fonemas.py` | Reglas grafema → articulema en español |
| `scripts/generar_html.py` | Construye los HTML a partir de `datos/` y `assets/` |

## De dónde sale el contenido

De las presentaciones **tipo A (VOCABULARIO)** del proyecto
`Claudia Code\📚 Programa Vocabulario y Lectura`, ya revisadas y validadas:

| Bloque de la ficha | Origen |
|---|---|
| Conciencia fonémica | secuencia de fonemas derivada por reglas + sílabas de la slide 3 |
| Escritura | la palabra (word-box) |
| Definición | slide 5 |
| Dibujo | imagen de portada, slide 1 |
| Sinónimos / Antónimos | slide 9, con su pictograma |
| Frase | slide 11, con su imagen |

Los articulemas del pptx no se reutilizan (se reescribieron al construir los
powers y su hash ya no coincide con `ARTICULEMAS/`): la secuencia de fonemas se
deriva con las reglas de `fonemas.py` y **se valida contra el número real de
articulemas de la slide 2**. En las 120 palabras extraídas coinciden las 120.

## Regenerar

```bat
python scripts\extraer_pptx.py     :: relee los pptx -> datos\*.json + assets\img\
python scripts\generar_html.py     :: datos\ + assets\ -> Infantil.html, Primaria.html
python scripts\generar_html.py --embed   :: versión autónoma con las imágenes dentro
```

## Uso en clase

- **Índice lateral**: buscador + lista agrupada por curso y unidad.
- **Teclado**: ← y → cambian de palabra.
- **Botones**: *Destapar todo* / *Tapar todo*.
- **Altavoz** junto a la palabra: la lee en voz alta (voz del navegador).
- **Enlaces directos**: `Infantil.html#ENCIMA` abre esa palabra;
  `Infantil.html#ENCIMA,abrir` la abre ya destapada (útil para proyectar).

## Pendiente

- Las 30 palabras de 5º Primaria del sistema de 4º-6º EP: esos archivos no son
  tipo A (son Día 1–4), habría que extraerlos con otro mapeo de slides.
- El resto de la programación (~1230 palabras de `Programación de
  Vocabulario.xlsx`) no tiene aún power de origen: hay que generar definición,
  sinónimos, antónimos, frase e imágenes (ARASAAC en Infantil y primeros cursos;
  Pixabay/Pexels a partir de 4º de Primaria).
