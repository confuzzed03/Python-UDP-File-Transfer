'''
Client Program

Assuming program is ran on beta.cse.ohio-state.edu (or any machine separate from server),
client will send all bytes of desired local file to server. Client will use following protocol:

    The payload of each UDP segment will contain the remote IP (4 bytes), remote port (2 bytes),
    and a flag (1 byte), followed by a data/control field as explained below. The flag takes 3 
    possible values depending on the data/control field:
    
        - First segment (4 bytes): The first segment should contain the number of bytes in the file to
            follow (in network byte order). The flag is set to a value of 1.
            
        - Second segment (20 bytes): The second segment should contain 20 bytes which is the name
            of the file (assume the name can fit in 20 bytes). The flag is set to a value of 2.
            
        - Other segments: The other segments will contain data bytes from the file to be transferred.
            Each segment can have up to 1,000 data bytes. The flag is set to a value of 3.
            
Buffer should not exceed 1000 bytes in size. 

Command should be:

    python ftpc.py <IP-address-of-gamma> <remote-port-on-gamma> <troll-port-on-beta> <local-file-to-transfer>

Created on October 17th, 2015

@author: Andy Kim
'''

# Import Packages
import sys
import os
import socket
import time
import select

# Check if a command line argument has been given
if len(sys.argv) > 4:
    # Get remote IP address/server name of gamma
    remoteIP = socket.gethostbyname(str(sys.argv[1]))
    # Get port number of gamma
    remotePort = int(sys.argv[2]).to_bytes(2, byteorder='big')
    # Get troll port on beta
    trollPort = int(sys.argv[3])
    # Get file path from command line arguments
    filepath = sys.argv[4]
    # Get file name from path
    fileName = os.path.basename(filepath)
    # Alternating bit protocol
    sequence = False
    # Checks if given file exists
    if os.path.isfile(filepath):
        # Get file size in bytes
        fileSize = os.path.getsize(filepath)
        # Check file size
        if fileSize > 0 and len(fileName) <= 20:
            # Create payload byte array
            payload = b''
            # Initialize flag
            flag = 1
            # Create remote IP byte array
            remoteByteArray = socket.gethostbyname(remoteIP).split('.')
            for byte in remoteByteArray:
                payload = payload + int(byte).to_bytes(1,byteorder='big')
            # Append remote port to payload
            payload += remotePort
            # Encode file name and size into bytes
            encodedFileName = fileName.rjust(20 - len(fileName)).encode(errors='ignore')
            fileSize = fileSize.to_bytes(4,byteorder = 'big')
            # Set up client socket
            clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            # Bind with HOST and PORT
            HOST = '' 
            PORT = 8000
            clientSocket.bind((HOST, PORT))
            # Send payload with first segment data, file size
            ip = socket.gethostbyname(socket.gethostname())
            clientSocket.sendto((payload+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+fileSize), (ip, trollPort))
            # Wait for ack or timeout
            while 1:
                print('Sending first segment')
                read, write, err = select.select([clientSocket],[],[],0.5)
                # If an ack is received and is expected, break loop
                if len(read) > 0 and int.from_bytes(read[0].recv(1),byteorder='big') == sequence:
                    print('ACK received for first segment!')
                    print(read)
                    break
                else:
                    clientSocket.sendto((payload+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+fileSize), (ip, trollPort))
            # Increment flag to second segment
            flag += 1
            # Alternate sequence number
            sequence = not(sequence)
            # Sleep in between sending udp packets
            time.sleep(0.5)
            # Send payload with second segment data, file name
            clientSocket.sendto((payload+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+encodedFileName), (ip, trollPort))
            # Wait for ack or timeout
            while 1:
                print('Sending second segment')
                read, write, err = select.select([clientSocket],[],[],0.5)
                # If an ack is received and is expected, break loop
                if len(read) > 0 and int.from_bytes(read[0].recv(1),byteorder='big') == sequence:
                    print('ACK received for second segment!')
                    break
                else:
                    clientSocket.sendto((payload+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+encodedFileName), (ip, trollPort))
            # Increment flag to third segment
            flag += 1
            # Alternate sequence number
            sequence = not(sequence)
            # Sleep in between sending udp packets
            time.sleep(0.5)
            # Read file in binary format
            with open(filepath, 'rb') as file:
                # Read up to first 900 bytes of file
                data = file.read(900);
                # Check if the read reached end of file
                while len(data) != 0:
                    # Send data to server
                    clientSocket.sendto((payload+flag.to_bytes(1, byteorder='big')+sequence.to_bytes(1,byteorder='big')+data), (ip, trollPort))
                    # Wait for ack or timeout
                    while 1:
                        read, write, err = select.select([clientSocket],[],[],0.5)
                        # If an ack is received and is expected, break loop
                        if len(read) > 0 and int.from_bytes(read[0].recv(1),byteorder='big') == sequence:
                            print('ACK received for third segment!')
                            break
                        else:
                            clientSocket.sendto((payload+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+data), (ip, trollPort))
                    # Alternate sequence number
                    sequence = not(sequence)
                    # Sleep in between sending UDP packets
                    time.sleep(0.5)
                    # Read up to next 900 bytes of file
                    data = file.read(900)
            # Close file after finish reading
            file.close()
            # Output server response confirmation
            print("Finished")
            # Close connection with server
            clientSocket.close()
        else:
            # Output error
            print("Error: not valid file")
    else:
        # Output error
        print("Error: file does not exist in local directory")
else:
    # Output error
    print("Error: invalid filename arguments")
