import asyncio
import websockets
import json
import psycopg2
from decimal import Decimal

# Decimal to JSON encoder class.
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

async def send_products(websocket, path):
    try:
        db_host = 'localhost'
        db_name = 'websocket-db'
        db_user = 'postgres'
        db_password = 'FAq1auyu@'

        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        # Bubble sort for price.
        for i in range(len(products)-1):
            for j in range(len(products)-i-1):
                if products[j][2] > products[j+1][2]:
                    products[j], products[j+1] = products[j+1], products[j]

        # JSON convert.
        products_json = json.dumps(products, cls=DecimalEncoder)

        # Sending products to client.
        await websocket.send(products_json)

    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()

start_server = websockets.serve(send_products, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
