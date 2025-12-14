from config.db_config import conexion_oracle
from datetime import date
from typing import Optional, List, Tuple, Any


class InsumosModel:
    def __init__(
        self,
        id_insumo: int,
        nombre: str,
        tipo: str,
        stock: int,
        costo_usd: float,
        conexion: conexion_oracle,
    ):

        self.id_insumo = id_insumo
        self.nombre = nombre
        self.tipo = tipo
        self.stock = stock
        self.costo_usd = costo_usd
        self.db = conexion

    def guardar_item(self, id_insumo: int, nombre: str, tipo: str, stock: int, costo_usd: float) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()

            consulta_validacion = "SELECT 1 FROM tv_insumos WHERE nombre = :1"
            cursor.execute(consulta_validacion, (nombre,))

            if cursor.fetchone():
                print(f"[ERROR]: Ya existe un ítem con el nombre {nombre}")
                return False

            consulta_insert = """
                INSERT INTO tv_insumos (id_insumo, nombre, tipo, stock, costo_usd)
                VALUES (:1, :2, :3, :4, :5)
            """
            cursor.execute(consulta_insert, (id_insumo, nombre, tipo, stock, costo_usd))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: {nombre} guardado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al guardar {nombre} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def editar_item(self, id_insumo: int, nombre: str, *datos: tuple) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()

            consulta_validacion = "SELECT 1 FROM tv_insumos WHERE id_insumo = :1"
            cursor.execute(consulta_validacion, (id_insumo,))

            if cursor.fetchone() is None:
                print(f"[ERROR]: {nombre} no existe en la tabla tv_insumos.")
                return False

            if not datos or len(datos) < 3:
                print(f"[ERROR]: Sin datos ingresados para {nombre} (se requiere tipo, stock, costo_usd)")
                return False

            consulta_update = "UPDATE tv_insumos SET tipo = :1, stock = :2, costo_usd = :3 WHERE id_insumo = :4"
            cursor.execute(consulta_update, (datos[0], datos[1], datos[2], id_insumo))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: {nombre} editado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al editar {nombre} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def mostrar_items(self) -> List[Tuple[Any, ...]]:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta = "SELECT id_insumo, nombre, tipo, stock, costo_usd FROM tv_insumos"
            cursor.execute(consulta)
            datos = cursor.fetchall()

            if datos:
                return datos
            else:
                print("[INFO]: Sin datos encontrados para tv_insumos.")
                return []

        except Exception as e:
            print(f"[ERROR]: Error al obtener items desde BD -> {e}")
            return []

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def eliminar_item(self, id_insumo: int) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_insumos WHERE id_insumo = :1"
            cursor.execute(consulta_validacion, (id_insumo,))

            if cursor.fetchone() is None:
                print(f"[ERROR]: El insumo con ID {id_insumo} no existe.")
                return False

            consulta_delete = "DELETE FROM tv_insumos WHERE id_insumo = :1"
            cursor.execute(consulta_delete, (id_insumo,))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Insumo con ID {id_insumo} eliminado correctamente.")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al eliminar insumo -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass


class RecetasModel:
    def __init__(
        self,
        id_receta: int,
        id_paciente: int,
        id_medico: int,
        descripcion: str,
        medicamentos_recetados: str,
        costo_clp: float,
        conexion: conexion_oracle,
    ):
        self.id_receta = id_receta
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.descripcion = descripcion
        self.medicamentos_recetados = medicamentos_recetados
        self.costo_clp = costo_clp
        self.db = conexion

    def guardar_item(
        self,
        id_receta: int,
        id_paciente: int,
        id_medico: int,
        descripcion: str,
        medicamentos_recetados: str,
        costo_clp: float,
    ) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_recetas WHERE id_receta = :1"
            cursor.execute(consulta_validacion, (id_receta,))

            if cursor.fetchone():
                print(f"[ERROR]: Ya existe un ítem con el id {id_receta}")
                return False

            consulta_insert = """
                INSERT INTO tv_recetas (id_receta, id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp)
                VALUES (:1, :2, :3, :4, :5, :6)
            """
            cursor.execute(consulta_insert, (id_receta, id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Receta folio n°{id_receta} guardada correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al guardar receta folio n°{id_receta} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def editar_item(self, id_receta: int, *datos: tuple) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_recetas WHERE id_receta = :1"
            cursor.execute(consulta_validacion, (id_receta,))

            if cursor.fetchone() is None:
                print(f"[ERROR]: Folio n°{id_receta} no existe en la tabla tv_recetas.")
                return False

            if not datos or len(datos) < 5:
                print(f"[ERROR]: Sin datos ingresados para Folio n°{id_receta} (se requiere id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp)")
                return False

            consulta_update = """
                UPDATE tv_recetas
                SET id_paciente = :1, id_medico = :2, descripcion = :3, medicamentos_recetados = :4, costo_clp = :5
                WHERE id_receta = :6
            """

            cursor.execute(consulta_update, (datos[0], datos[1], datos[2], datos[3], datos[4], id_receta))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Folio n°{id_receta} editado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al editar Folio n°{id_receta} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def mostrar_items(self) -> List[Tuple[Any, ...]]:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta = "SELECT id_receta, id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp FROM tv_recetas"
            cursor.execute(consulta)
            datos = cursor.fetchall()
            if datos:
                return datos
            else:
                print("[INFO]: Sin datos encontrados para tv_recetas.")
                return []
        except Exception as e:
            print(f"[ERROR]: Error al obtener items desde BD -> {e}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def eliminar_item(self, id_receta: int) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_recetas WHERE id_receta = :1"
            cursor.execute(consulta_validacion, (id_receta,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: Folio n°{id_receta} no existe en la tabla tv_recetas.")
                return False

            consulta_delete = "DELETE FROM tv_recetas WHERE id_receta = :1"
            cursor.execute(consulta_delete, (id_receta,))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Folio n°{id_receta} eliminado correctamente")
            return True
        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al eliminar Folio n°{id_receta} -> {e}")
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass


class ConsultasModel:
    def __init__(
        self,
        id_consulta: int,
        id_paciente: int,
        id_medico: int,
        id_receta: int,
        fecha: date,
        comentarios: str,
        valor: float,
        conexion: conexion_oracle,
    ):
        self.id = id_consulta
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.id_receta = id_receta
        self.fecha = fecha
        self.comentarios = comentarios
        self.valor = valor
        self.db = conexion

    def guardar_item(
        self,
        id_consulta: int,
        id_paciente: int,
        id_medico: int,
        id_receta: int,
        fecha: date,
        comentarios: str,
        valor: float,
    ) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_consultas WHERE id_consulta = :1"
            cursor.execute(consulta_validacion, (id_consulta,))

            if cursor.fetchone():
                print(f"[ERROR]: Ya existe un ítem con el id {id_consulta}")
                return False

            consulta_insert = """
                INSERT INTO tv_consultas (id_consulta, id_paciente, id_medico, id_receta, fecha, comentarios, valor)
                VALUES (:1, :2, :3, :4, :5, :6, :7)
            """
            cursor.execute(consulta_insert, (id_consulta, id_paciente, id_medico, id_receta, fecha, comentarios, valor))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Consulta n°{id_consulta} guardada correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al guardar consulta n°{id_consulta} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def editar_item(self, id_consulta: int, *datos: tuple) -> bool:

        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_consultas WHERE id_consulta = :1"
            cursor.execute(consulta_validacion, (id_consulta,))

            if cursor.fetchone() is None:
                print(f"[ERROR]: Consulta n°{id_consulta} no existe en la tabla tv_consultas.")
                return False

            if not datos or len(datos) < 6:
                print(f"[ERROR]: Sin datos ingresados para consulta n°{id_consulta} (se requiere id_paciente, id_medico, id_receta, fecha, comentarios, valor)")
                return False

            consulta_update = """
                UPDATE tv_consultas
                SET id_paciente = :1, id_medico = :2, id_receta = :3, fecha = :4, comentarios = :5, valor = :6
                WHERE id_consulta = :7
            """
            cursor.execute(consulta_update, (datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], id_consulta))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Consulta n°{id_consulta} editada correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al editar consulta n°{id_consulta} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def mostrar_items(self) -> List[Tuple[Any, ...]]:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta = "SELECT id_consulta, id_paciente, id_medico, id_receta, fecha, comentarios, valor FROM tv_consultas"
            cursor.execute(consulta)
            datos = cursor.fetchall()

            if datos:
                return datos
            else:
                print("[INFO]: Sin datos encontrados para tv_consultas.")
                return []

        except Exception as e:
            print(f"[ERROR]: Error al obtener items desde BD -> {e}")
            return []

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def eliminar_item(self, id_consulta: int) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_consultas WHERE id_consulta = :1"
            cursor.execute(consulta_validacion, (id_consulta,))

            if cursor.fetchone() is None:
                print(f"[ERROR]: Consulta n°{id_consulta} no existe en la tabla tv_consultas.")
                return False

            consulta_delete = "DELETE FROM tv_consultas WHERE id_consulta = :1"
            cursor.execute(consulta_delete, (id_consulta,))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Consulta n°{id_consulta} eliminada correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al eliminar consulta n°{id_consulta} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass


class AgendaModel:
    def __init__(self, id: int, id_paciente: int, id_medico: int, fecha_consulta: date, estado: str, conexion: conexion_oracle):
        self.id = id
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.fecha_consulta = fecha_consulta
        self.estado = estado
        self.db = conexion

    def guardar_item(self, id_agenda: int, id_paciente: int, id_medico: int, fecha_consulta: date, estado: str) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_agenda WHERE id_agenda = :1"
            cursor.execute(consulta_validacion, (id_agenda,))
            if cursor.fetchone():
                print(f"[ERROR]: Ya existe un ítem con el id {id_agenda}")
                return False

            consulta_insert = """
                INSERT INTO tv_agenda (id_agenda, id_paciente, id_medico, fecha_consulta, estado)
                VALUES (:1, :2, :3, :4, :5)
            """
            cursor.execute(consulta_insert, (id_agenda, id_paciente, id_medico, fecha_consulta, estado))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Agenda n°{id_agenda} guardada correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al guardar agenda n°{id_agenda} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def editar_item(self, id_agenda: int, *datos: tuple) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_agenda WHERE id_agenda = :1"
            cursor.execute(consulta_validacion, (id_agenda,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: Agenda n°{id_agenda} no existe en la tabla tv_agenda.")
                return False

            if not datos or len(datos) < 4:
                print(f"[ERROR]: Sin datos ingresados para agenda n°{id_agenda}")
                return False

            consulta_update = """
                UPDATE tv_agenda
                SET id_paciente = :1, id_medico = :2, fecha_consulta = :3, estado = :4
                WHERE id_agenda = :5
            """
            cursor.execute(consulta_update, (datos[0], datos[1], datos[2], datos[3], id_agenda))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Agenda n°{id_agenda} editada correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al editar agenda n°{id_agenda} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def mostrar_items(self) -> List[Tuple[Any, ...]]:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta = "SELECT id_agenda, id_paciente, id_medico, fecha_consulta, estado FROM tv_agenda"
            cursor.execute(consulta)
            datos = cursor.fetchall()
            if datos:
                return datos
            else:
                print("[INFO]: Sin datos encontrados para tv_agenda.")
                return []
        except Exception as e:
            print(f"[ERROR]: Error al obtener items desde BD -> {e}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def eliminar_item(self, id_agenda: int) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_agenda WHERE id_agenda = :1"
            cursor.execute(consulta_validacion, (id_agenda,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: Agenda n°{id_agenda} no existe en la tabla tv_agenda.")
                return False

            consulta_delete = "DELETE FROM tv_agenda WHERE id_agenda = :1"
            cursor.execute(consulta_delete, (id_agenda,))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Agenda n°{id_agenda} eliminada correctamente")
            return True
        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al eliminar agenda n°{id_agenda} -> {e}")
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass