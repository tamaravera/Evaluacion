from typing import Any, Dict, List
from model.personas_m import UsuarioModel, PacienteModel, MedicoModel, AdministradorModel


class UsuarioController:
    def __init__(self, modelo: UsuarioModel):
        self.modelo = modelo

    def registrar_usuario(
        self,
        id_usuario,
        nombre_usuario,
        clave,
        nombre,
        apellido,
        fecha_nacimiento,
        telefono,
        email,
        tipo,
    ) -> bool:
        if not id_usuario or not nombre_usuario or not clave or not nombre or not apellido or not fecha_nacimiento or not telefono or not email or not tipo:
            print("[Error]: Datos faltantes para registro de usuario.")
            return False

        try:
            return self.modelo.crear(
                id_usuario,
                nombre_usuario,
                clave,
                nombre,
                apellido,
                fecha_nacimiento,
                telefono,
                email,
                tipo,
            )
        except Exception as e:
            print(f"[ERROR]: Excepción al registrar usuario -> {e}")
            return False

    def listar_usuarios(self) -> List[Dict[str, Any]]:
        try:
            usuarios = self.modelo.mostrar_todos()
        except Exception as e:
            print(f"[ERROR]: Excepción al listar usuarios -> {e}")
            return []

        if usuarios and len(usuarios) > 0:
            return [
                {
                    "id_usuario": u[0],
                    "nombre_usuario": u[1],
                    "clave": u[2] if len(u) > 2 else None,
                    "nombre": u[2] if len(u) == 3 else u[3] if len(u) > 3 else None,
                    "apellido": u[4] if len(u) > 4 else None,
                    "fecha_nacimiento": u[5] if len(u) > 5 else None,
                    "telefono": u[6] if len(u) > 6 else None,
                    "email": u[7] if len(u) > 7 else None,
                    "tipo": u[8] if len(u) > 8 else None,
                }
                for u in usuarios
            ]
        else:
            return []
        
    def existe_usuario(self, nombre_usuario: str) -> bool:
        return self.usuario_model.existe_usuario(nombre_usuario)


class PacienteController:
    def __init__(self, modelo_usuario: UsuarioModel, modelo_paciente: PacienteModel):
        self.modelo_usuario = modelo_usuario
        self.modelo_paciente = modelo_paciente

    def registrar_paciente(
        self,
        id_paciente,
        nombre_usuario,
        clave,
        nombre,
        apellido,
        fecha_nacimiento,
        telefono,
        email,
        tipo,
        comuna,
        fecha_primera_visita,
    ) -> bool:
        if not all(
            [
                id_paciente,
                nombre_usuario,
                clave,
                nombre,
                apellido,
                fecha_nacimiento,
                telefono,
                email,
                tipo,
                comuna,
                fecha_primera_visita,
            ]
        ):
            print("[Error]: Datos faltantes para registro de paciente.")
            return False

        try:
            crear_usuario = self.modelo_usuario.crear(
                id_paciente,
                nombre_usuario,
                clave,
                nombre,
                apellido,
                fecha_nacimiento,
                telefono,
                email,
                tipo,
            )
        except Exception as e:
            print(f"[ERROR]: Excepción al crear usuario para paciente -> {e}")
            return False

        if not crear_usuario:
            return False

        try:
            crear_paciente = self.modelo_paciente.crear(id_paciente, comuna, fecha_primera_visita)
            return crear_paciente
        except Exception as e:
            print(f"[ERROR]: Excepción al crear paciente -> {e}")
            return False

    def listar_pacientes(self) -> List[Dict[str, Any]]:
        try:
            pacientes = self.modelo_paciente.mostrar_todos_completo()
        except Exception as e:
            print(f"[ERROR]: Excepción al listar pacientes -> {e}")
            return []

        if pacientes:
            return [
                {
                    "id_paciente": p[0],
                    "nombre_usuario": p[1],
                    "clave": p[2],
                    "nombre": p[3],
                    "apellido": p[4],
                    "fecha_nacimiento": p[5],
                    "telefono": p[6],
                    "email": p[7],
                    "tipo": p[8],
                    "comuna": p[9],
                    "fecha_primera_visita": p[10],
                }
                for p in pacientes
            ]
        else:
            return []


