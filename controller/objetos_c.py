import re
from datetime import date
from typing import Any, Dict, List

from model.objetos_m import InsumosModel, RecetasModel, ConsultasModel, AgendaModel


SUS_KEYS = [
    r";", r"--", r"/\*", r"\bOR\b", r"\bAND\b", r"\bUNION\b",
    r"\bSELECT\b", r"\bINSERT\b", r"\bUPDATE\b", r"\bDELETE\b",
    r"\bDROP\b", r"\bEXEC\b"
]
patron = re.compile("|".join(SUS_KEYS), re.IGNORECASE)


class InsumosController:
    def __init__(self, modelo: InsumosModel):
        self.modelo = modelo

    def registrar_insumo(self, id_insumo: int, nombre: str, tipo: str, stock: int, costo_usd: float) -> bool:

        if patron.search(str(nombre)) or patron.search(str(tipo)):
            print("[ERROR]: No se puede ingresar código SQL en los string.")
            return False

        try:
            id_insumo = int(id_insumo)
            stock = int(stock)
            costo_usd = float(costo_usd)
        except (ValueError, TypeError):
            print("[ERROR]: id_insumo y stock deben ser números enteros. costo_usd debe ser numérico.")
            return False

        if stock < 0:
            print("[ERROR]: Stock inválido")
            return False

        if costo_usd < 0:
            print("[ERROR]: costo_usd inválido")
            return False

        try:
            return self.modelo.guardar_item(id_insumo, nombre.strip(), tipo.strip(), stock, costo_usd)
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def editar_insumo(self, id_insumo: int, nombre: str, tipo: str, stock: int, costo_usd: float) -> bool:
        if patron.search(str(nombre)) or patron.search(str(tipo)):
            print("[ERROR]: No se puede ingresar código SQL en los string.")
            return False

        try:
            id_insumo = int(id_insumo)
            stock = int(stock)
            costo_usd = float(costo_usd)
        except (ValueError, TypeError):
            print("[ERROR]: id_insumo y stock deben ser números enteros. costo_usd debe ser numérico.")
            return False

        if stock < 0:
            print("[ERROR]: Stock inválido")
            return False

        if costo_usd < 0:
            print("[ERROR]: costo_usd inválido")
            return False

        try:

            return self.modelo.editar_item(id_insumo, nombre.strip(), tipo.strip(), stock, costo_usd)
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def eliminar_insumo(self, id_insumo: int) -> bool:
        try:
            id_insumo = int(id_insumo)
        except (ValueError, TypeError):
            print("[ERROR]: id_insumo debe ser un número entero.")
            return False

        try:
            return self.modelo.eliminar_item(id_insumo)
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def listar_insumos(self) -> List[Dict[str, Any]]:
        try:
            insumos = self.modelo.mostrar_items()
        except Exception as e:
            print("[ERROR]:", e)
            return []

        if not insumos:
            return []

        return [
            {
                "id_insumo": i[0],
                "nombre": i[1],
                "tipo": i[2],
                "stock": i[3],
                "costo_usd": i[4],
            }
            for i in insumos
        ]


