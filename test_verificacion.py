import os
import pandas as pd
import json
from datetime import datetime
import unicodedata

print("\n===== INICIANDO PROTOCOLO DE VERIFICACIÓN =====\n")

errores = []


def normalizar(texto):
    texto = str(texto)
    texto = (
        unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    )
    return texto.lower().strip()


# Test 1: Verificar existencia de archivos
archivos_necesarios = ["turnos.csv", "tareas.csv", "config.json"]

for archivo in archivos_necesarios:
    if not os.path.exists(archivo):
        errores.append(f"ERROR: No se encontró el archivo {archivo}")

# Test 2: Verificar columnas en turnos.csv
if "turnos.csv" in archivos_necesarios and os.path.exists("turnos.csv"):
    try:
        turnos = pd.read_csv("turnos.csv", encoding="utf-8")
        columnas_turnos_normalizadas = [normalizar(col) for col in turnos.columns]
        columnas_esperadas_turnos = ["dia", "turno"]
        for columna in columnas_esperadas_turnos:
            if columna not in columnas_turnos_normalizadas:
                errores.append(
                    f"ERROR: Falta la columna '{columna}' en turnos.csv (revisar mayúsculas, tildes o escritura)"
                )
    except Exception as e:
        errores.append(f"ERROR leyendo turnos.csv: {str(e)}")

# Test 3: Verificar columnas en tareas.csv
if "tareas.csv" in archivos_necesarios and os.path.exists("tareas.csv"):
    try:
        tareas = pd.read_csv("tareas.csv", encoding="utf-8")
        columnas_tareas_normalizadas = [normalizar(col) for col in tareas.columns]
        columnas_esperadas_tareas = [
            "tarea",
            "prioridad",
            "duracion horas",
            "categoria",
        ]
        for columna in columnas_esperadas_tareas:
            if columna not in columnas_tareas_normalizadas:
                errores.append(
                    f"ERROR: Falta la columna '{columna}' en tareas.csv (revisar mayúsculas, tildes o escritura)"
                )
    except Exception as e:
        errores.append(f"ERROR leyendo tareas.csv: {str(e)}")

# Test 4: Verificar contenido de config.json
if "config.json" in archivos_necesarios and os.path.exists("config.json"):
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        if "token" not in config or "chat_id" not in config:
            errores.append("ERROR: 'token' o 'chat_id' faltan en config.json")
    except Exception as e:
        errores.append(f"ERROR leyendo config.json: {str(e)}")

# Test 5: Verificar formato de fecha en turnos.csv (ISO o Humano)
if "turnos.csv" in archivos_necesarios and os.path.exists("turnos.csv"):
    try:
        fechas = turnos["Día"] if "Día" in turnos.columns else turnos.iloc[:, 0]
        for fecha in fechas:
            fecha = str(fecha)
            try:
                # Intenta primero como formato humano DD/MM/AAAA
                datetime.strptime(fecha, "%d/%m/%Y")
            except ValueError:
                try:
                    # Si falla, intenta como formato ISO AAAA-MM-DD
                    datetime.strptime(fecha, "%Y-%m-%d")
                except ValueError:
                    errores.append(
                        f"ERROR: Fecha '{fecha}' no tiene formato válido (ni DD/MM/AAAA ni YYYY-MM-DD)"
                    )
    except Exception as e:
        errores.append(f"ERROR analizando fechas en turnos.csv: {str(e)}")

# Resultados finales
if errores:
    print("\n===== RESULTADO DE VERIFICACIÓN =====\n")
    for error in errores:
        print(error)
    print("\n===== FIN DEL PROTOCOLO CON ERRORES =====\n")
else:
    print("TODO OK: Todos los archivos y datos pasaron la verificación.\n")
    print("===== FIN DEL PROTOCOLO EXITOSO =====\n")
