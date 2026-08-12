# -*- coding: utf-8 -*-
"""
Genera el HTML de repaso de vocabulario, un archivo por etapa.

    python generar_html.py            -> HTML ligero que usa la carpeta assets/
    python generar_html.py --embed    -> HTML autónomo con las imágenes dentro

Estructura de la ficha (la de la imagen de referencia):

    ┌───────────────────────────────┬──────────────┐
    │ Conciencia fonémica           │ Escritura    │
    ├───────────────────────────────┼──────────────┤
    │ Definición                    │ Dibujo       │
    ├───────────────┬───────────────┼──────────────┤
    │ Sinónimos     │ Antónimos     │ Frase        │
    └───────────────┴───────────────┴──────────────┘

Cada bloque empieza tapado y se destapa al pulsarlo.
"""
import base64
import json
import mimetypes
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATOS = BASE / "datos"
ASSETS = BASE / "assets"

ETAPAS = {
    "Infantil": ["INF3", "INF4", "INF5"],
    "Primaria": ["1EP", "2EP", "3EP", "4EP", "5EP", "6EP"],
    "ESO y CFGB": ["1ESO", "2ESO", "1CFGB", "2CFGB", "1CFGM", "2CFGM"],
}

EMBED = "--embed" in sys.argv


def data_uri(ruta):
    tipo = mimetypes.guess_type(ruta.name)[0] or "image/webp"
    return f"data:{tipo};base64," + base64.b64encode(ruta.read_bytes()).decode()


def src_articulema(fonema):
    f = ASSETS / "articulemas" / f"_{fonema}_.webp"
    if not f.exists():
        f = ASSETS / "articulemas" / f"_{fonema}_.png"
    if not f.exists():
        return ""
    return data_uri(f) if EMBED else f"assets/articulemas/{f.name}"


def src_img(curso, nombre):
    if not nombre:
        return ""
    f = ASSETS / "img" / curso / nombre
    if not f.exists():
        return ""
    return data_uri(f) if EMBED else f"assets/img/{curso}/{nombre}"


CAMPOS_SIMPLES = {"palabra", "definicion", "frase", "silabas", "fonemas",
                  "img_dibujo", "img_frase", "curso_nombre"}


def cargar_correcciones():
    """Lee datos/correcciones.json (retoques manuales que sobreviven a una
    reextracción de los pptx). Las claves que empiezan por '_' son notas."""
    ruta = DATOS / "correcciones.json"
    if not ruta.exists():
        return {}
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    return {k: v for k, v in datos.items() if not k.startswith("_")}


def aplicar_correcciones(fichas, correcciones, avisos):
    """Aplica los retoques sobre las fichas extraídas. Clave: 'CURSO/PALABRA'."""
    indice = {f"{f['curso']}/{f['palabra']}": f for f in fichas}
    usadas = set()

    for clave, cambios in correcciones.items():
        ficha = indice.get(clave.upper())
        if ficha is None:
            continue                      # puede ser de otra etapa; se avisa fuera
        usadas.add(clave)

        if cambios.get("oculta"):
            ficha["_oculta"] = True

        for campo, valor in cambios.items():
            if campo in ("oculta",):
                continue
            if campo in CAMPOS_SIMPLES:
                ficha[campo] = valor
            elif campo in ("sinonimos", "antonimos"):
                ficha[campo] = valor
            elif re.fullmatch(r"(sinonimo|antonimo)([1-3])", campo):
                tipo, n = re.fullmatch(r"(sinonimo|antonimo)([1-3])", campo).groups()
                lista = ficha[tipo + "s"]
                i = int(n) - 1
                while len(lista) <= i:
                    lista.append({"texto": "", "img": None})
                lista[i] = {**lista[i], **valor}
            else:
                avisos.append(f"{clave}: campo desconocido '{campo}', ignorado")

    return [f for f in fichas if not f.get("_oculta")], usadas


