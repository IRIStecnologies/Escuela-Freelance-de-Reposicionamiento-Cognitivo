from datetime import datetime
import os
import glob

# --- Configuración de proyecto ---
proyecto = "Escuela-Freelance-de-Reposicionamiento-Cognitivo"
raiz = os.getcwd()
ruta_proyecto = os.path.join(raiz, proyecto)
ruta_bitacora = os.path.join(ruta_proyecto, "bitacora")
ruta_codigo = os.path.join(ruta_proyecto, "codigo/practicas_python")

# --- Crear carpetas si no existen ---
os.makedirs(ruta_bitacora, exist_ok=True)
os.makedirs(ruta_codigo, exist_ok=True)

# --- Normalización de entradas ---
def normalizar_energia(e):
    mapa = {"a": "alto", "alto": "alto", "m": "medio", "medio": "medio", "b": "bajo", "bajo": "bajo"}
    return mapa.get(e.lower())

def normalizar_tipo(t):
    mapa = {
        "e": "estudio", "estudio": "estudio",
        "p": "proyecto", "proyecto": "proyecto",
        "r": "repaso", "repaso": "repaso",
        "o": "otro", "otro": "otro"
    }
    return mapa.get(t.lower(), t)

# --- Inputs ---
print("\n### Inicio de sesión cognitiva ###\n")

energia = normalizar_energia(input("Nivel de Energia Hoy ([Alto /a] [Medio /m] [Bajo /b]): "))
tipo = normalizar_tipo(input("Tipo de sesión ([estudio /e] [proyecto /p] [repaso /r] [otro /o]): "))

print("Contexto inicial (doble Enter para finalizar):")
lineas = []
while True:
    linea = input()
    if linea == "":
        break
    lineas.append(linea)
contexto = " ".join(lineas) if lineas else "Sin contexto declarado"

# --- Validación y guardado ---
if energia in ["alto", "medio", "bajo"]:
    ahora = datetime.now()
    fecha_txt = ahora.strftime("%Y-%m-%d %H:%M:%S")
    fecha_archivo = ahora.strftime("%Y-%m-%d")
    mes_carpeta = ahora.strftime("%Y-%m")
    
    # --- Crear carpeta del mes si no existe ---
    ruta_mes = os.path.join(ruta_bitacora, mes_carpeta)
    os.makedirs(ruta_mes, exist_ok=True)

    # --- Registro acumulativo ---
    registro = (
        f"{fecha_txt} | Energia: {energia} | Tipo de sesión: {tipo}\n"
        f"Contexto: {contexto}"
    )
    archivo_registro = os.path.join(ruta_proyecto, "Registro.txt")
    with open(archivo_registro, "a", encoding="utf-8") as f:
        f.write("\n" + "#"*90 + "\n")
        f.write(registro + "\n")

    # --- Numeración automática de sesión ---
    existentes = glob.glob(os.path.join(ruta_mes, "METADATOS_sesion_N°*_Dia_*.md"))
    numero_sesion = len(existentes) + 1
    nombre_archivo = os.path.join(ruta_mes, f"METADATOS_sesion_N°{numero_sesion}_Dia_{fecha_archivo}.md")

    # --- Contenido de metadatos ---
    contenido_md = f"""# Metadatos de Sesión {numero_sesion}

**Fecha:** {fecha_txt}  
**Energía:** {energia}  
**Tipo de sesión:** {tipo}

## Contexto
{contexto}
"""

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido_md)

    print("\n✅ Registro completo guardado.")
    print(f"Archivo de metadatos creado: {nombre_archivo}")

else:
    print("Entrada no válida para el nivel de energía.")
