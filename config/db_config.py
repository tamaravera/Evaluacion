import logging
import time
from contextlib import contextmanager
from typing import Optional, Iterator

import oracledb


logger = logging.getLogger(__name__)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class conexion_oracle:
    def __init__(self, usuario: str, password: str, url: str, connect_retries: int = 1, retry_delay: float = 1.0):
        self.usuario = usuario
        self.password = password
        self.url = url
        self.connection: Optional[oracledb.Connection] = None
        self.connect_retries = max(1, int(connect_retries))
        self.retry_delay = float(retry_delay)

    def __enter__(self) -> "conexion_oracle":
        self.conectar()
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            self.desconectar()
        except Exception:
            logger.exception("Error al desconectar en __exit__")

    def conectar(self) -> None:
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.connect_retries + 1):
            try:
                self.connection = oracledb.connect(
                    user=self.usuario,
                    password=self.password,
                    dsn=self.url
                )
                logger.info("Conectado a BD correctamente.")
                return
            except oracledb.Error as e:
                last_exc = e
                logger.warning("Intento %d/%d: no se pudo conectar -> %s", attempt, self.connect_retries, e)
                if attempt < self.connect_retries:
                    time.sleep(self.retry_delay)

        logger.error("No se pudo conectar a la BD después de %d intentos.", self.connect_retries)
        if last_exc:
            raise last_exc

    def desconectar(self) -> None:
        if self.connection:
            try:
                self.connection.close()
                logger.info("Conexión a BD cerrada correctamente.")
            finally:
                self.connection = None

    def obtener_cursor(self):
        if not self.connection:
            self.conectar()

        if not self.connection:
            raise RuntimeError("No se pudo establecer conexión a la BD")

        return self.connection.cursor()

    @contextmanager
    def cursor(self) -> Iterator[oracledb.Cursor]:
        cur = None
        try:
            cur = self.obtener_cursor()
            yield cur
        finally:
            if cur:
                try:
                    cur.close()
                except Exception:
                    logger.exception("Error cerrando el cursor")


def validar_tablas(db: conexion_oracle) -> None:
    tv_usuario = """
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
                tipo VARCHAR2(50) NOT NULL
            )';
    exception
        when others then
            if sqlcode != -955 then
                raise;
            end if;
    end;
    """

    tv_paciente = """
    begin
        execute immediate '
            create table tv_paciente(
                id_paciente NUMBER PRIMARY KEY,
                comuna VARCHAR2(50) NOT NULL,
                fecha_primera_visita DATE NOT NULL,
                CONSTRAINT fk_usuario_paciente FOREIGN KEY(id_paciente) REFERENCES tv_usuario(id_usuario)
            )';
    exception
        when others then
            if sqlcode != -955 then
                raise;
            end if;
    end;
    """

    tv_medico = """
    begin
        execute immediate '
            create table tv_medico(
                id_medico NUMBER PRIMARY KEY,
                especialidad VARCHAR2(80) NOT NULL,
                horario_atencion DATE NOT NULL,
                fecha_ingreso DATE NOT NULL,
                CONSTRAINT fk_usuario_medico FOREIGN KEY(id_medico) REFERENCES tv_usuario(id_usuario)
            )';
    exception
        when others then
            if sqlcode != -955 then
                raise;
            end if;
    end;
    """

    tv_administrador = """
    begin
        execute immediate '
            create table tv_administrador(
                id_administrador NUMBER PRIMARY KEY,
                CONSTRAINT fk_usuario_administrador FOREIGN KEY(id_administrador) REFERENCES tv_usuario(id_usuario)
            )';
    exception
        when others then
            if sqlcode != -955 then
                raise;
            end if;
    end;
    """

    tv_insumos = """
    begin
        execute immediate '
            create table tv_insumos(
                id_insumo NUMBER PRIMARY KEY,
                nombre VARCHAR2(50) NOT NULL,
                tipo VARCHAR2(50) NOT NULL,
                stock NUMBER NOT NULL,
                costo_usd NUMBER NOT NULL
            )';
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
                id_paciente NUMBER NOT NULL,
                id_medico NUMBER NOT NULL,
                descripcion VARCHAR2(400),
                medicamentos_recetados VARCHAR2(400) NOT NULL,
                costo_clp NUMBER NOT NULL,
                CONSTRAINT fk_recetas_paciente FOREIGN KEY(id_paciente) REFERENCES tv_paciente(id_paciente),
                CONSTRAINT fk_recetas_medico FOREIGN KEY(id_medico) REFERENCES tv_medico(id_medico)
            )';
    exception
        when others then
            if sqlcode != -955 then
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
                valor NUMBER NOT NULL,
                CONSTRAINT fk_consultas_paciente FOREIGN KEY(id_paciente) REFERENCES tv_paciente(id_paciente),
                CONSTRAINT fk_consultas_medico FOREIGN KEY(id_medico) REFERENCES tv_medico(id_medico),
                CONSTRAINT fk_consultas_receta FOREIGN KEY(id_receta) REFERENCES tv_recetas(id_receta)
            )';
    exception
        when others then
            if sqlcode != -955 then
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
                CONSTRAINT fk_agenda_medico FOREIGN KEY(id_medico) REFERENCES tv_medico(id_medico)
            )';
    exception
        when others then
            if sqlcode != -955 then
                raise;
            end if;
    end;
    """

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

    cursor = None
    try:
        cursor = db.obtener_cursor()
        for idx, sql in enumerate(sentencias, start=1):
            try:
                cursor.execute(sql)
                logger.debug("Sentencia %d ejecutada correctamente.", idx)
            except Exception:
                logger.exception("Error ejecutando la sentencia %d:", idx)
                raise


        if db.connection:
            db.connection.commit()
        logger.info("Tablas validadas/creadas correctamente")

    except Exception as e:

        if db.connection:
            try:
                db.connection.rollback()
                logger.info("Rollback ejecutado tras error al crear tablas")
            except Exception:
                logger.exception("Error ejecutando rollback")
        logger.error("Error al crear/validar tablas: %s", e)
        raise
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                logger.exception("Error cerrando cursor en validar_tablas")