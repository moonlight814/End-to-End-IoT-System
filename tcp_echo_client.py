import socket

# define valid queries
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

    # loop to allow multiple connection attempts until successful
    while True:
        try:
            # get the ip and port of the server from the user
            server_ip = input("Enter the server IP address: ").strip()
            if not server_ip:
                print("Server IP address cannot be blank.")
                continue # prompt for input again if blank

            server_port = input("Enter the server port number: ").strip()
            if not server_port.isdigit():
                print("Invalid port number. Please enter a valid number.")
                continue # prompt for input again if invalid
            
            # converts the port number to an integer
            server_port = int(server_port)
            
            # create a tcp/ip socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # connect to the server
            client_socket.connect((server_ip, server_port))
            print(f"Connected to {server_ip}:{server_port}")

            print("Valid Queries:")
            for query in VALID_QUERIES:
                print(f"- {query}")
            print("\nType 'exit' to quit the client.\n")
            
            # send and receive messages in a loop
            while True:
                query = input("Enter your query: ").strip()
                
                # handle exit command
                if query.lower() == 'exit':
                    print("Exiting the client.")
                    break # exit the loop if user types 'exit'

                # validate the query
                if query not in VALID_QUERIES:
                    print("\nSorry, this query cannot be processed.")
                    print("Please try one of the following:")
                    for valid_query in VALID_QUERIES:
                        print(f"- {valid_query}")
                    print()
                    continue

                # send the query to the server
                client_socket.send(query.encode())

            # close the client socket after exiting the loop
            client_socket.close()
            break

        except socket.error as e:
            # handle errors such as connection failure or invalid ip/port
            print(f"Error: {e}")
            print("Please enter a valid IP address and port.\n")

if __name__ == "__main__":
    # start the echo client
    start_client()
