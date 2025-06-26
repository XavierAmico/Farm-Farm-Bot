from database import connect
from datetime import datetime, timezone

colors = {"Black", "Blue", "Cyan", "Green", "Magenta", "Red", "White", "Yellow"}

def get_today():
    utc_now = datetime.now(timezone.utc)
    return utc_now.strftime("%B %d, %Y")

def add(color, x, y, server):
    today = get_today()
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO pearls (date, color, x, y, server)
                    VALUES (%s, %s, %s, %s, %s)
                """, (today, color, x, y, server))
            conn.commit()
        print(f"✅ Inserted {color} pearl at ({x}, {y}) for {today}")
        return True
    except Exception as e:
        print(f"❌ DB error: {e}")
        return False

def is_duplicate(color, x, y, server):
    today = get_today()
    with connect().cursor() as cur:
        cur.execute("""
            SELECT 1 FROM pearls
            WHERE date = %s AND color = %s AND x = %s AND y = %s AND server = %s
        """, (today, color, x, y, server))
        return cur.fetchone() is not None

def get_pearls(server):
    today = get_today()
    with connect().cursor() as cur:
        cur.execute("""
            SELECT color, x, y FROM pearls
            WHERE date = %s AND server = %s
            """, (today, server))
        results = cur.fetchall()
        return [{"color": row[0], "x": row[1], "y": row[2]} for row in results]

def remove(x, y, server):
    today = get_today()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM pearls
                WHERE date = %s AND x = %s AND y = %s AND server = %s
                RETURNING *
            """, (today, x, y, server))
        conn.commit()
        return cur.rowcount > 0

def clear(server):
    today = get_today()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM pearls
            WHERE date = %s AND server = %s
        """, (today, server))
    conn.commit()
