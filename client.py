"""
Assignment Requirements:

Update your TCP client to:
• Accept and process the following three queries only:
1. What is the average moisture inside my kitchen fridge in the past three hours?
2. What is the average water consumption per cycle in my smart dishwasher?
3. Which device consumed more electricity among my three IoT devices (two
refrigerators and a dishwasher)?
• Reject any other input with a user-friendly message, e.g., 'Sorry, this query cannot be
processed. Please try one of the following: [list the valid queries].'
• Send valid queries to your TCP server for processing.
• Display results from the server to the user.
"""

import socket

# Queries that the client can send to the server
VALID_QUERIES = [
    "What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "Which device consumed more electricity among my three IoT devices?"
]

def start_client():
    """
    - connects to the server using a TCP connection
    - sends messages to the server and receives responses
    - allows the client to send multiple messages in a loop and exit when needed
    """

    while True: # Retry loop for connection attempts and queries
        try:
            # This gets the server IP address and port number from the user
            server_ip = input("Enter the server IP address: ").strip()
            if not server_ip:
                print("Server IP address cannot be blank.")
                continue

            server_port = input("Enter the server port number: ").strip()
            if not server_port.isdigit():
                print("Invalid port number. Please enter a valid number.")
                continue
            
            server_port = int(server_port)
            
            # creates a TCP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            client_socket.connect((server_ip, server_port)) # connects to the server
            print(f"Connected to {server_ip}:{server_port}")

            print("Valid Queries:")
            for i, query in enumerate(VALID_QUERIES, start=1):
                print(f"{i}. {query}")
            print("\nType 'exit' to quit the client.\n")
            
            # Loop for continuously sending queries to the server by the client
            while True:
                user_input = input("Enter your query number or type your query: ").strip()
                
                if user_input.lower() == 'exit': # Gracefully exit the client
                    print("Exiting the client.")
                    break

                # Check if input is a valid query number OR a query string
                if user_input.isdigit():
                    query_index = int(user_input) - 1
                    if 0 <= query_index < len(VALID_QUERIES):
                        query = VALID_QUERIES[query_index]
                    else:
                        print("Invalid query number. Please choose a valid number.\n")
                        continue
                else:
                    query = user_input # this is the query string entered by the user
                
                if query not in VALID_QUERIES: # Reject invalid/unknown queries
                    print("\nSorry, this query cannot be processed.")
                    print("Please try one of the following:")
                    for i, valid_query in enumerate(VALID_QUERIES, start=1):
                        print(f"{i}. {valid_query}")
                    print()
                    continue

                # send the query to the server
                client_socket.send(query.encode())

                # This waits for receives the response from the server
                response = client_socket.recv(1024).decode()
                if not response:
                    print("Server closed the connection.")
                    break

                print(f"Server response: {response}\n")

            client_socket.close() # Cleans up the connection before exiting the client
            break

        except socket.error as e:
            # handle errors such as connection failure or invalid ip/port
            print(f"Error: {e}")
            print("Please enter a valid IP address and port.\n")

if __name__ == "__main__":
    start_client()

"""
NOTES:
- Make sure your TCP server is running before starting this script. Otherwise, the client will keep throwing connection errors.

- For local testing:
  1. Run the server script on your machine using `python3 tcp_server.py`.
  2. Run the client script on the same machine or another local device using `python3 tcp_client.py`.

- For VM testing:
  1. Use `gcloud compute ssh` to access the VMs
  2. Upload the server script to one VM instance and run it using `python3 tcp_server.py`.
  3. On another VM instance or locally, run the client script and connect to the server using the server's external IP and the assigned port.
  4. Ensure both instances are in the same network or have open firewall rules for the port used by the server.
"""