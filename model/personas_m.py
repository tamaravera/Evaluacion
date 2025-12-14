from config.db_config import conexion_oracle
from datetime import date
from typing import Optional, List, Tuple, Any


class UsuarioModel:
    def __init__(
        self,
        id_usuario: int,
        nombre_usuario: str,
        clave: str,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        telefono: str,
        email: str,
        tipo: str,
        conexion: conexion_oracle,
    ):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.clave = clave
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.email = email
        self.tipo = tipo
        self.db = conexion

    def guardar_item(
        self,
        id_usuario: int,
        nombre_usuario: str,
        clave: str,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        telefono: str,
        email: str,
        tipo: str,
    ) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_usuario WHERE id_usuario = :1 OR nombre_usuario = :2"
            cursor.execute(consulta_validacion, (id_usuario, nombre_usuario))

            if cursor.fetchone():
                print(f"[ERROR]: Ya existe un usuario con id {id_usuario} o nombre_usuario {nombre_usuario}")
                return False

            consulta_insert = """
                INSERT INTO tv_usuario (
                    id_usuario, nombre_usuario, clave, nombre, apellido,
                    fecha_nacimiento, telefono, email, tipo
                ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
            """
            cursor.execute(
                consulta_insert,
                (
                    id_usuario,
                    nombre_usuario,
                    clave,
                    nombre,
                    apellido,
                    fecha_nacimiento,
                    telefono,
                    email,
                    tipo,
                ),
            )
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Usuario {nombre_usuario} (id {id_usuario}) guardado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al guardar usuario {nombre_usuario} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def crear(self, *args, **kwargs) -> bool:
        return self.guardar_item(*args, **kwargs)

    def editar_item(self, id_usuario: int, *datos: tuple) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_usuario WHERE id_usuario = :1"
            cursor.execute(consulta_validacion, (id_usuario,))

            if cursor.fetchone() is None:
                print(f"[ERROR]: Usuario id {id_usuario} no existe en la tabla tv_usuario.")
                return False

            if not datos or len(datos) < 8:
                print(f"[ERROR]: Sin datos ingresados para usuario id {id_usuario} (se requieren 8 campos).")
                return False

            consulta_update = """
                UPDATE tv_usuario
                SET nombre_usuario = :1, clave = :2, nombre = :3, apellido = :4,
                    fecha_nacimiento = :5, telefono = :6, email = :7, tipo = :8
                WHERE id_usuario = :9
            """
            cursor.execute(
                consulta_update,
                (
                    datos[0],
                    datos[1],
                    datos[2],
                    datos[3],
                    datos[4],
                    datos[5],
                    datos[6],
                    datos[7],
                    id_usuario,
                ),
            )
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Usuario id {id_usuario} editado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al editar usuario id {id_usuario} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def editar(self, id_usuario: int, *datos: tuple) -> bool:
        return self.editar_item(id_usuario, *datos)

    def mostrar_items(self) -> List[Tuple[Any, ...]]:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta = """
                SELECT
                    id_usuario, nombre_usuario, nombre, apellido,
                    fecha_nacimiento, telefono, email, tipo
                FROM tv_usuario
            """
            cursor.execute(consulta)
            datos = cursor.fetchall()
            if datos:
                return datos
            else:
                print("[INFO]: Sin datos encontrados para tv_usuario.")
                return []
        except Exception as e:
            print(f"[ERROR]: Error al obtener usuarios desde BD -> {e}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass


    def mostrar_todos(self) -> List[Tuple[Any, ...]]:
        return self.mostrar_items()

    def eliminar_item(self, id_usuario: int) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_usuario WHERE id_usuario = :1"
            cursor.execute(consulta_validacion, (id_usuario,))

            if cursor.fetchone() is None:
                print(f"[ERROR]: Usuario id {id_usuario} no existe en la tabla tv_usuario.")
                return False

            consulta_delete = "DELETE FROM tv_usuario WHERE id_usuario = :1"
            cursor.execute(consulta_delete, (id_usuario,))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Usuario id {id_usuario} eliminado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al eliminar usuario id {id_usuario} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def eliminar(self, id_usuario: int) -> bool:
        return self.eliminar_item(id_usuario)


class PacienteModel(UsuarioModel):

    def __init__(
        self,
        id_usuario: int,
        nombre_usuario: str,
        clave: str,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        telefono: str,
        email: str,
        tipo: str,
        conexion: conexion_oracle,
    ):
        super().__init__(
            id_usuario,
            nombre_usuario,
            clave,
            nombre,
            apellido,
            fecha_nacimiento,
            telefono,
            email,
            tipo,
            conexion,
        )
        self.id_paciente = id_usuario

    def guardar_item(self, id_paciente: int, comuna: str, fecha_primera_visita: date) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            # validar que exista usuario
            consulta_usuario = "SELECT 1 FROM tv_usuario WHERE id_usuario = :1"
            cursor.execute(consulta_usuario, (id_paciente,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: No existe usuario con id {id_paciente} en tv_usuario; crear usuario antes de asignar paciente.")
                return False

            consulta_validacion = "SELECT 1 FROM tv_paciente WHERE id_paciente = :1"
            cursor.execute(consulta_validacion, (id_paciente,))
            if cursor.fetchone():
                print(f"[ERROR]: Ya existe un paciente con id {id_paciente}")
                return False

            consulta_insert = """
                INSERT INTO tv_paciente (id_paciente, comuna, fecha_primera_visita)
                VALUES (:1, :2, :3)
            """
            cursor.execute(consulta_insert, (id_paciente, comuna, fecha_primera_visita))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Paciente id {id_paciente} guardado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al guardar paciente id {id_paciente} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def crear(self, id_paciente: int, comuna: str, fecha_primera_visita: date) -> bool:
        return self.guardar_item(id_paciente, comuna, fecha_primera_visita)

    def editar_item(self, id_paciente: int, *datos: tuple) -> bool:

        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_paciente WHERE id_paciente = :1"
            cursor.execute(consulta_validacion, (id_paciente,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: Paciente id {id_paciente} no existe en la tabla tv_paciente.")
                return False

            if not datos or len(datos) < 2:
                print(f"[ERROR]: Sin datos ingresados para paciente id {id_paciente} (se requieren comuna y fecha_primera_visita).")
                return False

            consulta_update = "UPDATE tv_paciente SET comuna = :1, fecha_primera_visita = :2 WHERE id_paciente = :3"
            cursor.execute(consulta_update, (datos[0], datos[1], id_paciente))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Paciente id {id_paciente} editado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al editar paciente id {id_paciente} -> {e}")
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
            consulta = "SELECT id_paciente, comuna, fecha_primera_visita FROM tv_paciente"
            cursor.execute(consulta)
            datos = cursor.fetchall()
            if datos:
                return datos
            else:
                print("[INFO]: Sin datos encontrados para tv_paciente.")
                return []
        except Exception as e:
            print(f"[ERROR]: Error al obtener pacientes desde BD -> {e}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def mostrar_todos_completo(self) -> List[Tuple[Any, ...]]:

        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta = """
                SELECT
                    u.id_usuario,
                    u.nombre_usuario,
                    u.clave,
                    u.nombre,
                    u.apellido,
                    u.fecha_nacimiento,
                    u.telefono,
                    u.email,
                    u.tipo,
                    p.comuna,
                    p.fecha_primera_visita
                FROM tv_paciente p
                JOIN tv_usuario u ON p.id_paciente = u.id_usuario
            """
            cursor.execute(consulta)
            datos = cursor.fetchall()
            if datos:
                return datos
            else:
                print("[INFO]: Sin datos encontrados para pacientes completos.")
                return []
        except Exception as e:
            print(f"[ERROR]: Error al obtener pacientes completos desde BD -> {e}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def eliminar_item(self, id_paciente: int) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_paciente WHERE id_paciente = :1"
            cursor.execute(consulta_validacion, (id_paciente,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: Paciente id {id_paciente} no existe en tv_paciente.")
                return False

            consulta_delete = "DELETE FROM tv_paciente WHERE id_paciente = :1"
            cursor.execute(consulta_delete, (id_paciente,))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Paciente id {id_paciente} eliminado correctamente")
            return True
        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al eliminar paciente id {id_paciente} -> {e}")
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass


class MedicoModel(UsuarioModel):

    def __init__(
        self,
        id_usuario: int,
        nombre_usuario: str,
        clave: str,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        telefono: str,
        email: str,
        tipo: str,
        conexion: conexion_oracle,
    ):
        super().__init__(
            id_usuario,
            nombre_usuario,
            clave,
            nombre,
            apellido,
            fecha_nacimiento,
            telefono,
            email,
            tipo,
            conexion,
        )
        self.id_medico = id_usuario

    def guardar_item(self, id_medico: int, especialidad: str, horario_atencion: date, fecha_ingreso: date) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()

            consulta_usuario = "SELECT 1 FROM tv_usuario WHERE id_usuario = :1"
            cursor.execute(consulta_usuario, (id_medico,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: No existe usuario con id {id_medico} en tv_usuario; crear usuario antes de asignar médico.")
                return False

            consulta_validacion = "SELECT 1 FROM tv_medico WHERE id_medico = :1"
            cursor.execute(consulta_validacion, (id_medico,))
            if cursor.fetchone():
                print(f"[ERROR]: Ya existe un médico con id {id_medico}")
                return False

            consulta_insert = """
                INSERT INTO tv_medico (id_medico, especialidad, horario_atencion, fecha_ingreso)
                VALUES (:1, :2, :3, :4)
            """
            cursor.execute(consulta_insert, (id_medico, especialidad, horario_atencion, fecha_ingreso))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Médico id {id_medico} guardado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al guardar médico id {id_medico} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def crear(self, id_medico: int, especialidad: str, horario_atencion: date, fecha_ingreso: date) -> bool:
        return self.guardar_item(id_medico, especialidad, horario_atencion, fecha_ingreso)

    def editar_item(self, id_medico: int, *datos: tuple) -> bool:
        """
        datos expected: (especialidad, horario_atencion, fecha_ingreso)
        """
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_medico WHERE id_medico = :1"
            cursor.execute(consulta_validacion, (id_medico,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: Médico id {id_medico} no existe en la tabla tv_medico.")
                return False

            if not datos or len(datos) < 3:
                print(f"[ERROR]: Sin datos ingresados para médico id {id_medico} (se requieren especialidad, horario_atencion, fecha_ingreso).")
                return False

            consulta_update = "UPDATE tv_medico SET especialidad = :1, horario_atencion = :2, fecha_ingreso = :3 WHERE id_medico = :4"
            cursor.execute(consulta_update, (datos[0], datos[1], datos[2], id_medico))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Médico id {id_medico} editado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al editar médico id {id_medico} -> {e}")
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
            consulta = "SELECT id_medico, especialidad, horario_atencion, fecha_ingreso FROM tv_medico"
            cursor.execute(consulta)
            datos = cursor.fetchall()
            if datos:
                return datos
            else:
                print("[INFO]: Sin datos encontrados para tv_medico.")
                return []
        except Exception as e:
            print(f"[ERROR]: Error al obtener médicos desde BD -> {e}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def mostrar_todos_completo(self) -> List[Tuple[Any, ...]]:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta = """
                SELECT
                    u.id_usuario,
                    u.nombre_usuario,
                    u.clave,
                    u.nombre,
                    u.apellido,
                    u.fecha_nacimiento,
                    u.telefono,
                    u.email,
                    u.tipo,
                    m.especialidad,
                    m.horario_atencion,
                    m.fecha_ingreso
                FROM tv_medico m
                JOIN tv_usuario u ON m.id_medico = u.id_usuario
            """
            cursor.execute(consulta)
            datos = cursor.fetchall()
            if datos:
                return datos
            else:
                print("[INFO]: Sin datos encontrados para médicos completos.")
                return []
        except Exception as e:
            print(f"[ERROR]: Error al obtener médicos completos desde BD -> {e}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def eliminar_item(self, id_medico: int) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_medico WHERE id_medico = :1"
            cursor.execute(consulta_validacion, (id_medico,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: Médico id {id_medico} no existe en tv_medico.")
                return False

            consulta_delete = "DELETE FROM tv_medico WHERE id_medico = :1"
            cursor.execute(consulta_delete, (id_medico,))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Médico id {id_medico} eliminado correctamente")
            return True
        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al eliminar médico id {id_medico} -> {e}")
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass


class AdministradorModel(UsuarioModel):

    def __init__(
        self,
        id_usuario: int,
        nombre_usuario: str,
        clave: str,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        telefono: str,
        email: str,
        tipo: str,
        conexion: conexion_oracle,
    ):
        super().__init__(
            id_usuario,
            nombre_usuario,
            clave,
            nombre,
            apellido,
            fecha_nacimiento,
            telefono,
            email,
            tipo,
            conexion,
        )
        self.id_administrador = id_usuario

    def guardar_item(self, id_administrador: Optional[int] = None) -> bool:
        cursor = None
        id_admin = id_administrador if id_administrador is not None else self.id_administrador
        try:
            cursor = self.db.obtener_cursor()

            consulta_usuario = "SELECT 1 FROM tv_usuario WHERE id_usuario = :1"
            cursor.execute(consulta_usuario, (id_admin,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: No existe usuario con id {id_admin} en tv_usuario; crear usuario antes de asignar administrador.")
                return False

            consulta_validacion = "SELECT 1 FROM tv_administrador WHERE id_administrador = :1"
            cursor.execute(consulta_validacion, (id_admin,))
            if cursor.fetchone():
                print(f"[ERROR]: Ya existe un administrador con id {id_admin}")
                return False

            consulta_insert = "INSERT INTO tv_administrador (id_administrador) VALUES (:1)"
            cursor.execute(consulta_insert, (id_admin,))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Administrador id {id_admin} guardado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al guardar administrador id {id_admin} -> {e}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    def crear(self, id_administrador: Optional[int] = None) -> bool:
        return self.guardar_item(id_administrador)

    def eliminar_item(self, id_administrador: int) -> bool:
        cursor = None
        try:
            cursor = self.db.obtener_cursor()
            consulta_validacion = "SELECT 1 FROM tv_administrador WHERE id_administrador = :1"
            cursor.execute(consulta_validacion, (id_administrador,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: Administrador id {id_administrador} no existe en tv_administrador.")
                return False

            consulta_delete = "DELETE FROM tv_administrador WHERE id_administrador = :1"
            cursor.execute(consulta_delete, (id_administrador,))
            if self.db.connection:
                self.db.connection.commit()
            print(f"[INFO]: Administrador id {id_administrador} eliminado correctamente")
            return True

        except Exception as e:
            if self.db.connection:
                try:
                    self.db.connection.rollback()
                except Exception:
                    pass
            print(f"[ERROR]: Error al eliminar administrador id {id_administrador} -> {e}")
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
            consulta = """
                SELECT a.id_administrador,
                       u.nombre_usuario,
                       u.nombre,
                       u.apellido,
                       u.fecha_nacimiento,
                       u.telefono,
                       u.email,
                       u.tipo
                FROM tv_administrador a
                JOIN tv_usuario u ON a.id_administrador = u.id_usuario
            """
            cursor.execute(consulta)
            datos = cursor.fetchall()
            if datos:
                return datos
            else:
                print("[INFO]: Sin datos encontrados para tv_administrador.")
                return []
        except Exception as e:
            print(f"[ERROR]: Error al obtener administradores desde BD -> {e}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass