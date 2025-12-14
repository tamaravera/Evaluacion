from datetime import date
from typing import List, Dict, Any


class UsuarioView:
    @staticmethod
    def mostrar_usuarios(usuarios: List[Dict[str, Any]]) -> None:
        if usuarios:
            print("\n- Lista de usuarios -")
            for u in usuarios:
                fn = u.get("fecha_nacimiento")
                fn_str = fn.isoformat() if isinstance(fn, date) else str(fn)
                print(
                    f"--- ID: {u.get('id_usuario')} | Nombre_usuario: {u.get('nombre_usuario')}\n"
                    f" | Clave: {u.get('clave')} | Nombre: {u.get('nombre')} | Apellido: {u.get('apellido')}\n"
                    f" | Fecha_nacimiento: {fn_str} | Teléfono: {u.get('telefono')}\n"
                    f" | Email: {u.get('email')} | Tipo: {u.get('tipo')}"
                )
        else:
            print("[ERROR]: Sin usuarios registrados")


class PacienteView:
    @staticmethod
    def mostrar_pacientes(pacientes: List[Dict[str, Any]]) -> None:
        if pacientes:
            print("\n- Lista de pacientes -")
            for p in pacientes:
                fn = p.get("fecha_nacimiento")
                fn_str = fn.isoformat() if isinstance(fn, date) else str(fn)
                fpv = p.get("fecha_primera_visita")
                fpv_str = fpv.isoformat() if isinstance(fpv, date) else str(fpv)
                print(
                    f"--- ID: {p.get('id_paciente')} | Nombre_usuario: {p.get('nombre_usuario')}\n"
                    f" | Clave: {p.get('clave')} | Nombre: {p.get('nombre')} | Apellido: {p.get('apellido')}\n"
                    f" | Fecha_nacimiento: {fn_str} | Teléfono: {p.get('telefono')}\n"
                    f" | Email: {p.get('email')} | Tipo: {p.get('tipo')} | Comuna: {p.get('comuna')}\n"
                    f" | Fecha_primera_visita: {fpv_str}"
                )
        else:
            print("[ERROR]: Sin pacientes registrados")


class MedicoView:
    @staticmethod
    def mostrar_medicos(medicos: List[Dict[str, Any]]) -> None:
        if medicos:
            print("\n- Lista de médicos -")
            for m in medicos:
                fn = m.get("fecha_nacimiento")
                fn_str = fn.isoformat() if isinstance(fn, date) else str(fn)
                fi = m.get("fecha_ingreso")
                fi_str = fi.isoformat() if isinstance(fi, date) else str(fi)
                horario = m.get("horario_atencion")
                horario_str = horario.isoformat() if isinstance(horario, date) else str(horario)
                print(
                    f"--- ID: {m.get('id_medico')} | Nombre_usuario: {m.get('nombre_usuario')}\n"
                    f" | Clave: {m.get('clave')} | Nombre: {m.get('nombre')} | Apellido: {m.get('apellido')}\n"
                    f" | Fecha_nacimiento: {fn_str} | Teléfono: {m.get('telefono')}\n"
                    f" | Email: {m.get('email')} | Tipo: {m.get('tipo')} | Especialidad: {m.get('especialidad')}\n"
                    f" | Horario_atencion: {horario_str} | Fecha_ingreso: {fi_str}"
                )
        else:
            print("[ERROR]: Sin médicos registrados")


class AdministradorView:
    @staticmethod
    def mostrar_administradores(administradores: List[Dict[str, Any]]) -> None:
        if administradores:
            print("\n- Lista de administradores -")
            for a in administradores:
                fn = a.get("fecha_nacimiento")
                fn_str = fn.isoformat() if isinstance(fn, date) else str(fn)
                print(
                    f"--- ID Administrador: {a.get('id_administrador')} | Nombre_usuario: {a.get('nombre_usuario')}\n"
                    f" | Nombre: {a.get('nombre')} | Apellido: {a.get('apellido')}\n"
                    f" | Fecha_nacimiento: {fn_str} | Teléfono: {a.get('telefono')}\n"
                    f" | Email: {a.get('email')} | Tipo: {a.get('tipo')}"
                )
        else:
            print("[ERROR]: Sin administradores registrados")