import socket  # Import socket module for networking

def main():

    # Try to create a TCP socket
    try:
        myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket (IPv4)
    except socket.error as err:
        # Print an error message if socket creation fails
        print("Failure to create socket.")
    
    # Get the host and port number from the user
    host = input("Enter host: ")  # Input for the host (IP address or hostname)
    port = int(input("Enter port: "))  # Input for the port number

    # Bind the socket to the specified host and port
    myTCPSocket.bind((host, port))  # Bind the socket to the provided host and port

    # Start listening for incoming connections (max queue size of 2)
    myTCPSocket.listen(2)  # The server listens for incoming connections, allowing up to 2 clients to wait in the queue

    # Accept an incoming connection
    incomingSocket, incomingAddress = myTCPSocket.accept()  # Accept a new connection when a client tries to connect
    print(f"{incomingAddress} is connected!")  # Print the address of the connected client

    # Receive data from the client (max 1024 bytes) and decode it from UTF-8
    myData = incomingSocket.recv(1024).decode("utf-8")  # Read the message sent by the client

    # Loop to continuously receive and respond to client messages
    try:
        while myData:  # Continue as long as there is data from the client
            print("Client says: ", myData)  # Print the message received from the client
            myData = myData.upper()  # Convert the message to uppercase
            incomingSocket.send(bytearray(myData, encoding="utf-8"))  # Send the modified message back to the client
            myData = incomingSocket.recv(1024).decode("utf-8")  # Receive the next message from the client
    except:
        # If an error occurs, close the socket
        incomingSocket.close()  # Close the socket when done or in case of an error

# Call the main function to run the server
main()
