class Nodo:
    def __init__(self, nombre: str, identificacion: str):
        self.nombre = nombre
        self.identificacion = identificacion
        self.turnos_atendidos = 0  # RETO 1: Contador de turnos atendidos
        self.siguiente = None      # Puntero al siguiente nodo

class ListaCircular:
    def __init__(self):
        self.cabeza = None
        self.actual = None  # Puntero al turno activo actual

    def esta_vacia(self) -> bool:
        """Verifica si la lista no contiene elementos."""
        return self.cabeza is None

    def contar(self) -> int:
        """Retorna la cantidad total de personas en la lista circular."""
        if self.esta_vacia():
            return 0

        contador = 1
        temp = self.cabeza
        while temp.siguiente != self.cabeza:
            contador += 1
            temp = temp.siguiente
        return contador

    def agregar(self, nombre: str, identificacion: str) -> bool:
        """Agrega una persona al final de la lista circular."""
        # Validar si la identificación ya existe
        if self.buscar(identificacion) is not None:
            return False

        nuevo = Nodo(nombre, identificacion)

        if self.esta_vacia():
            self.cabeza = nuevo
            self.cabeza.siguiente = self.cabeza  # Apunta a sí mismo
            self.actual = self.cabeza
        else:
            # Buscar el último nodo (aquel cuyo siguiente es la cabeza)
            temp = self.cabeza
            while temp.siguiente != self.cabeza:
                temp = temp.siguiente

            temp.siguiente = nuevo
            nuevo.siguiente = self.cabeza  # Cierre circular: Último -> Primero
        return True

    def siguiente_turno(self) -> dict | None:
        """Avanza al siguiente turno en la lista circular."""
        if self.esta_vacia():
            return None

        # Registrar atención en el nodo actual antes de cambiar
        self.actual.turnos_atendidos += 1
        self.actual = self.actual.siguiente
        return self.obtener_turno_actual()

    def anterior_turno(self) -> dict | None:
        """Retrocede al turno anterior buscando el nodo previo."""
        if self.esta_vacia():
            return None

        # Al ser lista simplemente enlazada, debemos iterar hasta encontrar el previo
        temp = self.cabeza
        while temp.siguiente != self.actual:
            temp = temp.siguiente

        self.actual = temp
        return self.obtener_turno_actual()

    def buscar(self, identificacion: str) -> dict | None:
        """Busca a una persona por su identificación."""
        if self.esta_vacia():
            return None

        temp = self.cabeza
        while True:
            if temp.identificacion == identificacion:
                return {
                    "nombre": temp.nombre,
                    "identificacion": temp.identificacion,
                    "turnos_atendidos": temp.turnos_atendidos
                }
            temp = temp.siguiente
            if temp == self.cabeza:
                break
        return None

    def eliminar(self, identificacion: str) -> bool:
        """Elimina una persona controlando todos los casos borde."""
        if self.esta_vacia():
            return False

        curr = self.cabeza
        prev = None

        # Caso A: Único nodo en la lista
        if self.cabeza.siguiente == self.cabeza:
            if self.cabeza.identificacion == identificacion:
                self.cabeza = None
                self.actual = None
                return True
            return False

        # Encontrar el último nodo para actualizar la referencia si se elimina la cabeza
        ultimo = self.cabeza
        while ultimo.siguiente != self.cabeza:
            ultimo = ultimo.siguiente

        # Buscar el nodo a eliminar
        while True:
            if curr.identificacion == identificacion:
                # Si el turno actual está sobre el nodo a eliminar, mover el turno
                if self.actual == curr:
                    self.actual = curr.siguiente

                if curr == self.cabeza:
                    # Caso B: Eliminar la Cabeza
                    self.cabeza = curr.siguiente
                    ultimo.siguiente = self.cabeza
                else:
                    # Caso C: Eliminar nodo intermedio o último
                    prev.siguiente = curr.siguiente

                return True

            prev = curr
            curr = curr.siguiente
            if curr == self.cabeza:
                break  # Recorrido completo sin encontrar

        return False

    def obtener_turno_actual(self) -> dict | None:
        if self.esta_vacia() or self.actual is None:
            return None
        return {
            "nombre": self.actual.nombre,
            "identificacion": self.actual.identificacion,
            "turnos_atendidos": self.actual.turnos_atendidos
        }

    def mostrar(self) -> list[dict]:
        """Devuelve la secuencia estructurada de nodos en orden circular."""
        elementos = []
        if self.esta_vacia():
            return elementos

        temp = self.cabeza
        while True:
            elementos.append({
                "nombre": temp.nombre,
                "identificacion": temp.identificacion,
                "turnos_atendidos": temp.turnos_atendidos,
                "es_actual": (temp == self.actual),
                "es_cabeza": (temp == self.cabeza)
            })
            temp = temp.siguiente
            if temp == self.cabeza:
                break
        return elementos

    # --- RETO DE DESARROLLO: 3 FUNCIONALIDADES ADICIONALES ---

    def agregar_con_prioridad(self, nombre: str, identificacion: str) -> bool:
        """RETO 2: Inserta una persona inmediatamente después del turno actual."""
        if self.buscar(identificacion) is not None:
            return False

        if self.esta_vacia():
            return self.agregar(nombre, identificacion)

        nuevo = Nodo(nombre, identificacion)
        nuevo.siguiente = self.actual.siguiente
        self.actual.siguiente = nuevo
        return True

    def atender_y_eliminar_actual(self) -> dict | None:
        """RETO 3: Elimina automáticamente a la persona que termina su turno."""
        if self.esta_vacia():
            return None

        atendido = self.obtener_turno_actual()
        self.eliminar(self.actual.identificacion)
        return atendido