class MedicoController:
    def __init__(self, modelo_usuario: UsuarioModel, modelo_medico: MedicoModel):
        self.modelo_usuario = modelo_usuario
        self.modelo_medico = modelo_medico

    def registrar_medico(
        self,
        id_medico,
        nombre_usuario,
        clave,
        nombre,
        apellido,
        fecha_nacimiento,
        telefono,
        email,
        tipo,
        especialidad,
        horario_atencion,
        fecha_ingreso,
    ) -> bool:
        if not all(
            [
                id_medico,
                nombre_usuario,
                clave,
                nombre,
                apellido,
                fecha_nacimiento,
                telefono,
                email,
                tipo,
                especialidad,
                horario_atencion,
                fecha_ingreso,
            ]
        ):
            print("[Error]: Datos faltantes para registro de médico.")
            return False

        try:
            crear_usuario = self.modelo_usuario.crear(
                id_medico,
                nombre_usuario,
                clave,
                nombre,
                apellido,
                fecha_nacimiento,
                telefono,
                email,
                tipo,
            )
        except Exception as e:
            print(f"[ERROR]: Excepción al crear usuario para médico -> {e}")
            return False

        if not crear_usuario:
            return False

        try:
            crear_medico = self.modelo_medico.crear(id_medico, especialidad, horario_atencion, fecha_ingreso)
            return crear_medico
        except Exception as e:
            print(f"[ERROR]: Excepción al crear médico -> {e}")
            return False

    def listar_medicos(self) -> List[Dict[str, Any]]:
        try:
            medicos = self.modelo_medico.mostrar_todos_completo()
        except Exception as e:
            print(f"[ERROR]: Excepción al listar médicos -> {e}")
            return []

        if medicos:
            return [
                {
                    "id_medico": m[0],
                    "nombre_usuario": m[1],
                    "clave": m[2],
                    "nombre": m[3],
                    "apellido": m[4],
                    "fecha_nacimiento": m[5],
                    "telefono": m[6],
                    "email": m[7],
                    "tipo": m[8],
                    "especialidad": m[9],
                    "horario_atencion": m[10],
                    "fecha_ingreso": m[11],
                }
                for m in medicos
            ]
        else:
            return []


class AdministradorController:
    def __init__(self, modelo_usuario: UsuarioModel, modelo_administrador: AdministradorModel):
        self.modelo_usuario = modelo_usuario
        self.modelo_administrador = modelo_administrador

    def registrar_administrador(
        self,
        id_administrador,
        nombre_usuario,
        clave,
        nombre,
        apellido,
        fecha_nacimiento,
        telefono,
        email,
        tipo,
    ) -> bool:
        if not all(
            [
                id_administrador,
                nombre_usuario,
                clave,
                nombre,
                apellido,
                fecha_nacimiento,
                telefono,
                email,
                tipo,
            ]
        ):
            print("[Error]: Datos faltantes para registro de administrador.")
            return False

        try:
            crear_usuario = self.modelo_usuario.crear(
                id_administrador,
                nombre_usuario,
                clave,
                nombre,
                apellido,
                fecha_nacimiento,
                telefono,
                email,
                tipo,
            )
        except Exception as e:
            print(f"[ERROR]: Excepción al crear usuario para administrador -> {e}")
            return False

        if not crear_usuario:
            return False

        try:
            crear_admin = self.modelo_administrador.crear(id_administrador)
            return crear_admin
        except Exception as e:
            print(f"[ERROR]: Excepción al crear administrador -> {e}")
            return False

    def listar_administradores(self) -> List[Dict[str, Any]]:
        try:
            admins = self.modelo_administrador.mostrar_items()
        except Exception as e:
            print(f"[ERROR]: Excepción al listar administradores -> {e}")
            return []

        if admins:
            return [
                {
                    "id_administrador": a[0],
                    "nombre_usuario": a[1],
                    "nombre": a[2],
                    "apellido": a[3],
                    "fecha_nacimiento": a[4],
                    "telefono": a[5],
                    "email": a[6],
                    "tipo": a[7],
                }
                for a in admins
            ]
        else:
            return []