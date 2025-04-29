# 📋 Agenda Bot

**Agenda Bot** es una herramienta personal que organiza automáticamente tus días, basándose en tus horarios laborales y tareas personales.

Te envía un resumen diario por Telegram que:
- Lista las tareas pendientes según tu disponibilidad (día laboral, noche laboral o franco).
- Elimina tareas completadas y reagenda las no completadas.
- Se adapta dinámicamente a tu grilla rotativa de horarios.

---

## 🛠️ Estructura del Proyecto

```
- main.py: Código principal de ejecución del bot.
- test_verificacion.py: Sistema de verificación automática de archivos y configuraciones.
- tareas.csv: Base de datos de tareas pendientes.
- turnos.csv: Grilla mensual de turnos laborales.
- .env: Variables de entorno sensibles (NO se sube al repositorio).
- .env.template: Plantilla de variables de entorno (para configurar tu propio .env).
- .gitignore: Archivos y carpetas ignoradas por Git.
- requirements.txt: Lista de dependencias de Python necesarias para correr el proyecto.
```

---

## ⚙️ Configuración Inicial

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repo>
   ```


2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el bot**:
   ```bash
   python main.py
   ```

---

## 🚀 Características
- Detección automática de día laboral, noche laboral o franco.
- Asignación dinámica de tareas por prioridad.
- Envío automático de resumen diario vía Telegram.
- Resiliencia ante errores y validaciones automáticas de archivos.

---

## 📄 Notas
- **Importante**: Si re subis este repo, NO subas tu archivo `.env` al repositorio público.
- El bot está diseñado para uso personal, pero se puede adaptar para otros escenarios.

---

## 📌 Estado Actual
- Versión: **1.1 actualizando 1.2**
- Fase: Consolidación de arquitectura Python para futura migración a Flutter (App Mobile).