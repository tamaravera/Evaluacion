from config.configdb import conexion_oracle
from datetime import date
class UsuarioModel: 
    def __init__(self, conexion: conexion_oracle):
        self.db = conexion

    def crear(self, id_usuario: int, nombre_usuario: str, clave: str, nombre: str, apellido: str,
                fecha_nacimiento: date, telefono: int, email: str, tipo: str) -> bool:
        
        cursor = self.db.obtener_cursor()
        consulta ="insert into tv_usuario (id_usuario, nombre_usuario, clave, nombre, apellido, fecha_nacimiento, telefono, email, tipo) values (:1, :2, :3, :4, :5, :6, :7, :8, :9)"

        try:
            cursor.execute(consulta, (id_usuario, nombre_usuario, clave, nombre, apellido, fecha_nacimiento, telefono, email, tipo))
            self.db.connection.commit()
            print(f"[INFO]: Usuario {nombre_usuario} insertado correctamente.")
            return True
        
        except Exception as e:
            print(f"[ERROR]: No se pudo insertar usuario → {e}")

            return False
        finally:
            if cursor:
                cursor.close()

    def editar_usuario(self, id_usuario: int, nombre_usuario: str, *datos: tuple) -> bool:   
        
        if len(datos) < 7:
            print("[ERROR]: Cantidad insuficiente de datos para editar usuario.")
            return False
        
        clave, nombre, apellido, fecha_nacimiento, telefono, email, tipo = datos
        
        cursor = self.db.obtener_cursor()

        try:
            cursor.execute("SELECT 1 FROM tv_usuario WHERE id_usuario = :1", (id,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: Usuario con ID {id_usuario} no existe.")
                return False
        
            consulta_update = "update tv_usuario set nombre_usuario = :1, clave = :2, nombre = :3," \
            "apellido = :4,fecha_nacimiento = :5,telefono = :6,email = :7,tipo = :8 WHERE id_usuario = :9 "

            cursor.execute(consulta_update, (nombre_usuario, clave ,nombre ,apellido , fecha_nacimiento, telefono, email, tipo, id_usuario))
        
            self.db.connection.commit()
            print(f"[INFO]: Usuario {nombre_usuario} editado correctamente.")
            return True
        
        except Exception as e:
            print(f"[ERROR]: Error al editar usuario-> {e}")
            self.db.connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()

    def mostrar_todos(self) -> list:

        cursor = self.db.obtener_cursor()

        consulta = "select id_usuario, nombre_usuario, nombre, apellido, fecha_nacimiento, telefono," \
        " email, tipo from tv_usuario"

        try:
            cursor.execute(consulta)
            datos = cursor.fetchall()
            print("[INFO]: Usuarios obtenidos correctamente.")
            return datos
        
        except Exception as e:
            print(f"[ERROR]: Error al obtener usuarios -> {e}")
            return[]
        
        finally:
            if cursor:
                cursor.close()

class PacienteModel(UsuarioModel):
    def __init__(self, conexion: conexion_oracle):
        super().__init__(conexion)
        
    def crear(self, id_paciente: int, nombre_usuario: str, clave: str, nombre: str, apellido: str,
                fecha_nacimiento: date, telefono: int, email: str, tipo: str, comuna: str,
                fecha_primera_visita: date) -> bool:

        if not super().crear(id_paciente, nombre_usuario, clave, nombre, apellido, fecha_nacimiento, telefono, email, tipo):
            return False

        cursor = self.db.obtener_cursor()
        consulta = "insert into tv_paciente(id_paciente, comuna, fecha_primera_visita) values (:1, :2, :3)"

        try:
            cursor.execute(consulta,(id_paciente, comuna, fecha_primera_visita))
            self.db.connection.commit()
            print(f"[INFO]: Paciente '{nombre_usuario}' insertado correctamente.")
            return True
        
        except Exception as e:
            print(f"[ERROR]: No se pudo insertar -> {e}")
            self.db.connection.rollback()
            return False
        
        finally:
            if cursor:
                cursor.close()

    def mostrar_todos_completo(self):
        cursor = self.db.obtener_cursor()
        try:
            consulta = "SELECT u.id_usuario, u.nombre_usuario, u.clave, u.nombre, u.apellido," \
            " u.fecha_nacimiento, u.telefono, u.email, u.tipo, p.comuna, p.fecha_primera_visita" \
            " FROM tv_usuario u JOIN tv_paciente p ON u.id_usuario = p.id_paciente"
            cursor.execute(consulta)
            print("[INFO]: Pacientes obtenidos correctamente.")

            return cursor.fetchall()
        finally:
            cursor.close()

    def editar_paciente(self, id_paciente: int, nombre_usuario: str, *datos: tuple) -> bool:

        if len(datos) < 9:
            print("[ERROR]: Cantidad de datos insuficiente para editar un paciente.")
            return False
        
        if not super().editar_usuario(id_paciente, nombre_usuario, *datos[:7]):
            return False
        

        cursor = self.db.obtener_cursor()

        try: 
            consulta_validacion = "select 1 from tv_paciente where id_paciente = :1" 
            cursor.execute(consulta_validacion,(id_paciente,))

            if cursor.fetchone() is None:
                print(f"[ERROR]: Paciente con ID {id_paciente} no existe.")
                return False
            
            comuna = datos[7]
            fecha_primera_visita = datos[8]

            consulta_update = "update tv_paciente set comuna = :1, fecha_primera_visita = :2 where id_paciente = :3 "

            cursor.execute(consulta_update,(comuna, fecha_primera_visita, id_paciente))

            self.db.connection.commit()
            print(f"[INFO]: Paciente {nombre_usuario} editado correctamente.")
            return True
        
        except Exception as e:
            print(f"[ERROR]: Error al editar paciente -> {e}")
            self.db.connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()

    def mostrar_todos(self) -> list:

        cursor = self.db.obtener_cursor()

        consulta = "select u.id_usuario, u.nombre_usuario, u.nombre, u.apellido, u.fecha_nacimiento, u.telefono," \
        " u.email, u.tipo, p.comuna, p.fecha_primera_visita from tv_usuario u JOIN tv_paciente p ON u.id_usuario = p.id_paciente"

        try:
            cursor.execute(consulta)
            datos = cursor.fetchall()
            print("[INFO]: Pacientes obtenidos correctamente.")
            return datos
        
        except Exception as e:
            print(f"[ERROR]: Error al obtener pacientes -> {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()

    def eliminar_paciente(self, nombre_usuario: str) -> bool:

        cursor = self.db.obtener_cursor()
    
        try:
            consulta_validacion = "select id_usuario from tv_usuario where nombre_usuario = :1"
            cursor.execute(consulta_validacion, (nombre_usuario,))
            datos = cursor.fetchone()     

            if not datos:
                print(f"[ERROR]: El usuario {nombre_usuario} no existe.")   
                return False 

            id_usuario = datos[0]

            cursor.execute("select 1 from tv_paciente where id_paciente = :1", (id_usuario,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: El usuario {nombre_usuario} no es un paciente.")
                return False
        
            consulta_delete_paciente = "delete from tv_paciente where id_paciente = :1"
            cursor.execute(consulta_delete_paciente, (id_usuario,))

            consulta_delete_usuario = "delete from tv_usuario where id_usuario = :1"
            cursor.execute(consulta_delete_usuario, (id_usuario,))   

            self.db.connection.commit()
            print(f"[INFO]: Paciente {nombre_usuario} eliminado correctamente.")

            return True
        
        except Exception as e:
            print(f"[ERROR]: Error al eliminar paciente -> {e}")
            self.db.connection.rollback()
            return False
        
        finally:
            if cursor:
                cursor.close()

class MedicoModel(UsuarioModel):
    def __init__(self, conexion: conexion_oracle):
        super().__init__(conexion)
        
    def crear(self, id_medico: int, nombre_usuario: str, clave: str, nombre: str, apellido: str,
                fecha_nacimiento: date, telefono: int, email: str, tipo: str, especialidad: str,
                horario_atencion: date, fecha_ingreso: date) -> bool:
        
        if not super().crear(id_medico, nombre_usuario, clave, nombre, apellido, fecha_nacimiento, telefono, email, tipo):
            return False

        cursor = self.db.obtener_cursor()
        consulta = "insert into tv_medico(id_medico, especialidad, horario_atencion, fecha_ingreso) values (:1, :2, :3, :4)"

        try:
            cursor.execute(consulta,(id_medico, especialidad, horario_atencion, fecha_ingreso))
            self.db.connection.commit()
            print(f"[INFO]: Médico {nombre_usuario} insertado correctamente.")
            return True
        
        except Exception as e:
            print(f"[ERROR]: No se pudo insertar -> {e}")
            self.db.connection.rollback()
            return False
        
        finally:
            if cursor:
                cursor.close()

    def mostrar_todos_completo(self):
        cursor = self.db.obtener_cursor()
        try:
            consulta = "SELECT u.id_usuario, u.nombre_usuario, u.clave, u.nombre, u.apellido," \
            " u.fecha_nacimiento, u.telefono, u.email, u.tipo, m.especialidad, m.horario_atencion, m.fecha_ingreso " \
            " FROM tv_usuario u JOIN tv_medico m ON u.id_usuario = m.id_medico"
            cursor.execute(consulta)
            print("[INFO]: Médicos obtenidos correctamente.")
            return cursor.fetchall()
        finally:
            cursor.close()

    def editar_medico(self, id_medico: int, nombre_usuario: str, *datos: tuple) -> bool:   

        if len(datos) < 10:
            print("[ERROR]: Cantidad insuficiente de datos para editar médico.")
            return False
    
        if not super().editar_usuario(id_medico, nombre_usuario, *datos[:7]):
            return False
        
        cursor = self.db.obtener_cursor()

        try:          
            consulta_validacion = "select 1 from tv_medico where id_medico = :1" 
            cursor.execute(consulta_validacion,(id_medico,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: Médico con ID {id_medico} no existe.")
                return False
                        
            especialidad = datos[7]
            horario_atencion = datos[8]
            fecha_ingreso = datos[9]

            consulta_update = "update tv_medico set especialidad = :1, horario_atencion = :2, fecha_ingreso = :3 where id_medico = :4 "

            cursor.execute(consulta_update,(especialidad, horario_atencion, fecha_ingreso, id_medico))

            self.db.connection.commit()
            print(f"[INFO]: Médico {nombre_usuario} editado correctamente.")
            return True
        
        except Exception as e:
            print(f"[ERROR]: Error al editar médico -> {e}")
            self.db.connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()

    def mostrar_todos(self) -> list:

        cursor = self.db.obtener_cursor()

        consulta = "select u.id_usuario, u.nombre_usuario, u.nombre, u.apellido, u.fecha_nacimiento, u.telefono," \
        " u.email, u.tipo, m.especialidad, m.horario_atencion, m.fecha_ingreso from tv_usuario u JOIN tv_medico m ON u.id_usuario = m.id_medico"

        try:
            cursor.execute(consulta)
            datos = cursor.fetchall()
            print("[INFO]: Médicos obtenidos correctamente.")
            return datos
        
        except Exception as e:
            print(f"[ERROR]: Error al obtener médicos -> {e}")
            return[]
        
        finally:
            if cursor:
                cursor.close()

    def eliminar_medico(self, nombre_usuario: str) -> bool:

        cursor = self.db.obtener_cursor()
    
        try:
            cursor.execute("SELECT id_usuario FROM tv_usuario WHERE nombre_usuario = :1", (nombre_usuario,))
            datos = cursor.fetchone()

            if not datos:
                print(f"[ERROR]: El usuario {nombre_usuario} no existe.")
                return False

            id_usuario = datos[0]

            cursor.execute("SELECT 1 FROM tv_medico WHERE id_medico = :1", (id_usuario,))
            if cursor.fetchone() is None:
                print(f"[ERROR]: El usuario {nombre_usuario} no es un médico.")
                return False

            cursor.execute("DELETE FROM tv_medico WHERE id_medico = :1", (id_usuario,))
            cursor.execute("DELETE FROM tv_usuario WHERE id_usuario = :1", (id_usuario,))

            self.db.connection.commit()
            print(f"[INFO]: Médico {nombre_usuario} eliminado correctamente.")
            return True

        except Exception as e:
            print(f"[ERROR]: Error al eliminar médico -> {e}")
            self.db.connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()