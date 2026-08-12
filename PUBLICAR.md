# Cómo publicar el repaso en el site

El HTML no se puede pegar en Google Sites como texto: `Insertar > Insertar código`
admite del orden de 10.000 caracteres y `Infantil.html` tiene 113.706, y además
llama a 985 imágenes que Sites no puede alojar. La vía es alojarlo en **GitHub
Pages** (gratis) y luego incrustar esa dirección en el site.

Se hace una vez. Después, para actualizar el contenido basta con repetir el
paso 5 y la página del site se actualiza sola.

---

## Antes de empezar: el repositorio será público

GitHub Pages gratuito solo funciona con repositorios **públicos**. Eso significa
que cualquiera con la dirección puede ver las fichas y descargar las imágenes.

- Las fichas y los pictogramas: no hay problema, son material didáctico y los
  pictogramas de ARASAAC llevan ya su atribución (CC BY-NC-SA, uso no comercial
  — un colegio encaja).
- `Programación de Vocabulario.xlsx` **no se sube** (está en `.gitignore`), así
  que la programación curricular completa no queda expuesta.

Si prefieres que nada de esto sea público, esta vía no sirve: habría que usar el
hosting propio del colegio o repartir el archivo autónomo por Drive.

---

## Paso 1 — Crear la cuenta

Entra en <https://github.com> y crea una cuenta (o inicia sesión si ya tienes).
Apunta el **nombre de usuario**: aparecerá en la dirección final.

## Paso 2 — Crear el repositorio

1. Arriba a la derecha, **+** → **New repository**.
2. **Repository name**: `repaso-vocabulario`
3. Déjalo en **Public**.
4. **No marques** ninguna casilla de "Add a README", "Add .gitignore" ni licencia.
   El repositorio tiene que quedar vacío.
5. **Create repository**.

## Paso 3 — Subir los archivos

La carpeta ya está preparada como repositorio git, con todo confirmado en un
primer commit. Solo falta enlazarla con GitHub y subirla. En la pantalla que
aparece tras crear el repositorio, GitHub muestra la dirección; será algo como
`https://github.com/TU-USUARIO/repaso-vocabulario.git`.

Dime tu nombre de usuario y lanzo yo estos dos comandos:

```bash
git remote add origin https://github.com/TU-USUARIO/repaso-vocabulario.git
git push -u origin main
```

Al subir se abrirá una ventana del navegador pidiendo que inicies sesión en
GitHub: **esa parte la haces tú**, yo no manejo tus credenciales. Son unos 10 MB,
tarda un minuto.

## Paso 4 — Activar GitHub Pages

En el repositorio: **Settings** → **Pages** (menú izquierdo).

- **Source**: `Deploy from a branch`
- **Branch**: `main`, carpeta `/ (root)` → **Save**

Espera un par de minutos y recarga: aparecerá la dirección publicada,

```
https://TU-USUARIO.github.io/repaso-vocabulario/
```

Compruébala en el navegador antes de seguir.

## Paso 5 — Incrustarlo en el site

En Google Sites, en la página donde lo quieras:

1. Panel derecho → **Insertar** → **Insertar** → pestaña **Por URL**.
2. Pega la dirección de arriba y pulsa **Insertar**.
3. Estira el marco para que ocupe todo el ancho y bastante alto (**unos 800 px**;
   la ficha necesita altura, con poco espacio obliga a hacer scroll dentro del
   marco).
4. **Publicar**.

### Enlazar una palabra concreta

También puedes incrustar o enlazar una sola palabra:

- `.../repaso-vocabulario/Infantil.html#ENCIMA` abre esa ficha.
- `.../repaso-vocabulario/Infantil.html#ENCIMA,abrir` la abre ya destapada,
  útil para proyectar.

---

## Actualizar el contenido más adelante

Cuando se añadan cursos o palabras nuevas:

```bash
python scripts\generar_html.py
git add -A
git commit -m "Añadidas las palabras de ..."
git push
```

En un par de minutos la página del site muestra la versión nueva, sin tocar nada
en Google Sites.
