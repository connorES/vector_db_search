from database.db_connection import OnPremServerConnection

def execute_query(query, params=None):
    with OnPremServerConnection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def example(x, y):
    query = """
        SELECT Columns
        FROM Table 
        WHERE x = ?
        AND y = ?
    """
    return execute_query(query, [x, y])