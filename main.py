import pandas as pd
import datetime
import requests
import json

# Cargar configuración del archivo config.json
with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config['token']
CHAT_ID = config['chat_id']

# Función para mandar mensaje a Telegram
def enviar_mensaje(texto):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': texto}
    requests.post(url, data=payload)

# Cargar turnos y tareas
turnos = pd.read_csv('turnos.csv')
tareas = pd.read_csv('tareas.csv')

# Detectar fecha de hoy
hoy = datetime.datetime.now().date()

# Buscar turno de hoy
turno_hoy = turnos[turnos['Día'] == str(hoy)]

mensaje = ""

if not turno_hoy.empty:
    tipo_turno = turno_hoy.iloc[0]['Turno']

    if tipo_turno == 'F':
        # Día libre, ver tareas
        tareas_disponibles = tareas[tareas['Prioridad'].isin(['Alta', 'Media'])]

        if not tareas_disponibles.empty:
            mensaje = f"Hoy {hoy} estás de FRANCO.\nTareas sugeridas:\n"
            for idx, tarea in tareas_disponibles.iterrows():
                mensaje += f"- {tarea['Tarea']} ({tarea['Duración Horas']}h)\n"
        else:
            mensaje = f"Hoy {hoy} estás de franco, pero no hay tareas pendientes.\n¡Disfrutá!"
    else:
        mensaje = f"Hoy {hoy} tenés turno: {tipo_turno}. ¡A meterle fuerza!"
else:
    mensaje = f"No encontré tu turno para hoy {hoy}. Revisá el archivo de turnos."

# Mandar el mensaje a Telegram
enviar_mensaje(mensaje)

# Confirmación
print("Mensaje enviado correctamente.")