class RecetasController:
    def __init__(self, modelo: RecetasModel):
        self.modelo = modelo

    def registrar_receta(self, id_receta: int, id_paciente: int, id_medico: int, descripcion: str,
                         medicamentos_recetados: str, costo_clp: float) -> bool:
        if patron.search(str(descripcion)) or patron.search(str(medicamentos_recetados)):
            print("[ERROR]: No se puede ingresar código SQL en la descripción o medicamentos.")
            return False

        try:
            id_receta = int(id_receta)
            id_paciente = int(id_paciente)
            id_medico = int(id_medico)
            costo_clp = float(costo_clp)
        except (ValueError, TypeError):
            print("[ERROR]: id_receta, id_paciente e id_medico deben ser números enteros. costo_clp debe ser numérico.")
            return False

        if costo_clp < 0:
            print("[ERROR]: costo_clp inválido")
            return False

        if not isinstance(descripcion, str) or not descripcion.strip():
            print("[ERROR]: Descripción inválida.")
            return False

        if not isinstance(medicamentos_recetados, str) or not medicamentos_recetados.strip():
            print("[ERROR]: Medicamentos recetados inválidos.")
            return False

        try:
            return self.modelo.guardar_item(id_receta, id_paciente, id_medico, descripcion.strip(),
                                            medicamentos_recetados.strip(), costo_clp)
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def editar_receta(self, id_receta: int, id_paciente: int, id_medico: int, descripcion: str,
                      medicamentos_recetados: str, costo_clp: float) -> bool:
        if patron.search(str(descripcion)) or patron.search(str(medicamentos_recetados)):
            print("[ERROR]: No se puede ingresar código SQL en la descripción o medicamentos.")
            return False

        try:
            id_receta = int(id_receta)
            id_paciente = int(id_paciente)
            id_medico = int(id_medico)
            costo_clp = float(costo_clp)
        except (ValueError, TypeError):
            print("[ERROR]: id_receta, id_paciente e id_medico deben ser números enteros. costo_clp debe ser numérico.")
            return False

        if costo_clp < 0:
            print("[ERROR]: costo_clp inválido")
            return False

        if not isinstance(descripcion, str) or not descripcion.strip():
            print("[ERROR]: Descripción inválida.")
            return False

        if not isinstance(medicamentos_recetados, str) or not medicamentos_recetados.strip():
            print("[ERROR]: Medicamentos recetados inválidos.")
            return False

        try:

            return self.modelo.editar_item(id_receta, id_paciente, id_medico, descripcion.strip(),
                                           medicamentos_recetados.strip(), costo_clp)
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def eliminar_receta(self, id_receta: int) -> bool:
        try:
            id_receta = int(id_receta)
        except (ValueError, TypeError):
            print("[ERROR]: id_receta debe ser un número entero.")
            return False

        try:
            return self.modelo.eliminar_item(id_receta)
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def listar_recetas(self) -> List[Dict[str, Any]]:
        try:
            recetas = self.modelo.mostrar_items()
        except Exception as e:
            print("[ERROR]:", e)
            return []

        if not recetas:
            return []

        return [
            {
                "id_receta": r[0],
                "id_paciente": r[1],
                "id_medico": r[2],
                "descripcion": r[3],
                "medicamentos_recetados": r[4],
                "costo_clp": r[5],
            }
            for r in recetas
        ]


class ConsultasController:
    def __init__(self, modelo: ConsultasModel):
        self.modelo = modelo

    def registrar_consulta(self, id_consulta: int, id_paciente: int, id_medico: int,
                           id_receta: int, fecha: date, comentarios: str, valor: float) -> bool:
        if patron.search(str(comentarios)):
            print("[ERROR]: No se puede ingresar código SQL en los string.")
            return False

        try:
            id_consulta = int(id_consulta)
            id_paciente = int(id_paciente)
            id_medico = int(id_medico)
            if id_receta is not None:
                id_receta = int(id_receta)
            valor = float(valor)
        except (ValueError, TypeError):
            print("[ERROR]: id_consulta, id_paciente e id_medico deben ser números enteros. valor debe ser numérico.")
            return False

        if id_consulta < 0 or id_paciente < 0 or id_medico < 0:
            print("[ERROR]: IDs inválidos (deben ser >= 0).")
            return False

        if id_receta is not None and id_receta < 0:
            print("[ERROR]: id_receta inválido")
            return False

        if not isinstance(fecha, date):
            print("[ERROR]: Fecha inválida")
            return False

        if not isinstance(comentarios, str):
            print("[ERROR]: Comentarios inválidos")
            return False

        if valor < 0:
            print("[ERROR]: Valor inválido")
            return False

        try:
            return self.modelo.guardar_item(id_consulta, id_paciente, id_medico, id_receta, fecha, comentarios.strip(), valor)
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def editar_consulta(self, id_consulta: int, id_paciente: int, id_medico: int,
                        id_receta: int, fecha: date, comentarios: str, valor: float) -> bool:
        if patron.search(str(comentarios)):
            print("[ERROR]: No se puede ingresar código SQL en los string.")
            return False

        try:
            id_consulta = int(id_consulta)
            id_paciente = int(id_paciente)
            id_medico = int(id_medico)
            if id_receta is not None:
                id_receta = int(id_receta)
            valor = float(valor)
        except (ValueError, TypeError):
            print("[ERROR]: id_consulta, id_paciente e id_medico deben ser números enteros. valor debe ser numérico.")
            return False

        if id_consulta < 0 or id_paciente < 0 or id_medico < 0:
            print("[ERROR]: IDs inválidos (deben ser >= 0).")
            return False

        if id_receta is not None and id_receta < 0:
            print("[ERROR]: id_receta inválido")
            return False

        if not isinstance(fecha, date):
            print("[ERROR]: Fecha inválida")
            return False

        if not isinstance(comentarios, str):
            print("[ERROR]: Comentarios inválidos")
            return False

        if valor < 0:
            print("[ERROR]: Valor inválido")
            return False

        try:

            return self.modelo.editar_item(id_consulta, id_paciente, id_medico, id_receta, fecha, comentarios.strip(), valor)
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def eliminar_consulta(self, id_consulta: int) -> bool:
        try:
            id_consulta = int(id_consulta)
        except (ValueError, TypeError):
            print("[ERROR]: id_consulta debe ser un número entero.")
            return False

        try:
            return self.modelo.eliminar_item(id_consulta)
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def listar_consultas(self) -> List[Dict[str, Any]]:
        try:
            consultas = self.modelo.mostrar_items()
        except Exception as e:
            print("[ERROR]:", e)
            return []

        if not consultas:
            return []

        return [
            {
                "id_consulta": c[0],
                "id_paciente": c[1],
                "id_medico": c[2],
                "id_receta": c[3],
                "fecha": c[4],
                "comentarios": c[5],
                "valor": c[6],
            }
            for c in consultas
        ]
