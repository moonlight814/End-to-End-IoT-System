# End-to-End-IoT-System

## CECS 327 - Intro to Networking and Distributed Systems  
**Assignment 8: Build an End-to-End IoT System**  

---

## Objective  
The goal of this assignment is to build a fully functional end-to-end IoT system integrating:  
- TCP client/server communication.  
- Database.  
- IoT sensor data and metadata to process user queries.

---

## Learning Objectives  
1. Integrate IoT sensors and databases into a complete system.  
2. Improve TCP client-server communication using real-world IoT data.  
3. Utilize metadata for IoT devices for enhanced system functionality.  
4. Perform data analysis and unit conversions.  
5. Gain hands-on experience with cloud deployment and system integration.  

---

## Prospective Features  
- **TCP Client:**  
  - Accepts three specific queries:  
    1. Average moisture inside the kitchen fridge in the past three hours.  
    2. Average water consumption per cycle in the smart dishwasher.  
    3. Device consuming the most electricity among three IoT devices.  
  - Rejects invalid queries with user-friendly messages.  
  - Sends valid queries to the TCP server.  
  - Displays results from the server.  

- **TCP Server:**  
  - Connects to the database for IoT data retrieval.  
  - Utilizes device metadata (e.g., device ID, unit of measure).  
  - Performs calculations and unit conversions, including:  
    - Relative Humidity (RH%) conversion.  
    - Results in PST and imperial units (gallons, kWh).  
  - Efficiently manages data with a binary tree structure.  

- **IoT Sensor Research:**  
  - Documentation of IoT sensors used, including data type, precision, and time zones.  
  - Explanation of metadata usage for device management.  

---

## System Requirements  
- **Programming Languages:** Python 
- **Database:** MongoDB
- **IoT Platform:** Dataniz for metadata and virtual IoT devices.  

---

### Running the System  
1. **Start the TCP Server:**  
   ```bash
   python server.py
   ```
2. **Start the TCP Client:**  
   ```bash
   python client.py
   ```
3. Ensure the database is configured and running with relevant IoT data.  
