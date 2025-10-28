<h1 align="center">🪟 Cronómetro JW — Instrucciones de Compilación (Windows)</h1>

<p align="center">
  Guía para compilar el proyecto <strong>CronometroJW_2.py</strong> desde el código fuente en Windows, creando un ejecutable independiente.
</p>

---

## 🧩 Prerrequisitos

Asegúrate de tener instalado lo siguiente en tu sistema:

### 🐍 Python 3
Confirma que **Python 3** está instalado y que marcaste la opción **“Add Python to PATH”** durante la instalación.

Verifica la instalación abriendo el **Símbolo del sistema (cmd)** o **PowerShell** y escribiendo:

```powershell
python --version
```

### 📦 pip
El gestor de paquetes de Python (pip) se instala automáticamente con Python 3.  
Puedes comprobarlo con:

```powershell
pip --version
```

---

## ⚙️ Pasos para Compilar

### 1️⃣ Preparar el Directorio

Abre el **Símbolo del sistema** o **PowerShell**.  
Navega hasta el directorio donde se encuentran los archivos:

- `CronometroJW_2.py`
- `CronometroJW.png` o `CronometroJW.ico`

Ejemplo en PowerShell:

```powershell
cd C:\Ruta\A\Tu\Proyecto
```

---

### 2️⃣ Instalar Dependencias

El proyecto requiere las siguientes bibliotecas:

- [`sv-ttk`](https://pypi.org/project/sv-ttk/) — para el estilo visual moderno de la interfaz.  
- [`PyInstaller`](https://pyinstaller.org/) — para crear el ejecutable.

Instálalas con los siguientes comandos:

```powershell
pip install sv-ttk
pip install pyinstaller
```

---

### 3️⃣ Compilar el Ejecutable

En el mismo directorio del archivo `.py`, ejecuta el siguiente comando para empaquetar el programa en un único archivo ejecutable con su ícono:

```powershell
pyinstaller --onefile --icon="CronometroJW.ico" CronometroJW_2.py
```

> 💡 PyInstaller creará varias carpetas; la más importante es `dist`, donde se generará el archivo final **CronometroJW_2.exe**.

---

### 4️⃣ Ejecutar la Aplicación

Una vez compilado, puedes ejecutar el programa de dos maneras:

#### 🅰️ Opción A — Ejecución Directa

1. Navega a la carpeta `dist` dentro de tu proyecto.  
2. Busca el archivo `CronometroJW_2.exe`.  
3. Haz doble clic sobre él o ejecútalo desde PowerShell:

```powershell
cd dist
.\CronometroJW_2.exe
```

---

#### 🅱️ Opción B — Ejecución Rápida (Mover el Ejecutable)

Si deseas ejecutar el cronómetro desde cualquier lugar sin navegar hasta la carpeta `dist`:

1. Copia el archivo `CronometroJW_2.exe` desde la carpeta `dist`.  
2. Pégalo en una ubicación incluida en las **variables de entorno del sistema**, por ejemplo:
   - `C:\Windows\System32`
   - o una carpeta que hayas añadido a la variable `PATH`.

Después de moverlo, podrás ejecutar el programa desde cualquier terminal:

```powershell
CronometroJW_2
```

---


<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python Badge">
  <img src="https://img.shields.io/badge/License-NonCommercial-green" alt="License Badge">
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Status Badge">
</p>