class AgendaController:
    def __init__(self, modelo: AgendaModel):
        self.modelo = modelo

    def registrar_agenda(self, id_agenda: int, id_paciente: int, id_medico: int, fecha_consulta: date, estado: str) -> bool:
        if patron.search(str(estado)):
            print("[ERROR]: No se puede ingresar código SQL en los string.")
            return False

        try:
            id_agenda = int(id_agenda)
            id_paciente = int(id_paciente)
            id_medico = int(id_medico)
        except (ValueError, TypeError):
            print("[ERROR]: id_agenda, id_paciente e id_medico deben ser números enteros.")
            return False

        if id_agenda < 0 or id_paciente < 0 or id_medico < 0:
            print("[ERROR]: IDs inválidos (deben ser >= 0).")
            return False

        if not isinstance(fecha_consulta, date):
            print("[ERROR]: Fecha inválida")
            return False

        if not isinstance(estado, str) or not estado.strip():
            print("[ERROR]: Estado inválido")
            return False

        try:
            return self.modelo.guardar_item(id_agenda, id_paciente, id_medico, fecha_consulta, estado.strip())
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def editar_agenda(self, id_agenda: int, id_paciente: int, id_medico: int, fecha_consulta: date, estado: str) -> bool:
        if patron.search(str(estado)):
            print("[ERROR]: No se puede ingresar código SQL en los string.")
            return False

        try:
            id_agenda = int(id_agenda)
            id_paciente = int(id_paciente)
            id_medico = int(id_medico)
        except (ValueError, TypeError):
            print("[ERROR]: id_agenda, id_paciente e id_medico deben ser números enteros.")
            return False

        if id_agenda < 0 or id_paciente < 0 or id_medico < 0:
            print("[ERROR]: IDs inválidos (deben ser >= 0).")
            return False

        if not isinstance(fecha_consulta, date):
            print("[ERROR]: Fecha inválida")
            return False

        if not isinstance(estado, str) or not estado.strip():
            print("[ERROR]: Estado inválido")
            return False

        try:
            return self.modelo.editar_item(id_agenda, id_paciente, id_medico, fecha_consulta, estado.strip())
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def eliminar_agenda(self, id_agenda: int) -> bool:
        try:
            id_agenda = int(id_agenda)
        except (ValueError, TypeError):
            print("[ERROR]: id_agenda debe ser un número entero.")
            return False

        try:
            return self.modelo.eliminar_item(id_agenda)
        except Exception as e:
            print("[ERROR]:", e)
            return False

    def listar_agendas(self) -> List[Dict[str, Any]]:
        try:
            agendas = self.modelo.mostrar_items()
        except Exception as e:
            print("[ERROR]:", e)
            return []

        if not agendas:
            return []

        return [
            {
                "id_agenda": a[0],
                "id_paciente": a[1],
                "id_medico": a[2],
                "fecha_consulta": a[3],
                "estado": a[4],
            }
            for a in agendas
        ]