# Minecraft Bedrock - Google Drive Sync

Herramienta de automatización multiplataforma en Python para sincronizar y respaldar tu mundo de Minecraft Bedrock (configurable mediante `Nombre_carpeta_local`, originalmente "Sirius") directamente con **Google Drive**.

Permite descargar automáticamente la última versión del mundo guardada en la nube al iniciar una sesión de juego, así como empaquetar y subir los progresos actualizados al finalizar.

---

## 🚀 Características

* **Compatibilidad Multiplataforma:** Detecta automáticamente si el sistema operativo es Linux (Flatpak / mcpelauncher) o Windows, ajustando las rutas de instalación y carpetas locales.
* **Nombre de Mundo Dinámico:** Utiliza la variable `Nombre_carpeta_local` para adaptar los scripts a cualquier mundo que desees sincronizar sin tener que editar la lógica principal.
* **Descarga y Extracción Automatizada (`load.py`):**
  * Identifica la última versión/carpeta del respaldo en Google Drive.
  * Descarga el archivo `.mcworld` o `.zip`.
  * Limpia la instalación anterior del mundo local e instala la copia más reciente.
  * Fuerza el nombre legible dentro del menú del juego reescribiendo el archivo `levelname.txt` con el valor de `Nombre_carpeta_local`.
* **Respaldo y Carga a la Nube (`save.py`):**
  * Comprime el directorio local del mundo en un archivo `.mcworld`.
  * Elimina versiones y respaldos obsoletos en Google Drive para optimizar el almacenamiento.
  * Sube la copia más actualizada a la carpeta especificada de Drive.
* **Gestión de Autenticación (`utils.py`):**
  * Maneja el flujo OAuth2 con Google API Client.
  * Reutiliza tokens de sesión persistentes (`token.json`) y renueva credenciales caducadas automáticamente.

---

## 📁 Estructura del Proyecto

```text
Minecraft_Sync/
├── config.py         # Configuración de rutas según SO (Linux/Windows), constantes y Nombre_carpeta_local
├── utils.py          # Autenticación y credenciales de Google Drive API
├── load.py           # Script para descargar y restaurar la copia del mundo desde Drive
├── save.py           # Script para empaquetar y subir el mundo local a Drive
├── credentials.json  # Credenciales de Google API Client (generadas en Google Cloud Console)
└── token.json        # Token de autenticación guardado tras el primer inicio de sesión
```

---

## 🛠️ Requisitos e Instalación

### 1. Requisitos Previos

* **Python 3.8+**
* Una cuenta de Google con un proyecto activo en [Google Cloud Console](https://console.cloud.google.com/).
* **Google Drive API** habilitada en la consola de desarrolladores.

### 2. Dependencias de Python

Instala los paquetes necesarios ejecutando:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3. Configuración de API de Google

1. Ve a Google Cloud Console y crea un cliente de tipo **Desktop Application**.
2. Descarga las credenciales en formato JSON y guárdalas en la raíz del proyecto con el nombre `credentials.json`.

---

## 💻 Uso

### Descargar la última copia del mundo (Antes de jugar)

```bash
python load.py
```
> Busca el último respaldo en Google Drive, lo descarga, descomprime y actualiza la carpeta local de tu mundo.

### Respaldar el mundo local en la nube (Al terminar de jugar)

```bash
python save.py
```
> Embala el directorio del mundo, elimina copias antiguas en Drive y sube la versión más reciente.

---

## ⚙️ Configuración Personalizada (`config.py`)

El archivo `config.py` es el núcleo de las personalizaciones. Aquí puedes ajustar:
* `Nombre_carpeta_local`: Define el nombre de la carpeta y del mundo (ej. `"Sirius"`). Si decides sincronizar otro mundo, simplemente cambia esta variable.
* Si tus rutas de instalación de Minecraft Bedrock son distintas, puedes ajustar `BASE_DIR` y `ruta_carpeta_local`.
* No olvides configurar los ID de las carpetas de Drive (`id_carpeta_padre_drive`) dentro de `load.py` y `save.py`.