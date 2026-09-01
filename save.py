import os
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import BASE_DIR, ruta_carpeta_local, Nombre_carpeta_local
from utils import autenticar_google_drive

if __name__ == '__main__':
    creds = autenticar_google_drive()
    service = build('drive', 'v3', credentials=creds)
    
    # ID de tu carpeta contenedora principal en Google Drive
    id_carpeta_padre_drive = '1VBfr7y9K-8vdXd2e7y8y7l8CZqOw-QCV' 
    
    # 1. Limpiar únicamente los respaldos anteriores generados por el script (evita errores 403 con carpetas ajenas)
    print("Buscando y eliminando respaldos anteriores de Minecraft en Google Drive...")
    query = f"'{id_carpeta_padre_drive}' in parents and (name contains 'backup_{Nombre_carpeta_local}_' or name contains '.mcworld') and trashed = false"
    response = service.files().list(q=query, fields='files(id, name)').execute()
    archivos_antiguos = response.get('files', [])
    
    for archivo in archivos_antiguos:
        print(f"   -> Eliminando de Drive: {archivo['name']} ({archivo['id']})")
        try:
            service.files().delete(fileId=archivo['id']).execute()
        except Exception as e:
            print(f"   No se pudo eliminar {archivo['name']}: {e}")

    # Ruta local fija de tu mundo 'sirius'
    ruta_temporal = os.path.join(BASE_DIR, 'output')
    os.makedirs(ruta_temporal, exist_ok=True)
    
    if not os.path.exists(ruta_carpeta_local):
        print(f"Error: La carpeta local del mundo '{Nombre_carpeta_local}' no existe en: {ruta_carpeta_local}")
        exit(1)

    print(f"Empaquetando el mundo '{Nombre_carpeta_local}' local...")
    archivo_zip_base = os.path.join(ruta_temporal, f'{Nombre_carpeta_local}_backup')
    
    # Limpiar zip anterior temporal si existe
    if os.path.exists(archivo_zip_base + '.zip'):
        os.remove(archivo_zip_base + '.zip')
        
    shutil.make_archive(archivo_zip_base, 'zip', ruta_carpeta_local)
    
    zip_file = archivo_zip_base + ".zip"
    mcworld_file = os.path.join(ruta_temporal, f'{Nombre_carpeta_local}.mcworld')

    if os.path.exists(mcworld_file):
        os.remove(mcworld_file)

    os.rename(zip_file, mcworld_file)
    
    print(f"Subiendo '{Nombre_carpeta_local}.mcworld' limpio a Google Drive...")
    media = MediaFileUpload(mcworld_file, resumable=True)
    file_metadata = {
        'name': f'{Nombre_carpeta_local}.mcworld',
        'parents': [id_carpeta_padre_drive]
    }
    
    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    print(f"¡Proceso finalizado! Google Drive ha sido limpiado de respaldos viejos y el nuevo mundo '{Nombre_carpeta_local}.mcworld' se subió con éxito.")