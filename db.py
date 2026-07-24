import os, sqlite3
DATABASE_URL=os.getenv("DATABASE_URL", "").strip()
IS_POSTGRES=bool(DATABASE_URL)
DB_INTEGRITY_ERROR=sqlite3.IntegrityError
if IS_POSTGRES:
    try:
        import psycopg
        from psycopg.rows import dict_row
        DB_INTEGRITY_ERROR=psycopg.errors.UniqueViolation
    except ImportError as exc:
        raise RuntimeError("DATABASE_URL is set but psycopg is not installed. Install psycopg[binary].") from exc
class PGConnection:
    def __init__(self,url): self.conn=psycopg.connect(url, row_factory=dict_row)
    def _sql(self,sql):
        for name in ("pending_verification","pending","paid","cancelled"):
            sql=sql.replace(chr(34)+name+chr(34), chr(39)+name+chr(39))
        return sql.replace("?","%s")
    def execute(self,sql,params=()): return self.conn.execute(self._sql(sql),params)
    def executemany(self,sql,params): return self.conn.executemany(self._sql(sql),params)
    def commit(self): self.conn.commit()
    def close(self): self.conn.close()
def db():
    if IS_POSTGRES: return PGConnection(DATABASE_URL)
    c=sqlite3.connect("appointments.db",timeout=5);c.row_factory=sqlite3.Row;c.execute("PRAGMA journal_mode=WAL");return c
