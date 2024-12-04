import socket
from pymongo import MongoClient
from datetime import datetime, timedelta


# Define valid queries
VALID_QUERIES = [
    "What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "Which device consumed more electricity among my three IoT devices?"
]


def connect_to_mongodb(uri, db_name):
    """Connect to MongoDB."""
    try:
        client = MongoClient(uri)
        db = client[db_name]
        print("Connected to MongoDB.")
        return db
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None


def process_query(query, db):
    """Process client query using MongoDB."""
    try:
        if query == VALID_QUERIES[0]:
            current_time = datetime.utcnow()
            three_hours_ago = current_time - timedelta(hours=3)
            fridge_data = db.fridge_data.find({"timestamp": {"$gte": three_hours_ago}})
            readings = [doc.get("moisture", 0) for doc in fridge_data]
            if readings:
                avg_moisture = sum(readings) / len(readings)
                return f"Average Relative Humidity: {avg_moisture * 0.75:.2f}%"
            return "No data available for the past three hours."

        elif query == VALID_QUERIES[1]:
            result = list(
                db.dishwasher_data.aggregate([
                    {"$group": {"_id": None, "average_water": {"$avg": "$water_consumption"}}}
                ])
            )
            if result:
                avg_water = result[0]["average_water"] * 0.264172
                return f"Average Water Consumption: {avg_water:.2f} gallons"
            return "No data available for the dishwasher."

        elif query == VALID_QUERIES[2]:
            result = list(
                db.electricity_data.aggregate([
                    {"$group": {"_id": "$device_id", "total_usage": {"$sum": "$electricity_usage"}}}
                ])
            )
            if result:
                max_device = max(result, key=lambda x: x["total_usage"])
                return f"Device {max_device['_id']} consumed the most electricity: {max_device['total_usage']:.2f} kWh"
            return "No electricity usage data available."
    except Exception as e:
        return f"Error processing query: {e}"

    return "Invalid query."


def start_server(host, port, db):
    """Start the TCP server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print(f"Server listening on {host}:{port}...")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to {client_address}")

            try:
                while True:
                    query = client_socket.recv(1024).decode("utf-8")
                    if not query:
                        break
                    print(f"Received query: {query}")

                    if query in VALID_QUERIES:
                        response = process_query(query, db)
                    else:
                        response = "Invalid query. Please try again."

                    client_socket.send(response.encode("utf-8"))
            except Exception as e:
                print(f"Error: {e}")
            finally:
                client_socket.close()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    mongo_uri = "mongodb+srv://nataliaargumedo02:hello@327a6.lnmyx.mongodb.net/?retryWrites=true&w=majority&appName=327A6"
    db_name = "327A6"
    db = connect_to_mongodb(mongo_uri, db_name)
    if db:
        host = input("Enter host: ").strip()
        port = int(input("Enter port: ").strip())
        start_server(host, port, db)
