<h1 align="center">🐧 Cronómetro JW — Instrucciones de Compilación (Linux)</h1>

<p align="center">
  Guía para compilar el proyecto <strong>CronometroJW_2.py</strong> desde el código fuente en Linux.
</p>

---

## 🧩 Prerrequisitos

Asegúrate de tener instalado lo siguiente en tu sistema:

### 🐍 Python 3
Verifica que Python 3 esté instalado:

```bash
python3 --version
```

### 📦 pip
El gestor de paquetes de Python. Comprueba su instalación con:

```bash
pip --version
```

### 🌱 venv (opcional)
El módulo de entornos virtuales(opcional dependiendo de tu distribuciòn) de Python (generalmente incluido por defecto en la distribución).  
Permite aislar dependencias por proyecto.

---

## ⚙️ Pasos para Compilar

### 1️⃣ Preparar el Entorno

Abre una **terminal** y navega hasta el directorio donde se encuentran los archivos del proyecto:

- `CronometroJW_2.py`
- `CronometroJW.png` (ícono opcional)

Ejemplo:

```bash
cd /ruta/a/tu/proyecto
```

Crea un entorno virtual para instalar las dependencias de forma aislada (recomendado):

```bash
python3 -m venv venv
```

Activa el entorno virtual:

```bash
source venv/bin/activate
```

> 💡 Notarás que el nombre de tu terminal cambia, indicando que el entorno `venv` está activo.

---

### 2️⃣ Instalar Dependencias

Instala las bibliotecas necesarias con `pip`:

```bash
pip install sv-ttk
pip install pyinstaller
```

- [`sv-ttk`](https://pypi.org/project/sv-ttk/) — Proporciona un estilo visual moderno a la interfaz.
- [`PyInstaller`](https://pyinstaller.org/) — Convierte el script de Python en un ejecutable independiente.

---

### 3️⃣ Compilar el Ejecutable

Con el entorno virtual activo y en la misma carpeta del proyecto, ejecuta:

```bash
pyinstaller --onefile --icon="CronometroJW.png" CronometroJW_2.py
```

> ⚙️ Este comando empaqueta todo en un solo archivo (`--onefile`) y le asigna el ícono especificado (`--icon`).  
> PyInstaller creará una carpeta `dist/` que contendrá el ejecutable final.

---

## 🚀 Ejecutar la Aplicación

### 🅰️ Opción A — Ejecución Directa

Navega a la carpeta `dist` generada por PyInstaller:

```bash
cd dist
```

Ejecuta el programa directamente desde la terminal:

```bash
./CronometroJW_2
```

O haz doble clic sobre el archivo `CronometroJW_2` (sin extensión) desde tu explorador de archivos.

---

### 🅱️ Opción B — Instalar como Comando del Sistema (Avanzado)

Si deseas ejecutar el cronómetro desde cualquier ubicación o añadirlo a tu menú de aplicaciones:

1. Asegúrate de que exista la carpeta local de binarios:

```bash
mkdir -p ~/.local/bin
```

2. Mueve el ejecutable desde `dist` a esa carpeta:

```bash
mv dist/CronometroJW_2 ~/.local/bin/
```

3. Cierra y vuelve a abrir la terminal.  
   Ahora podrás ejecutar la aplicación escribiendo simplemente:

```bash
CronometroJW_2
```

---

### 🎨 (Opcional) Añadir al Menú de Aplicaciones

Para que aparezca en tu menú (Gnome, KDE, etc.) con su ícono, crea un archivo `.desktop` en:

```
~/.local/share/applications/
```

Ejemplo de contenido del archivo `cronometrojw.desktop`:

```ini
[Desktop Entry]
Name=Cronómetro JW
Exec=/home/tu_usuario/.local/bin/CronometroJW_2
Icon=/ruta/a/tu/proyecto/CronometroJW.png
Type=Application
Categories=Utility;
Terminal=false
```

Guarda el archivo y dale permisos de ejecución:

```bash
chmod +x ~/.local/share/applications/cronometrojw.desktop
```

---


<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python Badge">
  <img src="https://img.shields.io/badge/License-NonCommercial-green" alt="License Badge">
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Status Badge">
</p>
