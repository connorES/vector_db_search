from pyodbc import connect


class OnPremServerConnection:
    def __init__(self):
        self.conn = None
        self.connection_string = "connection string"

    def __enter__(self):
        self.conn = connect(self.connection_string)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
