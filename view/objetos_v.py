from datetime import date

class InsumosView:
    @staticmethod
    def mostrar_insumos(insumos: list) -> None:
        if insumos:
            print("\n[INFO]:- Insumos -")
            for i in insumos:
                print(f"[INFO]:--- ID: {i.get('id_insumo')} | Nombre: {i.get('nombre')} | Tipo: {i.get('tipo')} | Stock: {i.get('stock')}")
        else:
            print("[ERROR]: Sin registro en insumos.")

class RecetasView:
    @staticmethod
    def mostrar_recetas(recetas: list) -> None:
        if recetas:
            print("\n[INFO]:- Recetas -")
            for r in recetas:
                print(f"[INFO]:--- ID: {r.get('id_receta')} | ID_paciente: {r.get('id_paciente')} | ID_medico: {r.get('id_medico')} | Descripcion: {r.get('descripcion')}")
        else:
            print("[ERROR]: Sin registro en recetas.")

class ConsultasView:
    @staticmethod
    def mostrar_consultas(consultas: list) -> None:
        if consultas:
            print("\n[INFO]:- Consultas -")
            for c in consultas:
                fecha = c.get('fecha')
                fecha_str = fecha.isoformat() if isinstance(fecha, date) else str(fecha)
                print(f"[INFO]:--- ID: {c.get('id_consulta')} | ID_paciente: {c.get('id_paciente')} | ID_medico: {c.get('id_medico')} | ID_receta: {c.get('id_receta')} | Fecha: {fecha_str} | Comentarios: {c.get('comentarios')}")
        else:
            print("[ERROR]: Sin registro en consultas.")

class AgendaView:
    @staticmethod
    def mostrar_agenda(agendas: list) -> None:
        if agendas:
            print("\n[INFO]:- Agenda -")
            for a in agendas:
                fecha = a.get('fecha_consulta')
                fecha_str = fecha.isoformat() if isinstance(fecha, date) else str(fecha)
                print(f"[INFO]:--- ID: {a.get('id_agenda')} | ID_paciente: {a.get('id_paciente')} | ID_medico: {a.get('id_medico')} | Fecha_consulta: {fecha_str} | Estado: {a.get('estado')}")
        else:
            print("[ERROR]: Sin registro en agenda.")