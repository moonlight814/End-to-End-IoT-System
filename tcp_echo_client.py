import socket

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

            # send and receive messages in a loop
            while True:
                message = input("Enter the message to send (or type 'exit' to quit): ").strip()
                
                # validates that the message is not empty
                if not message:
                    print("Message cannot be blank.")
                    continue  # don't send blank messages
                
                if message.lower() == 'exit':
                    print("Exiting the client.")
                    break  # exit the loop if user types 'exit'

                try:
                    # send message to the server
                    client_socket.send(message.encode())

                    # receive the response from the server
                    response = client_socket.recv(1024)
                    if not response:
                        print("Server closed the connection.")
                        break  # if no response, the server closed the connection
                    print(f"Server response: {response.decode()}") # display the server's response

                except socket.error as e:
                    print(f"Error during communication: {e}")
                    break  # handle any communication errors

            # close the client socket after exiting the loop
            client_socket.close()
            break

        except socket.error as e:
            # handle errors such as connection failure or invalid ip/port
            print(f"Error: {e}")
            print("Please enter a valid IP address and port.")

if __name__ == "__main__":
    # start the echo client
    start_client()
