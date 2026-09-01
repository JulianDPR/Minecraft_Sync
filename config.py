import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']
BASE_DIR = f'/home/{os.getlogin()}/Scripts/Python/Minecraft' if os.name != 'nt' else os.path.join(fr'C:\Users\{os.getlogin()}\Documents', 'Scripts', 'Python', 'Minecraft_Sync')
Nombre_carpeta_local = 'Sirius'
ruta_carpeta_local = f'/home/{os.getlogin()}/.var/app/io.mrarm.mcpelauncher/data/mcpelauncher/games/com.mojang/minecraftWorlds/{Nombre_carpeta_local}' if os.name != 'nt' else os.path.join(fr'C:\Users\{os.getlogin()}\AppData\Roaming\Minecraft Bedrock\Users\8553173656490203070\games\com.mojang\minecraftWorlds\{Nombre_carpeta_local}')

CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')
