import pandas as pd
import datetime
import requests
import json
import unicodedata

print("\n===== INICIANDO EJECUCIÓN DE AGENDA BOT V1.1 =====\n")

# Función para normalizar texto
def normalizar(texto):
    texto = str(texto)
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.lower().strip()

# Función para convertir fechas humanas a ISO
def convertir_fecha(fecha_str):
    try:
        return datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except ValueError:
            return None

# Cargar configuración
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    token = config['token']
    chat_id = config['chat_id']
except Exception as e:
    print(f"ERROR cargando config.json: {e}")
    exit()

# Cargar archivos
try:
    turnos = pd.read_csv('turnos.csv', encoding='utf-8')
    tareas = pd.read_csv('tareas.csv', encoding='utf-8')
except Exception as e:
    print(f"ERROR cargando archivos CSV: {e}")
    exit()

# Normalizar columnas
turnos.columns = [normalizar(col) for col in turnos.columns]
tareas.columns = [normalizar(col) for col in tareas.columns]

# Obtener la fecha de hoy
hoy = datetime.date.today()

# Verificar turno de hoy
turnos['fecha_normalizada'] = turnos['dia'].apply(lambda x: convertir_fecha(x))
turno_hoy = turnos[turnos['fecha_normalizada'] == hoy]

# Construir mensaje
mensaje = f"📅 Hoy es {hoy.strftime('%d/%m/%Y')}\n"

if turno_hoy.empty:
    mensaje += "⚠️ No encontré tu turno para hoy.\nRevisá el archivo de turnos."
else:
    tipo_turno = turno_hoy.iloc[0]['turno'].upper()
    if tipo_turno == 'F':
        mensaje += "🎉 Hoy tenés franco.\n\n"
        mensaje += "📝 Tareas sugeridas para hoy:\n"
        for idx, row in tareas.iterrows():
            mensaje += f"- {row['tarea']} ({row['duracion horas']} horas)\n"
    else:
        mensaje += "💼 Hoy trabajás.\n\n"
        mensaje += "📋 Checklist de trabajo:\n"
        mensaje += "- 📦 Verificar ropa de trabajo\n"
        mensaje += "- 🍱 Preparar comida para llevar\n"
        mensaje += "- 🔋 Cargar celular\n"
        mensaje += "- ⏰ Salir con tiempo\n"

# Enviar mensaje a Telegram
try:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": mensaje
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("\n✅ Mensaje enviado correctamente.")
    else:
        print(f"\n❌ Error enviando mensaje. Código: {response.status_code}")
except Exception as e:
    print(f"ERROR enviando mensaje a Telegram: {e}")

print("\n===== FIN DE LA EJECUCIÓN =====\n")
