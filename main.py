from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from lista_circular import ListaCircular

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lista_turnos = ListaCircular()

class PersonaDTO(BaseModel):
    nombre: str
    identificacion: str

@app.get("/estado")
def obtener_estado():
    return {
        "vacia": lista_turnos.esta_vacia(),
        "total": lista_turnos.contar(),
        "turno_actual": lista_turnos.obtener_turno_actual(),
        "personas": lista_turnos.mostrar()
    }

@app.post("/agregar")
def agregar(persona: PersonaDTO):
    if not lista_turnos.agregar(persona.nombre, persona.identificacion):
        raise HTTPException(status_code=400, detail="La identificación ya se encuentra registrada.")
    return {"mensaje": "Persona registrada exitosamente"}

@app.post("/agregar-prioridad")
def agregar_prioridad(persona: PersonaDTO):
    if not lista_turnos.agregar_con_prioridad(persona.nombre, persona.identificacion):
        raise HTTPException(status_code=400, detail="La identificación ya existe.")
    return {"mensaje": "Persona colada con prioridad en la fila"}

@app.get("/siguiente")
def siguiente():
    res = lista_turnos.siguiente_turno()
    if res is None:
        raise HTTPException(status_code=400, detail="La lista está vacía")
    return res

@app.get("/anterior")
def anterior():
    res = lista_turnos.anterior_turno()
    if res is None:
        raise HTTPException(status_code=400, detail="La lista está vacía")
    return res

@app.delete("/eliminar/{identificacion}")
def eliminar(identificacion: str):
    if not lista_turnos.eliminar(identificacion):
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return {"mensaje": "Persona eliminada correctamente"}

@app.delete("/atender-actual")
def atender_actual():
    res = lista_turnos.atender_y_eliminar_actual()
    if res is None:
        raise HTTPException(status_code=400, detail="No hay personas en la lista")
    return {"mensaje": "Persona atendida y retirada del sistema", "persona": res}

@app.get("/buscar/{identificacion}")
def buscar(identificacion: str):
    res = lista_turnos.buscar(identificacion)
    if res is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return res