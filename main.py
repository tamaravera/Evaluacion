

from utils.helpers import rows_to_dicts, validar_tablas

DB_CONFIG = {
    "host": "localhost",
    "dbname": "mediplus",
    "user": "postgres",
    "password": "postgres"
}

def main ():
    db = conexion_oracle(
        usuario="Tu usuario",
        password="Tu contraseña",
        url= "Tu_dsn_oracle"
    )
    db.conectar()
    
     try: 
            validar_tablas(db)
            insumos_ctrl= InsumosController(db)
            recetas_ctrl= RecetasController(db)
            consultas_ctrl= ConsultasController(db)
            agenda_ctrl= AgendaController(db)
            
            #INSUMOS
            cur = db.obtener_cursor()
            rows = insumos_ctrl.listar_insumos(cur)
            insumos = rows_to_dics(cur, rows)
            InsumosView.mostrar_insumos(insumos)
            cur.close()

            #RECETAS
            cur = db.obtener.cursor()
            rows = recetas_ctrl.listar_recetas(cur)
            recetas = rows_to_dics(cur, rows)
            RecetasView.mostrar_recetas(recetas)
            cur.close()

            #CONSULTAS
            cur = db.obtener.cursor()
            rows = consultas_ctrl.listar_consultas(cur)
            consultas = rows_to_dics(cur, rows)
            ConsultasView.mostrar_consultas(consultas)    
            cur.close()

            #AGENDA
            cur = db.obtener.cursor()
            rows = agenda_ctrl.listar_agenda(cur)
            agendas = rows_to_dics(cur, rows)
            AgendaView.mostrar_agenda(agendas)
            cur.close()

        except Exception as e:
        print(f"[ERROR]:", e)

        finally:
        db.desconectar()

    if __name__ =="__main__":
    main()

