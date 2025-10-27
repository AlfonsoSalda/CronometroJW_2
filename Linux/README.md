Cronómetro JW - Instrucciones de Compilación (Linux)
Esta guía explica cómo compilar el proyecto CronometroJW_2.py desde el código fuente en un sistema operativo Linux.

Prerrequisitos
Python 3: Asegúrate de tener Python 3 instalado.

python3 --version
pip: El gestor de paquetes de Python.
venv: El módulo de entornos virtuales de Python (generalmente incluido y opcional dependiendo de tu distribuciòn).

Pasos para Compilar
1. Preparar el Entorno
Abre una terminal y navega hasta el directorio donde se encuentra el archivo CronometroJW_2.py y el icono CronometroJW.png.

Crea un entorno virtual para instalar las dependencias de forma aislada. Esto es una buena práctica y evita conflictos con otros proyectos.

Bash:
python3 -m venv venv

Activa el entorno virtual:
Bash:
source venv/bin/activate
(Notarás que el nombre de tu terminal cambia, indicando que el entorno venv está activo).

2. Instalar Dependencias
El proyecto requiere la biblioteca sv-ttk para el estilo visual. Instálala con pip:

Bash:
pip install sv-ttk

Necesitarás PyInstaller para convertir el script en un ejecutable. Instálalo también:

Bash:
pip install pyinstaller

3. Compilar el Ejecutable
Estando en la misma carpeta (y con el entorno venv activado), ejecuta el siguiente comando para crear el ejecutable.
Este comando empaquetará todo en un solo archivo (--onefile) y le asignará el icono (--icon) que se encuentra en esta misma carpeta.

Bash:
pyinstaller --onefile --icon="CronometroJW.png" CronometroJW_2.py
PyInstaller trabajará por unos momentos y creará varias carpetas. Tu aplicación final se encontrará dentro de la carpeta dist.

Ejecutar la Aplicación
Una vez compilado, tienes dos formas principales de ejecutar tu cronómetro:

Opción A: Ejecución Directa
Navega a la carpeta dist que se acaba de crear:

Bash:
cd dist
Puedes hacer doble clic sobre el archivo CronometroJW_2 (que no tendrá extensión) desde tu explorador de archivos para abrirlo.

O bien, ejecutarlo desde la terminal:

Bash:
./CronometroJW_2
Opción B: (Avanzado) Instalar como Comando del Sistema
Si deseas poder abrir tu aplicación desde cualquier terminal o añadirla a tu menú de aplicaciones (como neofetch), sigue estos pasos:

Mueve el ejecutable a tu carpeta local de binarios:

Bash:
(Asegúrate de que la carpeta exista primero)
mkdir -p ~/.local/bin

(Mueve el ejecutable desde la carpeta dist)
mv dist/CronometroJW_2 ~/.local/bin/
Cierra y vuelve a abrir tu terminal. Ahora deberías poder ejecutar la aplicación simplemente escribiendo:

Bash:
CronometroJW_2
Para el icono del menú: Para que aparezca en tu menú de aplicaciones (Gnome, KDE, etc.) con su icono, necesitarás crear un archivo .desktop en la carpeta ~/.local/share/applications/.