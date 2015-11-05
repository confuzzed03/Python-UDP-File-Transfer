'''
Server Program

Assuming program is ran on gamma.cse.ohio-state.edu (or any machine separate from client),
server will receive a binary file from client. File will be saved in directory 'recv'. 
Server and client will use the following protocol:

    The payload of each UDP segment will contain the remote IP (4 bytes), remote port (2 bytes),
    a flag (1 byte), and a 1-bit sequence number (1 byte), followed by a data/control field as explained 
    below. The flag takes 3 possible values depending on the data/control field:
    
        - First segment (4 bytes): The first segment should contain the number of bytes in the file to
            follow (in network byte order). The flag is set to a value of 1.
            
        - Second segment (20 bytes): The second segment should contain 20 bytes which is the name
            of the file (assume the name can fit in 20 bytes). The flag is set to a value of 2.
        
        - Other segments: The other segments will contain data bytes from the file to be transferred.
            Each segment can have up to 1,000 data bytes. The flag is set to a value of 3.

    
Buffer should not exceed 1000 bytes in size. Using alternating bit protocol, server will send ACK for
every packet received to client.

Command should be:

    python3 ftps.py <local-port-on-gamma> <troll-port-on-gamma>

Created on November 5th, 2015

@author: Andy Kim
'''

# Import Packages
import sys
import os
import socket

# Check if a command line argument has been given
if len(sys.argv) > 2:
    # Get local port number from command line arguments
    serverPort = int(sys.argv[1])
    # Get troll port number on gamma from command line arguments
    trollPort = int(sys.argv[2])
    # Create HOST and PORT
    HOST = ''
    # Create IP
    ip = socket.gethostbyname(socket.gethostname())
    # Create ack
    ack = False
    # Create TCP welcoming socket
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    serverSocket.bind((HOST,serverPort))
    print('The server is waiting for packets')
    # Loop forever to continue accepting connections
    while 1:
        # Get payload and address from first UDP segment
        payload, addr = serverSocket.recvfrom(12)
        # Get sequence number
        sequence = payload[7]
        # Check if sequence matches with ack
        while sequence != ack:
            print('Wrong sequence for first segment!')
            # Send ack to client
            serverSocket.sendto(sequence.to_bytes(1,byteorder='big'), (ip,trollPort))
            # Get payload and address from first UDP segment
            payload, addr = serverSocket.recvfrom(12)
            # Get sequence number
            sequence = payload[7]
        # Receive encoded file size and decode
        fileSize = int.from_bytes(payload[8:len(payload)], byteorder='big')
        print('The file size is: ',fileSize)
        # Send ack to client
        serverSocket.sendto(ack.to_bytes(1,byteorder='big'), (ip,trollPort))
        # Alternate ack
        ack = not(ack)
        # Get payload and address from second UDP segment
        payload, addr = serverSocket.recvfrom(28)
        # Get sequence number
        sequence = payload[7]
        # Check sequence number
        while sequence != ack:
            print('Wrong sequence for second segment!')
            # Send ack to client
            serverSocket.sendto(sequence.to_bytes(1,byteorder='big'), (ip,trollPort))
            # Get payload and address from first UDP segment
            payload, addr = serverSocket.recvfrom(28)
            # Get sequence number
            sequence = payload[7]
        # Receive encoded file name, remove padding, and decode
        fileName = payload[8:len(payload)].decode(errors='ignore').lstrip()
        print('The name of the file is: ',fileName)
        # Send ack to client
        serverSocket.sendto(ack.to_bytes(1,byteorder='big'), (ip,trollPort))
        # Alternate ack
        ack = not(ack)
        # Establish output file with associated directory
        outputFile = os.getcwd() + "/recv/" + fileName
        # Make recv directory if not present
        os.makedirs(os.path.dirname(outputFile), exist_ok=True)
        # Overwrite copy of file if it exists
        open(outputFile, 'w').close()
        x = 1
        # Open file to write and append file bytes
        with open(outputFile, 'ab') as output:
            # Keep receiving data till you reach file size
            while fileSize > 0:
                print('Counter: ',x)
                # Get payload and address from third UDP segments
                payload, addr = serverSocket.recvfrom(908)
                # Get sequence number
                sequence = payload[7]
                # Check sequence number
                while sequence != ack:
                    print('Wrong sequence for third segment!')
                    # Send ack to client
                    serverSocket.sendto(sequence.to_bytes(1,byteorder='big'), (ip,trollPort))
                    # Get payload and address from first UDP segment
                    payload, addr = serverSocket.recvfrom(908)
                    # Get sequence number
                    sequence = payload[7]
                # Extract data from payload, up to last 900 bytes
                data = payload[8:len(payload)]
                # Send ack to client
                serverSocket.sendto(ack.to_bytes(1,byteorder='big'), (ip,trollPort))
                # Alternate ack
                ack = not(ack)
                # Write binary data to output file
                output.write(data)
                # Update file size remaining to retrieve
                fileSize -= len(data)
                print('Remaining file size: ', fileSize)
                x = x + 1
        # Close output file
        output.close()
        # Print to server prompt successful copy
        print('Copied file in recv directory:', fileName)
        # Send successful file copy confirmation to client
        serverSocket.sendto(('File copy successful!').encode(errors='ignore'), (ip,trollPort))
else:
    # Output error for invalid command line arguments
    print('Error: invalid command line arguments')
