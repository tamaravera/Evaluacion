from datetime import date
from typing import List, Dict, Any, Optional


class InsumosView:
    @staticmethod
    def mostrar_insumos(insumos: List[Dict[str, Any]]) -> None:
        if insumos:
            print("\n[INFO]:- Insumos -")
            for i in insumos:
                costo = i.get("costo_usd")
                costo_str = f"{float(costo):.2f} USD" if costo is not None else "N/A"
                print(
                    f"[INFO]:--- ID: {i.get('id_insumo')} | Nombre: {i.get('nombre')} | "
                    f"Tipo: {i.get('tipo')} | Stock: {i.get('stock')} | Costo: {costo_str}"
                )
        else:
            print("[ERROR]: Sin registro en insumos.")


class RecetasView:
    @staticmethod
    def mostrar_recetas(recetas: List[Dict[str, Any]]) -> None:
        if recetas:
            print("\n[INFO]:- Recetas -")
            for r in recetas:
                costo = r.get("costo_clp")
                costo_str = f"{float(costo):.2f} CLP" if costo is not None else "N/A"
                print(
                    f"[INFO]:--- ID: {r.get('id_receta')} | ID_paciente: {r.get('id_paciente')} | "
                    f"ID_medico: {r.get('id_medico')} | Descripcion: {r.get('descripcion')} | "
                    f"Medicamentos: {r.get('medicamentos_recetados')} | Costo: {costo_str}"
                )
        else:
            print("[ERROR]: Sin registro en recetas.")


class ConsultasView:
    @staticmethod
    def mostrar_consultas(consultas: List[Dict[str, Any]]) -> None:
        if consultas:
            print("\n[INFO]:- Consultas -")
            for c in consultas:
                fecha = c.get("fecha")
                fecha_str = fecha.isoformat() if isinstance(fecha, date) else str(fecha)
                valor = c.get("valor")
                valor_str = f"{float(valor):.2f}" if valor is not None else "N/A"
                print(
                    f"[INFO]:--- ID: {c.get('id_consulta')} | ID_paciente: {c.get('id_paciente')} | "
                    f"ID_medico: {c.get('id_medico')} | ID_receta: {c.get('id_receta')} | "
                    f"Fecha: {fecha_str} | Comentarios: {c.get('comentarios')} | Valor: {valor_str}"
                )
        else:
            print("[ERROR]: Sin registro en consultas.")


class AgendaView:
    @staticmethod
    def mostrar_agenda(agendas: List[Dict[str, Any]]) -> None:
        if agendas:
            print("\n[INFO]:- Agenda -")
            for a in agendas:
                fecha = a.get("fecha_consulta")
                fecha_str = fecha.isoformat() if isinstance(fecha, date) else str(fecha)
                print(
                    f"[INFO]:--- ID: {a.get('id_agenda')} | ID_paciente: {a.get('id_paciente')} | "
                    f"ID_medico: {a.get('id_medico')} | Fecha_consulta: {fecha_str} | Estado: {a.get('estado')}"
                )
        else:
            print("[ERROR]: Sin registro en agenda.")