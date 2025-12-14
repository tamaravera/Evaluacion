import json
import os
from datetime import date
import inspect
import sys
import bcrypt
from datetime import date, datetime
from typing import Any, Optional, Dict
from utils.validaciones import normalizar_telefono
try:
    from config.db_config import conexion_oracle, validar_tablas
except Exception:
    try:
        from config.configdb import conexion_oracle, validar_tablas
    except Exception as e:
        print("[ERROR]: No se encontró config.db_config ni config.configdb:", e)
        sys.exit(1)


def try_import(module_names):
    for m in module_names:
        try:
            mod = __import__(m, fromlist=["*"])
            return mod
        except Exception:
            continue
    return None



mod_personas = try_import(
    [
        "model.m_personas",
        "model.personas_m",
        "model.personas",
        "personas",  
    ]
)
if mod_personas:
    UsuarioModel = getattr(mod_personas, "UsuarioModel", None)
    PacienteModel = getattr(mod_personas, "PacienteModel", None)
    MedicoModel = getattr(mod_personas, "MedicoModel", None)
    AdministradorModel = getattr(mod_personas, "AdministradorModel", None)
else:
    UsuarioModel = PacienteModel = MedicoModel = AdministradorModel = None


mod_objetos = try_import(
    [
        "model.m_objetos",
        "model.objetos_m",
        "model.m_objetos",
        "model.objetos",
        "objetos", 
    ]
)
if mod_objetos:
    InsumosModel = getattr(mod_objetos, "InsumosModel", None)
    RecetasModel = getattr(mod_objetos, "RecetasModel", None)
    ConsultasModel = getattr(mod_objetos, "ConsultasModel", None)
    AgendaModel = getattr(mod_objetos, "AgendaModel", None)
else:
    InsumosModel = RecetasModel = ConsultasModel = AgendaModel = None

mod_ctrl_personas = try_import(
    [
        "personas_controller",
        "controller.personas_c",
        "controller.personas",
        "controllers.personas",
        "controller.personas_controller",
    ]
)
if mod_ctrl_personas:
    UsuarioController = getattr(mod_ctrl_personas, "UsuarioController", None)
    PacienteController = getattr(mod_ctrl_personas, "PacienteController", None)
    MedicoController = getattr(mod_ctrl_personas, "MedicoController", None)
    AdministradorController = getattr(mod_ctrl_personas, "AdministradorController", None)
else:
    UsuarioController = PacienteController = MedicoController = AdministradorController = None

mod_ctrl_objetos = try_import(
    [
        "controllers",
        "controller.objetos_c",
        "controller.objetos",
        "controllers.objetos",
        "objetos_controller",
    ]
)
if mod_ctrl_objetos:
    InsumosController = getattr(mod_ctrl_objetos, "InsumosController", None)
    RecetasController = getattr(mod_ctrl_objetos, "RecetasController", None)
    ConsultasController = getattr(mod_ctrl_objetos, "ConsultasController", None)
    AgendaController = getattr(mod_ctrl_objetos, "AgendaController", None)
else:
    InsumosController = RecetasController = ConsultasController = AgendaController = None


mod_view_personas = try_import(["personas_view", "view.personas_v", "view.personas", "personas_v"])
if mod_view_personas:
    UsuarioView = getattr(mod_view_personas, "UsuarioView", None)
    PacienteView = getattr(mod_view_personas, "PacienteView", None)
    MedicoView = getattr(mod_view_personas, "MedicoView", None)
    AdministradorView = getattr(mod_view_personas, "AdministradorView", None)
else:
    UsuarioView = PacienteView = MedicoView = AdministradorView = None

mod_view_objetos = try_import(["objetos_view", "view.objetos_v", "view.objetos", "objetos_v"])
if mod_view_objetos:
    InsumosView = getattr(mod_view_objetos, "InsumosView", None)
    RecetasView = getattr(mod_view_objetos, "RecetasView", None)
    ConsultasView = getattr(mod_view_objetos, "ConsultasView", None)
    AgendaView = getattr(mod_view_objetos, "AgendaView", None)
