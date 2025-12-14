from model.m_personas import UsuarioModel, PacienteModel, MedicoModel

class UsuarioController:
    def __init__(self, modelo: UsuarioModel):
        self.modelo = modelo

    def registrar_usuario(self, id_usuario, nombre_usuario, clave, nombre, apellido, fecha_nacimiento, telefono, email, tipo) -> bool:
        if not id_usuario or not nombre_usuario or not clave or not nombre or not apellido or not fecha_nacimiento or not telefono or not email or not tipo:
            print("[Error]: Datos faltantes para registro de usuario.")
            return False
        
        return self.modelo.crear(id_usuario, nombre_usuario, clave, nombre, apellido, fecha_nacimiento, telefono, email, tipo)
    
    def listar_usuarios(self) -> list:
        usuarios = self.modelo.mostrar_todos()

        if len(usuarios) > 0 :
            return [{"id_usuario": u[0], "nombre_usuario": u[1], "clave": u[2], "nombre": u[3], "apellido": u[4], "fecha_nacimiento": u[5], "telefono": u[6],"email": u[7], "tipo": u[8]} for u in usuarios]
        
        else:
            return[]


class PacienteController:
    def __init__(self, modelo_usuario: UsuarioModel, modelo_paciente: PacienteModel):
        self.modelo_usuario = modelo_usuario
        self.modelo_paciente = modelo_paciente

    def registrar_paciente(self, id_paciente, nombre_usuario, clave, nombre, apellido,
                            fecha_nacimiento, telefono, email, tipo, comuna,
                            fecha_primera_visita) -> bool:

        if not all([id_paciente, nombre_usuario, clave, nombre, apellido,
                    fecha_nacimiento, telefono, email, tipo, comuna,
                    fecha_primera_visita]):
            print("[Error]: Datos faltantes para registro de paciente.")
            return False

        crear_usuario = self.modelo_usuario.crear(
            id_paciente, nombre_usuario, clave, nombre, apellido,
            fecha_nacimiento, telefono, email, tipo
        )
        if not crear_usuario:
            return False

        crear_paciente = self.modelo_paciente.crear(id_paciente, comuna, fecha_primera_visita)
        return crear_paciente

    
    def listar_pacientes(self) -> list:
        pacientes = self.modelo_paciente.mostrar_todos_completo()

        if pacientes: return [{"id_paciente": p[0], "nombre_usuario": p[1], "clave": p[2], "nombre": p[3],
                    "apellido": p[4], "fecha_nacimiento": p[5], "telefono": p[6],"email": p[7],
                    "tipo": p[8]} for p in pacientes]
        else:
            return[]
        
class MedicoController:
    def __init__(self, modelo_usuario: UsuarioModel, modelo_medico: MedicoModel):
        self.modelo_usuario = modelo_usuario
        self.modelo_medico = modelo_medico

    def registrar_medico(self, id_medico, nombre_usuario, clave, nombre, apellido,
                         fecha_nacimiento, telefono, email, tipo, especialidad,
                         horario_atencion, fecha_ingreso) -> bool:

        if not all([id_medico, nombre_usuario, clave, nombre, apellido,
                    fecha_nacimiento, telefono, email, tipo, especialidad,
                    horario_atencion, fecha_ingreso]):
            print("[Error]: Datos faltantes para registro de médico.")
            return False

        crear_usuario = self.modelo_usuario.crear(
            id_medico, nombre_usuario, clave, nombre, apellido,
            fecha_nacimiento, telefono, email, tipo
        )
        if not crear_usuario:
            return False

        crear_medico = self.modelo_medico.crear(
            id_medico, nombre_usuario, clave, nombre, apellido,
            fecha_nacimiento, telefono, email, tipo,
            especialidad, horario_atencion, fecha_ingreso
        )
        return crear_medico

    def listar_medicos(self) -> list:
        medicos = self.modelo_medico.mostrar_todos_completo()

        if medicos:
            return [{"id_medico": m[0], "nombre_usuario": m[1], "clave": m[2], "nombre": m[3],
                   "apellido": m[4], "fecha_nacimiento": m[5], "telefono": m[6], "email": m[7],
                   "tipo": m[8], "especialidad": m[9], "horario_atencion": m[10], 
                   "fecha_ingreso": m[11]} for m in medicos]
        else:
            return []