def cargar(etapa):
    fichas = []
    for codigo in ETAPAS[etapa]:
        ruta = DATOS / f"{codigo}.json"
        if not ruta.exists():
            continue
        fichas.extend(json.loads(ruta.read_text(encoding="utf-8")))
    return fichas


def preparar(fichas):
    """Sustituye nombres de archivo por rutas/URIs listas para el HTML."""
    out = []
    for f in fichas:
        c = f["curso"]
        out.append({
            "curso": c,
            "cursoNombre": f["curso_nombre"],
            "unidad": f["unidad"],
            "palabra": f["palabra"],
            "fonemas": [{"letra": x, "src": src_articulema(x)} for x in f["fonemas"]],
            "silabas": f.get("silabas", []),
            "definicion": f["definicion"],
            "dibujo": src_img(c, f.get("img_dibujo")),
            "frase": f["frase"],
            "fraseImg": src_img(c, f.get("img_frase")),
            "sinonimos": [{"texto": s["texto"], "src": src_img(c, s["img"])}
                          for s in f["sinonimos"]],
            "antonimos": [{"texto": s["texto"], "src": src_img(c, s["img"])}
                          for s in f["antonimos"]],
        })
    return out


CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --azul:#1268b3; --cian:#00b0f0; --verde:#00a94f; --verdeclaro:#92d050;
  --rojo:#e8112d; --rojoosc:#b00020; --ambar:#f5a800;
  --gris:#f1f2f4; --borde:#d8dbe0; --texto:#22262b;
}
html,body{margin:0;padding:0}
body{font-family:"Segoe UI",system-ui,-apple-system,sans-serif;color:var(--texto);
     background:#e9ecef;display:flex;min-height:100vh}

/* ---------- índice lateral ---------- */
#indice{width:270px;flex:0 0 270px;background:#fff;border-right:1px solid var(--borde);
        display:flex;flex-direction:column;height:100vh;position:sticky;top:0}
#indice h1{font-size:17px;margin:0;padding:16px 16px 10px;line-height:1.25}
#indice h1 small{display:block;font-weight:400;font-size:12px;color:#6b7280;margin-top:3px}
#buscar{margin:0 16px 10px;padding:8px 10px;border:1px solid var(--borde);
        border-radius:8px;font-size:14px;width:calc(100% - 32px)}
#lista{overflow-y:auto;flex:1;padding-bottom:24px}
.grupo{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
       color:#6b7280;background:#f6f7f9;padding:7px 16px;position:sticky;top:0;
       border-top:1px solid var(--borde);border-bottom:1px solid var(--borde)}
.item{display:flex;justify-content:space-between;gap:8px;align-items:baseline;
      padding:8px 16px;cursor:pointer;font-size:14px;border-bottom:1px solid #f0f1f3}
.item:hover{background:#eef5fc}
.item.activo{background:var(--azul);color:#fff}
.item .u{font-size:11px;color:#9ca3af}
.item.activo .u{color:#cfe3f7}

/* ---------- ficha ---------- */
#panel{flex:1;padding:22px 26px 40px;min-width:0}
.cabecera{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:16px}
.cabecera .titulo{font-size:26px;font-weight:700;margin:0}
.cabecera .meta{font-size:13px;color:#5b6472}
.botones{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
button.acc{border:1px solid var(--borde);background:#fff;border-radius:8px;
      padding:8px 13px;font-size:13px;cursor:pointer;font-family:inherit;color:var(--texto)}
button.acc:hover{background:#f3f6f9}
button.acc:disabled{opacity:.4;cursor:default}

.ficha{display:grid;gap:10px;
       grid-template-columns:1fr 1fr 1.05fr;
       grid-template-areas:"fon fon esc" "def def dib" "sin ant fra"}
.b-fon{grid-area:fon}.b-esc{grid-area:esc}.b-def{grid-area:def}
.b-dib{grid-area:dib}.b-sin{grid-area:sin}.b-ant{grid-area:ant}.b-fra{grid-area:fra}

.bloque{background:#fff;border:1px solid var(--borde);border-radius:10px;overflow:hidden;
        display:flex;flex-direction:column;min-width:0;
        box-shadow:0 1px 2px rgba(16,24,40,.05)}
.bloque > h2{margin:0;font-size:14px;font-weight:700;letter-spacing:.02em;color:#fff;
             padding:8px 12px;text-align:center}
.b-fon>h2{background:var(--azul)}.b-esc>h2{background:var(--cian)}
.b-def>h2{background:var(--verde)}.b-dib>h2{background:var(--verdeclaro)}
.b-sin>h2{background:var(--rojo)}.b-ant>h2{background:var(--rojoosc)}
.b-fra>h2{background:var(--ambar)}

.cuerpo{position:relative;flex:1;min-height:132px;display:flex;align-items:center;
        justify-content:center;padding:14px;background:var(--gris)}
.contenido{width:100%;display:flex;align-items:center;justify-content:center;
           flex-direction:column;gap:10px}
.tapa{position:absolute;inset:0;background:var(--gris);display:flex;align-items:center;
      justify-content:center;gap:9px;cursor:pointer;color:#7b8494;font-size:14px;
      font-weight:600;user-select:none;transition:background .15s}
.tapa:hover{background:#e6e9ee;color:#4b5563}
.tapa svg{width:19px;height:19px;flex:0 0 19px}
.bloque.abierto .tapa{display:none}
.bloque.abierto .cuerpo{cursor:pointer}

/* contenidos concretos */
.fonemas{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
.fonemas img{height:78px;width:auto;border-radius:5px}
.silabas{display:flex;gap:7px;flex-wrap:wrap;justify-content:center;margin-top:2px}
.silabas span{background:#fff;border:1px solid var(--borde);border-radius:7px;
              padding:4px 11px;font-size:15px;font-weight:600}
.palabra{font-size:34px;font-weight:700;letter-spacing:.01em;text-align:center;
         line-height:1.15;word-break:break-word}
.definicion{font-size:19px;line-height:1.45;text-align:center;max-width:64ch}
.frase{font-size:18px;line-height:1.45;text-align:center}
.ilustra{max-width:100%;max-height:210px;border-radius:8px;display:block}
.b-fra .ilustra{max-height:150px}
.lista-sa{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;width:100%}
.sa{display:flex;flex-direction:column;align-items:center;gap:5px;width:92px}
.sa img{width:74px;height:74px;object-fit:contain;background:#fff;border-radius:7px;
        border:1px solid var(--borde)}
.sa span{font-size:13px;font-weight:700;text-align:center;line-height:1.15;
         word-break:break-word}
.altavoz{border:none;background:transparent;cursor:pointer;font-size:20px;padding:2px 6px;
         line-height:1;opacity:.55}
.altavoz:hover{opacity:1}
.vacio{color:#9aa2ad;font-size:14px;font-style:italic}
.creditos{margin-top:18px;font-size:12px;color:#79828f;line-height:1.5;max-width:80ch}
.creditos a{color:#5b6472}

@media (max-width:1100px){
  .ficha{grid-template-columns:1fr 1fr;
         grid-template-areas:"fon fon" "esc dib" "def def" "sin ant" "fra fra"}
}
@media (max-width:760px){
  body{flex-direction:column}
  #indice{width:100%;flex:none;height:auto;position:static;border-right:none;
          border-bottom:1px solid var(--borde)}
  #lista{max-height:230px}
  .ficha{grid-template-columns:1fr;
         grid-template-areas:"fon" "esc" "def" "dib" "sin" "ant" "fra"}
  #panel{padding:16px}
  .cabecera .titulo{font-size:22px}
  .botones{margin-left:0;width:100%}
  .botones button.acc{flex:1 1 auto}
  .palabra{font-size:28px}
  .definicion{font-size:17px}
}
"""

JS = r"""
const $ = (s, r=document) => r.querySelector(s);
let actual = 0;
let abrirPorDefecto = false;

/* La URL admite  #PALABRA  ,  #abrir  o  #PALABRA,abrir  */
function leerHash(){
  const partes = decodeURIComponent(location.hash.replace(/^#/, ""))
                 .split(",").map(s => s.trim()).filter(Boolean);
  abrirPorDefecto = partes.some(p => p.toLowerCase() === "abrir");
  const pal = partes.find(p => p.toLowerCase() !== "abrir");
  if (!pal) return 0;
  const i = FICHAS.findIndex(f => f.palabra.toLowerCase() === pal.toLowerCase());
  return i >= 0 ? i : 0;
}

function claveGrupo(f){ return f.cursoNombre + " · " + f.unidad; }

function pintarIndice(filtro=""){
  const lista = $("#lista"); lista.innerHTML = "";
  const f = filtro.trim().toLowerCase();
  let grupo = null;
  FICHAS.forEach((ficha, i) => {
    if (f && !ficha.palabra.toLowerCase().includes(f)
          && !ficha.cursoNombre.toLowerCase().includes(f)
          && !ficha.unidad.toLowerCase().includes(f)) return;
    const g = claveGrupo(ficha);
    if (g !== grupo){
      grupo = g;
      const h = document.createElement("div");
      h.className = "grupo"; h.textContent = g;
      lista.appendChild(h);
    }
    const el = document.createElement("div");
    el.className = "item" + (i === actual ? " activo" : "");
    el.innerHTML = `<span>${ficha.palabra}</span><span class="u">${ficha.unidad}</span>`;
    el.onclick = () => mostrar(i);
    lista.appendChild(el);
  });
  if (!lista.children.length){
    lista.innerHTML = '<div class="grupo">Sin resultados</div>';
  }
}

const OJO = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
  stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.6-7 10-7 10 7 10 7
  -3.6 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>`;

function bloque(clase, titulo, htmlContenido){
  return `<section class="bloque ${clase}">
    <h2>${titulo}</h2>
    <div class="cuerpo">
      <div class="contenido">${htmlContenido}</div>
      <div class="tapa">${OJO}<span>Pulsa para ver</span></div>
    </div>
  </section>`;
}

function listaSA(items){
  if (!items.length) return '<span class="vacio">Sin datos</span>';
  return '<div class="lista-sa">' + items.map(x =>
    `<div class="sa">${x.src ? `<img src="${x.src}" alt="">` : ""}<span>${x.texto}</span></div>`
  ).join("") + "</div>";
}

function mostrar(i){
  actual = i;
  const f = FICHAS[i];

  $("#titulo").textContent = f.palabra;
  $("#meta").textContent = `${f.cursoNombre} · Unidad ${f.unidad.replace("U","")}`;

  const fon = `<div class="fonemas">${f.fonemas.map(x =>
      x.src ? `<img src="${x.src}" alt="${x.letra}">` : `<span>${x.letra}</span>`).join("")}</div>`
    + (f.silabas.length
        ? `<div class="silabas">${f.silabas.map(s => `<span>👏 ${s}</span>`).join("")}</div>`
        : "");

  const esc = `<div class="palabra">${f.palabra}</div>
    <button class="altavoz" title="Escuchar la palabra"
      onclick="event.stopPropagation();decir('${f.palabra.replace(/'/g,"\\'")}')">🔊</button>`;

  $("#ficha").innerHTML =
      bloque("b-fon", "Conciencia fonémica", fon)
    + bloque("b-esc", "Escritura", esc)
    + bloque("b-def", "Definición", `<div class="definicion">${f.definicion || ""}</div>`)
    + bloque("b-dib", "Dibujo", f.dibujo
        ? `<img class="ilustra" src="${f.dibujo}" alt="">`
        : '<span class="vacio">Sin imagen</span>')
    + bloque("b-sin", "Sinónimos", listaSA(f.sinonimos))
    + bloque("b-ant", "Antónimos", listaSA(f.antonimos))
    + bloque("b-fra", "Frase", `<div class="frase">${f.frase || ""}</div>`
        + (f.fraseImg ? `<img class="ilustra" src="${f.fraseImg}" alt="">` : ""));

  document.querySelectorAll(".bloque").forEach(b => {
    b.querySelector(".cuerpo").onclick = () => b.classList.toggle("abierto");
  });

  // #abrir en la URL -> la ficha sale destapada (para proyectar o imprimir)
  if (abrirPorDefecto) todos(true);

  const h = "#" + encodeURIComponent(f.palabra) + (abrirPorDefecto ? ",abrir" : "");
  history.replaceState(null, "", h);

  $("#prev").disabled = i === 0;
  $("#next").disabled = i === FICHAS.length - 1;
  pintarIndice($("#buscar").value);
  document.querySelector(".item.activo")?.scrollIntoView({block:"nearest"});
}

function decir(texto){
  if (!window.speechSynthesis) return;
  const u = new SpeechSynthesisUtterance(texto);
  u.lang = "es-ES"; u.rate = .85;
  speechSynthesis.cancel(); speechSynthesis.speak(u);
}

function todos(abrir){
  document.querySelectorAll(".bloque").forEach(b => b.classList.toggle("abierto", abrir));
}

document.addEventListener("DOMContentLoaded", () => {
  $("#buscar").addEventListener("input", e => pintarIndice(e.target.value));
  $("#prev").onclick = () => mostrar(Math.max(0, actual - 1));
  $("#next").onclick = () => mostrar(Math.min(FICHAS.length - 1, actual + 1));
  $("#abrir").onclick = () => todos(true);
  $("#cerrar").onclick = () => { abrirPorDefecto = false; todos(false); };
  document.addEventListener("keydown", e => {
    if (e.target.tagName === "INPUT") return;
    if (e.key === "ArrowLeft" && actual > 0) mostrar(actual - 1);
    if (e.key === "ArrowRight" && actual < FICHAS.length - 1) mostrar(actual + 1);
  });
  mostrar(leerHash());
});
"""


def generar(etapa, fichas):
    datos = json.dumps(preparar(fichas), ensure_ascii=False, separators=(",", ":"))
    cursos = sorted({f["curso_nombre"] for f in fichas})
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Repaso de vocabulario · {etapa}</title>
<style>{CSS}</style>
</head>
<body>
<aside id="indice">
  <h1>Repaso de vocabulario<small>{etapa} · {len(fichas)} palabras</small></h1>
  <input id="buscar" type="search" placeholder="Buscar palabra o unidad…" autocomplete="off">
  <div id="lista"></div>
</aside>

<main id="panel">
  <div class="cabecera">
    <h2 class="titulo" id="titulo"></h2>
    <span class="meta" id="meta"></span>
    <div class="botones">
      <button class="acc" id="prev">← Anterior</button>
      <button class="acc" id="next">Siguiente →</button>
      <button class="acc" id="abrir">Destapar todo</button>
      <button class="acc" id="cerrar">Tapar todo</button>
    </div>
  </div>
  <div class="ficha" id="ficha"></div>
  <p class="creditos">
    Pictogramas de <strong>ARASAAC</strong> — autor Sergio Palao, propiedad del
    Gobierno de Aragón, licencia
    <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es" rel="noopener">CC BY-NC-SA</a>.
    Articulemas y contenidos didácticos: material propio del centro.
  </p>
</main>

<script>const FICHAS={datos};</script>
<script>{JS}</script>
</body>
</html>
"""
    sufijo = "_autonomo" if EMBED else ""
    nombre = etapa.replace(" y ", "_").replace(" ", "_")
    salida = BASE / f"{nombre}{sufijo}.html"
    salida.write_text(html, encoding="utf-8")
    return salida


INDICE_CSS = """
*,*::before,*::after{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI",system-ui,-apple-system,sans-serif;color:#22262b;
     background:#e9ecef;display:flex;justify-content:center;padding:48px 20px}
.caja{background:#fff;border:1px solid #d8dbe0;border-radius:14px;padding:32px 34px;
      max-width:720px;width:100%;box-shadow:0 1px 3px rgba(16,24,40,.07)}
h1{margin:0 0 6px;font-size:26px}
.sub{margin:0 0 26px;color:#5b6472;font-size:15px}
.etapa{display:flex;align-items:center;gap:14px;text-decoration:none;color:inherit;
       border:1px solid #d8dbe0;border-radius:10px;padding:15px 18px;margin-bottom:11px;
       transition:border-color .15s,background .15s}
a.etapa:hover{border-color:#1268b3;background:#f4f9fe}
.etapa .n{font-size:13px;color:#6b7280;margin-left:auto;white-space:nowrap}
.etapa strong{font-size:17px}
.etapa small{display:block;color:#6b7280;font-size:13px;margin-top:2px}
.pendiente{opacity:.5;border-style:dashed;cursor:default}
.pie{margin-top:26px;font-size:12px;color:#79828f;line-height:1.5}
.pie a{color:#5b6472}
"""


def generar_indice(resumen):
    filas = []
    for etapa, n, archivo, cursos in resumen:
        if archivo:
            filas.append(
                f'<a class="etapa" href="{archivo}">'
                f'<span><strong>{etapa}</strong><small>{cursos}</small></span>'
                f'<span class="n">{n} palabras</span></a>')
        else:
            filas.append(
                f'<span class="etapa pendiente">'
                f'<span><strong>{etapa}</strong><small>{cursos}</small></span>'
                f'<span class="n">en preparación</span></span>')
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Repaso de vocabulario</title>
<style>{INDICE_CSS}</style>
</head>
<body>
<div class="caja">
  <h1>Repaso de vocabulario</h1>
  <p class="sub">Elige la etapa. Dentro, cada palabra tiene su ficha: los bloques
     empiezan tapados y se destapan al pulsarlos.</p>
  {"".join(filas)}
  <p class="pie">
    Pictogramas de <strong>ARASAAC</strong> — autor Sergio Palao, propiedad del
    Gobierno de Aragón, licencia
    <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es" rel="noopener">CC BY-NC-SA</a>.
    Articulemas y contenidos didácticos: material propio del centro.
  </p>
</div>
</body>
</html>
"""
    salida = BASE / "index.html"
    salida.write_text(html, encoding="utf-8")
    return salida


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    correcciones = cargar_correcciones()
    avisos, usadas_total = [], set()
    if correcciones:
        print(f"Correcciones manuales: {len(correcciones)} palabras")

    resumen = []
    for etapa in ETAPAS:
        fichas = cargar(etapa)
        if fichas and correcciones:
            fichas, usadas = aplicar_correcciones(fichas, correcciones, avisos)
            usadas_total |= usadas
        if not fichas:
            print(f"{etapa}: sin fichas todavía, no se genera")
            resumen.append((etapa, 0, None, "todavía sin palabras"))
            continue
        salida = generar(etapa, fichas)
        cursos = ", ".join(sorted({f["curso_nombre"] for f in fichas}))
        resumen.append((etapa, len(fichas), salida.name, cursos))
        print(f"{etapa}: {len(fichas)} palabras -> {salida.name} "
              f"({salida.stat().st_size/1024/1024:.2f} MB)")
    if not EMBED:
        print("índice ->", generar_indice(resumen).name)

    huerfanas = set(correcciones) - usadas_total
    for clave in sorted(huerfanas):
        avisos.append(f"{clave}: no existe esa palabra en ese curso, corrección sin aplicar")
    for a in avisos:
        print("  AVISO:", a)


if __name__ == "__main__":
    main()
