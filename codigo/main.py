import json

archivo = "recordatorios.json"

def cargar_recordatorios():
    try:
        with open(archivo,"r") as f:
            return json.load(f)
    except:
        return []

def guardar_recordatorios(datos):
    with open(archivo,"w") as f:
        json.dump(datos,f,indent=4)

def crear_recordatorio(titulo,descripcion,fecha,hora):

    recordatorios=cargar_recordatorios()

    nuevo={
        "titulo":titulo,
        "descripcion":descripcion,
        "fecha":fecha,
        "hora":hora
    }

    recordatorios.append(nuevo)
    guardar_recordatorios(recordatorios)

def eliminar_recordatorio(indice):

    recordatorios=cargar_recordatorios()

    if indice<len(recordatorios):

        recordatorios.pop(indice)
        guardar_recordatorios(recordatorios)