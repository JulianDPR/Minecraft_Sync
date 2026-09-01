import os
import io
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from config import BASE_DIR, ruta_carpeta_local, Nombre_carpeta_local
from utils import autenticar_google_drive

if __name__ == '__main__':
    creds = autenticar_google_drive()
    service = build('drive', 'v3', credentials=creds)
    
    # ID de tu carpeta contenedora principal en Google Drive
    id_carpeta_padre_drive = '1c9rg4H_wBOYIRgXf09c8tShYLKLmGCXf'
    
    # Ruta local donde Minecraft Bedrock espera los mundos, forzando el nombre 'sirius'
    ruta_temp = os.path.join(BASE_DIR, 'output')
    os.makedirs(ruta_temp, exist_ok=True)

    print("Buscando la carpeta más reciente en Google Drive...")
    
    # Listar carpetas hijas ordenadas de la más nueva a la más antigua
    query = f"'{id_carpeta_padre_drive}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    response = service.files().list(
        q=query,
        spaces='drive',
        orderBy='createdTime desc',
        fields='files(id, name, createdTime)'
    ).execute()
    
    folders = response.get('files', [])
    
    if not folders:
        print("No se encontró ninguna carpeta de respaldo en Google Drive.")
        exit(1)
        
    # La más reciente es la primera de la lista
    carpeta_reciente = folders[0]
    print(fodler_msg := f"-> Carpeta más reciente detectada: {carpeta_reciente['name']} (Creada: {carpeta_reciente['createdTime']})")

    # Borrar el resto de carpetas antiguas en Google Drive para limpiar
    if len(folders) > 1:
        print("Limpiando carpetas de respaldo antiguas en Google Drive...")
        for folder_antigua in folders[1:]:
            print(f"   Eliminando carpeta vieja: {folder_antigua['name']} ({folder_antigua['id']})")
            try:
                service.files().delete(fileId=folder_antigua['id']).execute()
            except Exception as e:
                print(f"   No se pudo eliminar {folder_antigua['name']}: {e}")

    # Buscar el archivo .mcworld o .zip dentro de la carpeta más reciente
    q_files = f"'{carpeta_reciente['id']}' in parents and trashed = false"
    res_files = service.files().list(q=q_files, fields='files(id, name)').execute()
    archivos = res_files.get('files', [])
    
    archivo_mcworld = None
    for archivo in archivos:
        if archivo['name'].endswith('.mcworld') or archivo['name'].endswith('.zip'):
            archivo_mcworld = archivo
            break
            
    if not archivo_mcworld:
        print("Error: No se encontró ningún archivo .mcworld dentro de la última carpeta de Drive.")
        exit(1)
        
    print(f"-> Descargando archivo: {archivo_mcworld['name']}...")
    request = service.files().get_media(fileId=archivo_mcworld['id'])
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while not done:
        status, done = downloader.next_chunk()
        
    ruta_archivo_mcworld = os.path.join(ruta_temp, archivo_mcworld['name'])
    with open(ruta_archivo_mcworld, 'wb') as f:
        f.write(fh.getvalue())

    # CONVERSIÓN: Cambiar la extensión a .zip para que shutil pueda descomprimirlo
    ruta_archivo_zip = ruta_archivo_mcworld.replace('.mcworld', '.zip')
    if os.path.exists(ruta_archivo_zip):
        os.remove(ruta_archivo_zip)
    os.rename(ruta_archivo_mcworld, ruta_archivo_zip)

    # Preparar el directorio local 'sirius' limpio
    if os.path.exists(ruta_carpeta_local):
        print(f"Limpiando datos anteriores de la carpeta local '{Nombre_carpeta_local}'...")
        shutil.rmtree(ruta_carpeta_local)
    
    os.makedirs(ruta_carpeta_local, exist_ok=True)
    
    print(f"Descomprimiendo el archivo zip en la carpeta '{Nombre_carpeta_local}'...")
    shutil.unpack_archive(ruta_archivo_zip, ruta_carpeta_local)
    
    # Forzar el nombre visible dentro del juego editando levelname.txt
    ruta_levelname = os.path.join(ruta_carpeta_local, 'levelname.txt')
    with open(ruta_levelname, 'w', encoding='utf-8') as f:
        f.write(Nombre_carpeta_local)
    print(f"-> Archivo levelname.txt sobrescrito con el nombre '{Nombre_carpeta_local}'.")