"""
Assignment Requirements:

Update your TCP server to:
• Connect to the database created in Assignment 7 to retrieve relevant IoT data.
• Use metadata for each IoT device created in dataniz to manage and process queries
effectively. Metadata might include device ID, data source type, time zone, and unit of
measure.
• Perform calculations or unit conversions where needed:
- Convert moisture readings to RH% (Relative Humidity).
- Provide results in PST and imperial units (e.g., gallons, kWh).
• Use an efficient data structure (e.g., binary tree) for searching and managing the data.
"""

import socket
from pymongo import MongoClient
from datetime import datetime, timedelta
from pytz import timezone, utc

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

def convert_to_pst(utc_timestamp):
    """Convert a Unix timestamp to PST."""
    pst = timezone("US/Pacific")
    dt = datetime.fromtimestamp(utc_timestamp, tz=timezone.utc)
    return dt.astimezone(pst)

def process_query(query, db):
    """Process client query using MongoDB."""
    try:
        current_time = datetime.utcnow()
        three_hours_ago = current_time - timedelta(hours=3)

        if query == VALID_QUERIES[0]:  # Moisture query
            # Query MongoDB
            fridge_data = db.Databases_virtual_virtual.find({
                "payload.topic": "Link",  # Ensure topic matches
                "payload.timestamp": {"$exists": True}  # Ensure timestamp exists
            })

            # Debug: Print retrieved documents
            # print("Debug: Retrieved documents for moisture query:")
            # for doc in fridge_data:
            #     print(doc)

            # Reset cursor after printing for processing
            fridge_data = db.Databases_virtual_virtual.find({
                "payload.topic": "Link",
                "payload.timestamp": {"$exists": True}
            })

            # Extract readings safely
            readings = [
                float(doc.get("payload", {}).get("Moisture Meter - Moisture Meter", 0))
                for doc in fridge_data
                if "payload" in doc and "Moisture Meter - Moisture Meter" in doc["payload"]
            ]

            # Calculate and return average
            if readings:
                avg_moisture = sum(readings) / len(readings) * 0.75  # RH% conversion
                return f"Average Relative Humidity: {avg_moisture:.2f}% "
            return "No data available for the past three hours."


        elif query == VALID_QUERIES[1]:  # Water consumption query
            water_data = db.Databases_virtual_virtual.find({
                "payload.topic": "Link",
                "payload.Float Switch - Water Consumption Sensor": {"$exists": True}
            })
            readings = [float(doc["payload"]["Float Switch - Water Consumption Sensor"]) for doc in water_data]
            if readings:
                avg_water = sum(readings) / len(readings) * 0.264172  # Convert liters to gallons
                return f"Average Water Consumption: {avg_water:.2f} gallons"
            return "No data available for the dishwasher."

        elif query == VALID_QUERIES[2]:  # Electricity usage query
            # Processing electricity usage query
            return process_electricity_usage(db)

        return "Invalid query."
    except Exception as e:
        return f"Error processing query: {e}"

def process_electricity_usage(db):
    """Process electricity usage among devices."""
    try:
        # Define mappings for Ammeter fields based on board_name
        board_name_to_ammeter = {
            "Arduino Pro Mini - Arduino - Fridge": "Ammeter",
            "board 1 ceda25c7-92ba-45ea-a37e-b01c178946cc": "sensor 1 ff047cb5-6008-4f0b-aca7-c3dfb9baadbc",
            "Arduino Pro Mini - Arduino": "Ammeter - Washer"
        }

        # Voltage constant for power calculation
        VOLTAGE = 120

        # Query to fetch all relevant device data
        device_data = list(db.Databases_virtual_virtual.find({
            "payload.board_name": {"$in": list(board_name_to_ammeter.keys())}
        }))

        if not device_data:
            return "No electricity usage data available."

        # Process each device's energy consumption
        devices_consumption = []
        for doc in device_data:
            # Extract board_name and Ammeter field
            board_name = doc["payload"]["board_name"]
            ammeter_field = board_name_to_ammeter.get(board_name)

            # Safely get Ammeter reading
            ammeter_value = float(doc["payload"].get(ammeter_field, 0))

            # Assume each reading represents a 1-hour interval
            power_watts = ammeter_value * VOLTAGE  # Power in watts
            energy_kwh = power_watts / 1000  # Convert to kWh

            # Add energy consumption data for the device
            devices_consumption.append({
                "board_name": board_name,
                "energy_kwh": energy_kwh
            })

        # Find the device with the highest energy consumption
        max_device = max(devices_consumption, key=lambda x: x["energy_kwh"])
        board_name = max_device["board_name"]
        total_kwh = max_device["energy_kwh"]

        # Map board_name to user-friendly device names
        board_name_to_device = {
            "Arduino Pro Mini - Arduino - Fridge": "Fridge 1",
            "board 1 ceda25c7-92ba-45ea-a37e-b01c178946cc": "Fridge 2",
            "Arduino Pro Mini - Arduino": "Dishwasher"
        }

        # Get device name or fallback to board_name
        device_name = board_name_to_device.get(board_name, f"Unknown Device ({board_name})")

        return f"{device_name} consumed the most electricity: {total_kwh:.2f} kWh"
    except Exception as e:
        return f"Error processing electricity usage query: {e}"



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
                        response = f"Invalid query. Please try one of the following: {', '.join(VALID_QUERIES)}."

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
    db_name = "test"
    db = connect_to_mongodb(mongo_uri, db_name)
    if db is not None:  # Explicitly check for None
        host = input("Enter host: ").strip()
        port = int(input("Enter port: ").strip())
        start_server(host, port, db)
    else:
        print("Failed to connect to MongoDB. Please check your connection.")
