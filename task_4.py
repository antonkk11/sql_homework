import psycopg2
from psycopg2 import Error
from psycopg2.extras import DictCursor
from torchgen.executorch.api.et_cpp import return_type


def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="netology_db",
            user="postgres",
            password="admin",
            host="localhost"
        )
        return conn
    except Error as e:
        print(f"Connection error: {e}")
        return None

def create_db_structure(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                phone_id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE,
                phone_number VARCHAR(20) UNIQUE
            );
        """)
        conn.commit()
        print("Database structure created successfully")

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO clients (first_name, last_name, email)
                VALUES (%s, %s, %s)
                RETURNING client_id;
            """, (first_name, last_name, email))
            client_id = cur.fetchone()[0]
            if phones:
                for phone in phones:
                    cur.execute("""
                        INSERT INTO phones (client_id, phone_number)
                        VALUES (%s, %s);
                    """, (client_id, phone))
            conn.commit()
            print(f"Client added with ID: {client_id}")
            return client_id
        except Error as e:
            conn.rollback()
            print(f"Error adding client: {e}")
            return None

def add_phone_to_client(conn, client_id, phone):
    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO phones (client_id, phone_number)
                VALUES (%s, %s);
            """, (client_id, phone))
            conn.commit()
            print("Phone added successfully")
        except Error as e:
            conn.rollback()
            print(f"Error adding phone: {e}")

def update_client(conn, client_id, first_name=None, last_name=None, email=None):
    updates = []
    params = []
    if first_name:
        updates.append("first_name = %s")
        params.append(first_name)
    if last_name:
        updates.append("last_name = %s")
        params.append(last_name)
    if email:
        updates.append("email = %s")
        params.append(email)
    if not updates:
        print("No data to update")
        return
    params.append(client_id)
    query = f"""
        UPDATE clients
        SET {', '.join(updates)}
        WHERE client_id = %s;
    """
    with conn.cursor() as cur:
        try:
            cur.execute(query, params)
            conn.commit()
            print("Client updated successfully")
        except Error as e:
            conn.rollback()
            print(f"Error updating client: {e}")

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        try:
            cur.execute("""
                DELETE FROM phones
                WHERE client_id = %s AND phone_number = %s;
            """, (client_id, phone))
            conn.commit()
            print("Phone deleted successfully")
        except Error as e:
            conn.rollback()
            print(f"Error deleting phone: {e}")

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        try:
            cur.execute("""
                DELETE FROM clients
                WHERE client_id = %s;
            """, (client_id,))
            conn.commit()
            print("Client deleted successfully")
        except Error as e:
            conn.rollback()
            print(f"Error deleting client: {e}")
        try:
            cur.execute("""
                            DELETE FROM phones
                            WHERE client_id = %s;
                        """, (client_id,))
            conn.commit()
            print("Client phones also deleted successfully")
        except Error as e:
            conn.rollback()
            print(f"Error deleting client: {e}")

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        where_clauses = []
        params = {}
        if first_name:
            where_clauses.append("c.first_name = %(first_name)s")
            params['first_name'] = first_name
        if last_name:
            where_clauses.append("c.last_name = %(last_name)s")
            params['last_name'] = last_name
        if email:
            where_clauses.append("c.email = %(email)s")
            params['email'] = email
        if phone:
            where_clauses.append("p.phone_number = %(phone)s")
            params['phone'] = phone

        if not where_clauses:
            print("At least one search parameter is required")
            return []

        join_clause = "LEFT JOIN phones p ON c.client_id = p.client_id" if phone else ""
        where_clause = "WHERE " + " AND ".join(where_clauses)

        # Условно добавляем p.phone_number в SELECT, только если phone передан
        select_phone = ", p.phone_number" if phone else ""
        query = f"""
            SELECT DISTINCT c.client_id, c.first_name, c.last_name, c.email {select_phone}
            FROM clients c
            {join_clause}
            {where_clause};
        """
        cur.execute(query, params)
        rows = cur.fetchall()

        clients = {}
        for row in rows:
            client_id = row['client_id']
            if client_id not in clients:
                clients[client_id] = {
                    'client_id': client_id,
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'phones': []
                }
            if phone and row.get('phone_number'):  # Добавляем телефон, только если phone передан
                clients[client_id]['phones'].append(row['phone_number'])
        return list(clients.values())

def delete_tables(conn, tables):
    with conn.cursor() as cur:
        for table in tables:
            print(f"Deleting table: {table}")
            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")

def main():
    conn = get_connection()

    delete_tables(conn, ["clients", "phones"])

    if not conn:
        return

    # Create tables
    create_db_structure(conn)

    # Add clients
    client1 = add_client(conn, "John", "Doe", "john.doe@example.com", ["123-456-7890"])
    client2 = add_client(conn, "Jane", "Smith", "jane.smith@example.com")

    # Add phone to client
    add_phone_to_client(conn, client2, "987-654-3210")

    # Update client
    update_client(conn, client1, email="john.new@example.com")

    # Find client by email
    print("Finding client by email:")
    found = find_client(conn, email="john.doe@example.com")
    for client in found:
        print(client)

    # Delete phone
    delete_phone(conn, client1, "123-456-7890")

    # Find client by name
    print("Finding client by name:")
    found = find_client(conn, first_name="John", last_name="Doe")
    for client in found:
        print(client)

    # Delete client
    delete_client(conn, client2)

    # Verify deletion
    print("Checking for deleted client:")
    found = find_client(conn, email="jane.smith@example.com")
    print(found)

    conn.close()

if __name__ == "__main__":
    main()
