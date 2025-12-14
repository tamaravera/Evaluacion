import oracledb 

class conexion_oracle:
    def __init__(self, usuario: str, password: str, url:str):
        self.usuario = usuario
        self.password = password
        self.url = url
        self.connection = None

    def conectar(self):
        try:
            self.connection = oracledb.connect(
                user = self.usuario,
                password = self.password,
                dsn = self.url
            )
            print("[INFO]: Conectado a BD correctamente.")
        
        except oracledb.DatabaseError as e:
            msg = e.args[0].message if e.args and hasattr(e.args[0], 'message') else str(e)
            print(f"[ERROR]: No se pudo conectar a BD correctamente. -> {msg}")
    
    def desconectar(self):
        if self.connection:
            self.connection.close()
            print("[INFO]: Conexión a BD cerrada correctamente.")

    def obtener_cursor(self):

        if not self.connection:
            self.conectar()

        if not self.connection:
            raise RuntimeError("No se pudo establecer conexión a la BD")

        return self.connection.cursor()
    
def validar_tablas(db):

    tv_usuario ="""
            begin
                execute immediate '
                    create table tv_usuario(
                        id_usuario NUMBER PRIMARY KEY,
                        nombre_usuario VARCHAR2(50) NOT NULL,
                        clave VARCHAR2(100) NOT NULL,
                        nombre VARCHAR2(50) NOT NULL,
                        apellido VARCHAR2(50) NOT NULL,
                        fecha_nacimiento DATE NOT NULL,
                        telefono VARCHAR2(9) NOT NULL,
                        email VARCHAR2(100) NOT NULL,
                        tipo VARCHAR2(50) NOT NULL)'
                ;
            exception 
                when others then 
                    if sqlcode != -955 then
                        raise;
                    end if;
            end;
        """

    tv_paciente ="""
            begin
                execute immediate '
                    create table tv_paciente(
                        id_paciente NUMBER PRIMARY KEY,
                        comuna VARCHAR2(50) NOT NULL,
                        fecha_primera_visita DATE NOT NULL,

                        CONSTRAINT fk_usuario_paciente FOREIGN KEY(id_paciente) REFERENCES tv_usuario(id_usuario))'
                ;
            exception 
                when others then 
                    if sqlcode != -955 then
                        raise;
                    end if;
            end;
        """

    tv_medico ="""
            begin
                execute immediate '
                    create table tv_medico(
                        id_medico NUMBER PRIMARY KEY,
                        especialidad VARCHAR2(80) NOT NULL,
                        horario_atencion DATE NOT NULL,
                        fecha_ingreso DATE NOT NULL,

                        CONSTRAINT fk_usuario_medico FOREIGN KEY(id_medico) REFERENCES tv_usuario(id_usuario))'
                ;
            exception 
                when others then 
                    if sqlcode != -955 then
                        raise;
                    end if;
            end;
        """
    tv_administrador= """
            begin 
                execute immediate '
                    create table tv_administrador(
                        id_administrador NUMBER PRIMARY KEY,
                        CONSTRAINT fk_admin_usuario FOREIGN KEY(id_admin) REFERENCES tv_usuario(id_usuario))'
                ;
            execption
                when others then 
                    if sqlcode != -955 then
                        raise;
                    end if;
            end;
        """

    tv_insumos= """
            begin    
                execute immediate '
                    create table tv_insumos(
                        id_insumo NUMBER PRIMARY KEY,
                        nombre VARCHAR2(50) NOT NULL,
                        tipo VARCHAR2(50) NOT NULL,
                        stock NUMBER NOT NULL)'
                    ;
                exception 
                when others then
                    if sqlcode != -955 then
                        raise;
                    end if;
            end;
        """
      
    tv_recetas = """
            begin 
                execute immediate '
                    create table tv_recetas(
                        id_receta NUMBER PRIMARY KEY,
                        id_paciente NUMBER NOT NULL ,
                        id_medico NUMBER NOT NULL,
                        descripcion VARCHAR2(400),

                        CONSTRAINT fk_recetas_paciente FOREIGN KEY(id_paciente) REFERENCES tv_paciente(id_paciente),
                        CONSTRAINT fk_recetas_medico FOREIGN KEY(id_medico) REFERENCES tv_medico(id_medico))'
                    ;
                exception
                when others then
                if  sqlcode != -955 then
                    raise;
                end if;
            end;
        """

    tv_consultas = """
            begin
                execute immediate '
                    create table tv_consultas(
                        id_consulta NUMBER PRIMARY KEY,
                        id_paciente NUMBER,
                        id_medico NUMBER,
                        id_receta NUMBER,
                        fecha DATE NOT NULL,
                        comentarios VARCHAR2(400) NOT NULL,

                        CONSTRAINT fk_consultas_paciente FOREIGN KEY(id_paciente) REFERENCES tv_paciente(id_paciente),
                        CONSTRAINT fk_consultas_medico FOREIGN KEY(id_medico) REFERENCES tv_medico(id_medico),
                        CONSTRAINT fk_consultas_receta FOREIGN KEY(id_receta) REFERENCES tv_recetas(id_receta))'
                    ;
                exception
                when others then
                if  sqlcode != -955 then
                    raise;
                end if;
            end;                        
                        """

    tv_agenda = """
            begin
                execute immediate '
                    create table tv_agenda(
                        id_agenda NUMBER PRIMARY KEY,
                        id_paciente NUMBER NOT NULL,
                        id_medico NUMBER NOT NULL,
                        fecha_consulta DATE NOT NULL,
                        estado VARCHAR2(50) NOT NULL,
                        
                        CONSTRAINT fk_agenda_paciente FOREIGN KEY(id_paciente) REFERENCES tv_paciente(id_paciente),
                        CONSTRAINT fk_agenda_medico FOREIGN KEY(id_medico) REFERENCES tv_medico(id_medico))'
                    ;
                exception
                when others then
                if  sqlcode != -955 then
                    raise;
                end if;
            end;                        
                        """
        
    cursor = db.obtener_cursor()

    sentencias = [
        tv_usuario,
        tv_paciente,
        tv_medico,
        tv_administrador,
        tv_insumos,
        tv_recetas,
        tv_consultas,
        tv_agenda
    ]

    try:
        for sql in sentencias:
            cursor.execute(sql)

        db.connection.commit()

        print("[INFO]: Tablas validadas/creadas correctamente")
    except Exception as e:
        db.connection.rollback()

        print("[ERROR]: Error al crear tablas:", e)
    finally:
        if cursor:
            cursor.close()