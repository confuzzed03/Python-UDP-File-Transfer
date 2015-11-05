CSE 3461 Lab 4

Section: Tuesdays & Thursdays, 2:20 - 3:40 pm

Summary
	There is one program called ftpc.py that rests on the client side
	and one called ftps.py that rests with the server side. The client
	will transfer a file via UDP protocol to the server side. The
	client will first send packets to troll which will then be forwarded
	to the server side. The server will receive the file in packets and
	save it in the sub-directory, 'recv'. Server will send an ACK back to
	client via troll. Alternating bit protocol is used to synchronize file
	transfer between client and server.

Instructions

	Important Note:
	
		The server program must be used first, then the troll command for client (beta),
		then troll command for server (gamma), followed by the client program. 
		
		To execute the server side program ftps.py, use the following command:
			python3 ftps.py <local-port-on-gamma> <troll-port-on-gamma>
		
		An example would be:
			python3 ftps.py 8008 8005

		For client (beta), use the following troll command:

			./troll -C <IP-address-of-beta> -S <IP-address-of-gamma> -a 8000
				-b <server-port-on-gamma> <troll-port-on-beta> -t -x <packet-drop-%>

		An example would be:
			./troll -C beta.cse.ohio-state.edu -S gamma.cse.ohio-state.edu -a 8000 -b 8008
				8006 -t -x 10

		For server (gamma), use the following troll command:

			./troll -C <IP-address-of-gamma> -S <IP-address-of-beta> -a 8000
				-b <client-port-on-beta> <troll-port-on-gamma> -t -x <packet-drop-%>

		An example would be:
			./troll -C gamma.cse.ohio-state.edu -S beta.cse.ohio-state.edu -a 8008 -b 8000
				8005 -t -x 10

		Note: Client port is hard coded with port number 8000. You must use this number.
	
		To execute the client side program ftpc.py, use the following command:
			python3 ftpc.py <remote-IP-gamma> <remote-port-on-gamma> <troll–port-on-beta>
				<local-file-to-transfer>
				
		An example would be:
			python3 ftpc.py gamma.cse.ohio-state.edu 8008 8006 1.jpg