else:
    InsumosView = RecetasView = ConsultasView = AgendaView = None


def hacer_hash_clave(clave: str) -> str:
    b = clave.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(b, salt).decode("utf-8")


def verificar_clave(clave_plana: str, clave_hash: str) -> bool:
    try:
        return bcrypt.checkpw(clave_plana.encode("utf-8"), clave_hash.encode("utf-8"))
    except Exception:
        return False


def parse_fecha(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None


def instanciar_modelo(ModelClass: type, db: conexion_oracle):

    try:
        return ModelClass(db)
    except Exception:
        pass

    try:
        sig = inspect.signature(ModelClass.__init__)
        params = list(sig.parameters.values())[1:]  
        args = []
        for p in params:
            name = p.name.lower()

            if name in ("db", "conexion", "conexion_oracle", "connection", "conn"):
                args.append(db)
                continue

            if name.startswith("id") or name.endswith("_id") or name == "id":
                args.append(0)
                continue

            if name in ("stock", "cantidad", "cantidad_stock"):
                args.append(0)
                continue

            if any(k in name for k in ("costo", "valor", "precio", "amount")):
                args.append(0.0)
                continue

            if "fecha" in name or "date" in name or "ingreso" in name:
                args.append(None)
                continue

            if any(k in name for k in ("nombre", "tipo", "descripcion", "email", "apellido", "usuario", "estado", "horario", "medicamentos")):
                args.append("")
                continue

            ann = p.annotation
            if ann is int:
                args.append(0)
            elif ann is float:
                args.append(0.0)
            elif ann is str:
                args.append("")
            elif ann is date:
                args.append(None)
            else:
                args.append(None)

        return ModelClass(*args)
    except Exception:
        pass


    try:
        return ModelClass()
    except Exception as e:
        raise RuntimeError(f"No se pudo instanciar el modelo {ModelClass}: {e}") from e



def crear_controllers(db: conexion_oracle) -> Dict[str, Any]:
    if UsuarioModel is None or InsumosModel is None:
        raise RuntimeError("No están disponibles los modelos básicos (UsuarioModel/InsumosModel). Revisa imports.")

    usuario_model = instanciar_modelo(UsuarioModel, db)
    paciente_model = instanciar_modelo(PacienteModel, db) if PacienteModel else None
    medico_model = instanciar_modelo(MedicoModel, db) if MedicoModel else None
    administrador_model = instanciar_modelo(AdministradorModel, db) if AdministradorModel else None

    insumos_model = instanciar_modelo(InsumosModel, db)
    recetas_model = instanciar_modelo(RecetasModel, db) if RecetasModel else None
    consultas_model = instanciar_modelo(ConsultasModel, db) if ConsultasModel else None
    agenda_model = instanciar_modelo(AgendaModel, db) if AgendaModel else None


    if UsuarioController is None:
        raise RuntimeError("UsuarioController no encontrado en tus controladores.")
    usuario_ctrl = UsuarioController(usuario_model)

    paciente_ctrl = None
    if PacienteController and paciente_model:
        paciente_ctrl = PacienteController(usuario_model, paciente_model)

    medico_ctrl = None
    if MedicoController and medico_model:
        medico_ctrl = MedicoController(usuario_model, medico_model)

    administrador_ctrl = None
    if AdministradorController and administrador_model:
        administrador_ctrl = AdministradorController(usuario_model, administrador_model)

    if InsumosController is None:
        raise RuntimeError("InsumosController no encontrado en tus controladores.")
    insumos_ctrl = InsumosController(insumos_model)

    recetas_ctrl = RecetasController(recetas_model) if RecetasController and recetas_model else None
    consultas_ctrl = ConsultasController(consultas_model) if ConsultasController and consultas_model else None
    agenda_ctrl = AgendaController(agenda_model) if AgendaController and agenda_model else None

    return {
        "usuario_ctrl": usuario_ctrl,
        "paciente_ctrl": paciente_ctrl,
        "medico_ctrl": medico_ctrl,
        "administrador_ctrl": administrador_ctrl,
        "insumos_ctrl": insumos_ctrl,
        "recetas_ctrl": recetas_ctrl,
        "consultas_ctrl": consultas_ctrl,
        "agenda_ctrl": agenda_ctrl,
    }


def login_interactivo(db: conexion_oracle) -> Optional[int]:
    try:
        usuario_login = input("Usuario: ").strip()
        clave_login = input("Clave: ").strip()
        if not usuario_login or not clave_login:
            print("[ERROR]: datos incompletos")
            return None

        cur = db.obtener_cursor()
        try:
            cur.execute("SELECT id_usuario, clave FROM tv_usuario WHERE nombre_usuario = :1", (usuario_login,))
            row = cur.fetchone()
        finally:
            try:
                cur.close()
            except Exception:
                pass

        if row is None:
            print("[ERROR]: Usuario no encontrado")
            return None

        id_usuario, clave_hash = row[0], row[1]
        if not isinstance(clave_hash, str):
            print("[ERROR]: Formato de clave en BD inesperado")
            return None

        if verificar_clave(clave_login, clave_hash):
            print("[INFO]: Ingreso correcto")
            return id_usuario
        else:
            print("[ERROR]: Credenciales incorrectas")
            return None
    except Exception as e:
        print("[ERROR]: Error en login ->", e)
        return None


def submenu_gestion_insumos(insumos_ctrl):
    while True:
        print("\n--- Gestión Insumos ---")
        print("1) Listar insumos")
        print("2) Agregar insumo")
        print("3) Editar insumo")
        print("4) Eliminar insumo")
        print("0) Volver")
        opt = input("Opción: ").strip()
        if opt == "1":
            items = insumos_ctrl.listar_insumos()
            if InsumosView:
                InsumosView.mostrar_insumos(items)
            else:
                print(items)
        elif opt == "2":
            try:
                id_insumo = int(input("ID insumo: ").strip())
                nombre = input("Nombre: ").strip()
                tipo = input("Tipo: ").strip()
                stock = int(input("Stock: ").strip())
                costo = float(input("Costo USD: ").strip())
                ok = insumos_ctrl.registrar_insumo(id_insumo, nombre, tipo, stock, costo)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "3":
            try:
                id_insumo = int(input("ID insumo a editar: ").strip())
                nombre = input("Nombre: ").strip()
                tipo = input("Tipo: ").strip()
                stock = int(input("Stock: ").strip())
                costo = float(input("Costo USD: ").strip())
                ok = insumos_ctrl.editar_insumo(id_insumo, nombre, tipo, stock, costo)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "4":
            try:
                id_insumo = int(input("ID insumo a eliminar: ").strip())
                ok = insumos_ctrl.eliminar_insumo(id_insumo)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "0":
            break
        else:
            print("Opción inválida")


def submenu_gestion_recetas(recetas_ctrl):
    while True:
        print("\n--- Gestión Recetas ---")
        print("1) Listar recetas")
        print("2) Agregar receta")
        print("3) Editar receta")
        print("4) Eliminar receta")
        print("0) Volver")
        opt = input("Opción: ").strip()
        if opt == "1":
            items = recetas_ctrl.listar_recetas()
            if RecetasView:
                RecetasView.mostrar_recetas(items)
            else:
                print(items)
        elif opt == "2":
            try:
                id_receta = int(input("ID receta: ").strip())
                id_paciente = int(input("ID paciente: ").strip())
                id_medico = int(input("ID medico: ").strip())
                descripcion = input("Descripción: ").strip()
                medicamentos = input("Medicamentos recetados: ").strip()
                costo = float(input("Costo CLP: ").strip())
                ok = recetas_ctrl.registrar_receta(id_receta, id_paciente, id_medico, descripcion, medicamentos, costo)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "3":
            try:
                id_receta = int(input("ID receta a editar: ").strip())
                id_paciente = int(input("ID paciente: ").strip())
                id_medico = int(input("ID medico: ").strip())
                descripcion = input("Descripción: ").strip()
                medicamentos = input("Medicamentos recetados: ").strip()
                costo = float(input("Costo CLP: ").strip())
                ok = recetas_ctrl.editar_receta(id_receta, id_paciente, id_medico, descripcion, medicamentos, costo)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "4":
            try:
                id_receta = int(input("ID receta a eliminar: ").strip())
                ok = recetas_ctrl.eliminar_receta(id_receta)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "0":
            break
        else:
            print("Opción inválida")


def submenu_gestion_consultas(consultas_ctrl):
    while True:
        print("\n--- Gestión Consultas ---")
        print("1) Listar consultas")
        print("2) Agregar consulta")
        print("3) Editar consulta")
        print("4) Eliminar consulta")
        print("0) Volver")
        opt = input("Opción: ").strip()
        if opt == "1":
            items = consultas_ctrl.listar_consultas()
            if ConsultasView:
                ConsultasView.mostrar_consultas(items)
            else:
                print(items)
        elif opt == "2":
            try:
                id_consulta = int(input("ID consulta: ").strip())
                id_paciente = int(input("ID paciente: ").strip())
                id_medico = int(input("ID medico: ").strip())
                id_receta_raw = input("ID receta (vacío si none): ").strip()
                id_receta = int(id_receta_raw) if id_receta_raw else None
                fecha_raw = input("Fecha (YYYY-MM-DD): ").strip()
                fecha = parse_fecha(fecha_raw)
                comentarios = input("Comentarios: ").strip()
                valor = float(input("Valor: ").strip())
                ok = consultas_ctrl.registrar_consulta(id_consulta, id_paciente, id_medico, id_receta, fecha, comentarios, valor)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "3":
            try:
                id_consulta = int(input("ID consulta a editar: ").strip())
                id_paciente = int(input("ID paciente: ").strip())
                id_medico = int(input("ID medico: ").strip())
                id_receta_raw = input("ID receta (vacío si none): ").strip()
                id_receta = int(id_receta_raw) if id_receta_raw else None
                fecha_raw = input("Fecha (YYYY-MM-DD): ").strip()
                fecha = parse_fecha(fecha_raw)
                comentarios = input("Comentarios: ").strip()
                valor = float(input("Valor: ").strip())
                ok = consultas_ctrl.editar_consulta(id_consulta, id_paciente, id_medico, id_receta, fecha, comentarios, valor)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "4":
            try:
                id_consulta = int(input("ID consulta a eliminar: ").strip())
                ok = consultas_ctrl.eliminar_consulta(id_consulta)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "0":
            break
        else:
            print("Opción inválida")


def submenu_gestion_agenda(agenda_ctrl):
    while True:
        print("\n--- Gestión Agenda ---")
        print("1) Listar agenda")
        print("2) Agregar agenda")
        print("3) Editar agenda")
        print("4) Eliminar agenda")
        print("0) Volver")
        opt = input("Opción: ").strip()
        if opt == "1":
            items = agenda_ctrl.listar_agendas()
            if AgendaView:
                AgendaView.mostrar_agenda(items)
            else:
                print(items)
        elif opt == "2":
            try:
                id_agenda = int(input("ID agenda: ").strip())
                id_paciente = int(input("ID paciente: ").strip())
                id_medico = int(input("ID medico: ").strip())
                fecha_raw = input("Fecha consulta (YYYY-MM-DD): ").strip()
                fecha = parse_fecha(fecha_raw)
                estado = input("Estado: ").strip()
                ok = agenda_ctrl.registrar_agenda(id_agenda, id_paciente, id_medico, fecha, estado)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "3":
            try:
                id_agenda = int(input("ID agenda a editar: ").strip())
                id_paciente = int(input("ID paciente: ").strip())
                id_medico = int(input("ID medico: ").strip())
                fecha_raw = input("Fecha consulta (YYYY-MM-DD): ").strip()
                fecha = parse_fecha(fecha_raw)
                estado = input("Estado: ").strip()
                ok = agenda_ctrl.editar_agenda(id_agenda, id_paciente, id_medico, fecha, estado)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "4":
            try:
                id_agenda = int(input("ID agenda a eliminar: ").strip())
                ok = agenda_ctrl.eliminar_agenda(id_agenda)
                print("OK" if ok else "FALLÓ")
            except Exception as e:
                print("[ERROR]:", e)
        elif opt == "0":
            break
        else:
            print("Opción inválida")


DB_USER = "system"
DB_PASS = "Tamara21."
DB_DSN = "localhost:1521/xe"


def conectar_bd() -> conexion_oracle:
    db = conexion_oracle(DB_USER, DB_PASS, DB_DSN)
    db.conectar()
    return db

def cargar_usuarios_desde_json(ruta_json: str, usuario_ctrl):
    if not os.path.exists(ruta_json):
        print(f"[ERROR]: Archivo no encontrado: {ruta_json}")
        return

    with open(ruta_json, "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    for u in usuarios:
        username = u.get("username")

        try:
            if usuario_ctrl.existe_usuario(username):
                print(f"[SKIP]: {username} ya está insertado")
                continue

            telefono = normalizar_telefono(u.get("phone", ""))

            nombre_completo = u.get("name", "")
            partes = nombre_completo.split(" ", 1)

            nombre = partes[0]
            apellido = partes[1] if len(partes) > 1 else ""

            clave_hash = hacer_hash_clave("1234")

            ok = usuario_ctrl.registrar_usuario(
                u.get("id"),
                username,
                clave_hash,
                nombre,
                apellido,
                date(2000, 1, 1),
                telefono,
                u.get("email"),
                "paciente"
            )

            if ok:
                print(f"[OK]: {username} insertado correctamente")
            else:
                print(f"[WARN]: {username} no se pudo insertar")

        except Exception as e:
            print(f"[ERROR]: {username} omitido -> {e}")



def main():
    db = conectar_bd()
    try:
        try:
            validar_tablas(db)
        except Exception as e:
            print("[WARN]: validar_tablas falló:", e)

        ctrls = crear_controllers(db)

        usuario_ctrl = ctrls["usuario_ctrl"]
        paciente_ctrl = ctrls["paciente_ctrl"]
        medico_ctrl = ctrls["medico_ctrl"]
        administrador_ctrl = ctrls["administrador_ctrl"]
        insumos_ctrl = ctrls["insumos_ctrl"]
        recetas_ctrl = ctrls["recetas_ctrl"]
        consultas_ctrl = ctrls["consultas_ctrl"]
        agenda_ctrl = ctrls["agenda_ctrl"]

        while True:
            print("\n--- MENU PRINCIPAL ---")
            print("1) Registrar usuario manual")
            print("2) Iniciar sesión")
            print("3) Gestionar Insumos")
            print("4) Gestionar Recetas")
            print("5) Gestionar Consultas")
            print("6) Gestionar Agenda")
            print("7) Listar usuarios / pacientes / médicos / administradores")
            print("8) Cargar usuarios desde JSON")
            print("0) Salir")
            opt = input("Elija opción: ").strip()

            if opt == "1":
                try:
                    id_usuario = int(input("ID usuario: ").strip())
                    nombre_usuario = input("Nombre usuario: ").strip()
                    clave_plain = input("Clave: ").strip()
                    nombre = input("Nombre: ").strip()
                    apellido = input("Apellido: ").strip()
                    fecha_raw = input("Fecha nacimiento (YYYY-MM-DD): ").strip()
                    fecha_nacimiento = parse_fecha(fecha_raw)
                    telefono = input("Teléfono: ").strip()
                    email = input("Email: ").strip()
                    tipo = input("Tipo (paciente/medico/administrador): ").strip().lower()

                    if not fecha_nacimiento:
                        print("[ERROR]: Fecha inválida")
                        continue

                    clave_hashed = hacer_hash_clave(clave_plain)
                    ok = usuario_ctrl.registrar_usuario(
                        id_usuario,
                        nombre_usuario,
                        clave_hashed,
                        nombre,
                        apellido,
                        fecha_nacimiento,
                        telefono,
                        email,
                        tipo,
                    )
                    if ok:
                        print("[INFO]: Usuario creado.")
                        if tipo == "paciente" and paciente_ctrl:
                            comuna = input("Comuna: ").strip()
                            fpv_raw = input("Fecha primera visita (YYYY-MM-DD): ").strip()
                            fpv = parse_fecha(fpv_raw)
                            if comuna and fpv:
                                paciente_ctrl.registrar_paciente(id_usuario, nombre_usuario, clave_hashed, nombre, apellido,
                                                                fecha_nacimiento, telefono, email, tipo, comuna, fpv)
                        elif tipo == "medico" and medico_ctrl:
                            especialidad = input("Especialidad: ").strip()
                            horario_raw = input("Horario (YYYY-MM-DD o cadena): ").strip()
                            horario = parse_fecha(horario_raw) if horario_raw else horario_raw
                            fecha_ingreso_raw = input("Fecha ingreso (YYYY-MM-DD): ").strip()
                            fecha_ingreso = parse_fecha(fecha_ingreso_raw)
                            if especialidad and fecha_ingreso:
                                medico_ctrl.registrar_medico(id_usuario, nombre_usuario, clave_hashed, nombre, apellido,
                                                            fecha_nacimiento, telefono, email, tipo, especialidad, horario, fecha_ingreso)
                        elif tipo == "administrador" and administrador_ctrl:
                            administrador_ctrl.registrar_administrador(id_usuario, nombre_usuario, clave_hashed, nombre, apellido,
                                                                      fecha_nacimiento, telefono, email, tipo)
                    else:
                        print("[WARN]: No se pudo crear usuario (posible duplicado).")
                except Exception as e:
                    print("[ERROR]:", e)

            elif opt == "2":
                login_interactivo(db)

            elif opt == "3":
                submenu_gestion_insumos(insumos_ctrl)

            elif opt == "4":
                if recetas_ctrl:
                    submenu_gestion_recetas(recetas_ctrl)
                else:
                    print("[WARN]: Controlador de recetas no disponible.")

            elif opt == "5":
                if consultas_ctrl:
                    submenu_gestion_consultas(consultas_ctrl)
                else:
                    print("[WARN]: Controlador de consultas no disponible.")

            elif opt == "6":
                if agenda_ctrl:
                    submenu_gestion_agenda(agenda_ctrl)
                else:
                    print("[WARN]: Controlador de agenda no disponible.")

            elif opt == "7":
                try:
                    usuarios = usuario_ctrl.listar_usuarios()
                    if UsuarioView:
                        UsuarioView.mostrar_usuarios(usuarios)
                    else:
                        print(usuarios)
                except Exception as e:
                    print("[ERROR]:", e)
                try:
                    if paciente_ctrl:
                        pacientes = paciente_ctrl.listar_pacientes()
                        if PacienteView:
                            PacienteView.mostrar_pacientes(pacientes)
                        else:
                            print(pacientes)
                except Exception as e:
                    print("[ERROR]:", e)
                try:
                    if medico_ctrl:
                        medicos = medico_ctrl.listar_medicos()
                        if MedicoView:
                            MedicoView.mostrar_medicos(medicos)
                        else:
                            print(medicos)
                except Exception as e:
                    print("[ERROR]:", e)
                try:
                    if administrador_ctrl:
                        admins = administrador_ctrl.listar_administradores()
                        if AdministradorView:
                            AdministradorView.mostrar_administradores(admins)
                        else:
                            print(admins)
                except Exception as e:
                    print("[ERROR]:", e)

            elif opt == "8":
                ruta = input("Ruta del archivo JSON (ej: usuarios.json): ").strip()
                cargar_usuarios_desde_json(ruta, usuario_ctrl)


            elif opt == "0":
                print("Saliendo...")
                break

            else:
                print("Opción inválida")

    finally:
        try:
            db.desconectar()
        except Exception:
            pass


if __name__ == "__main__":
    main()