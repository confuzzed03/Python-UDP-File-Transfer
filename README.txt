CSE 3461 Lab 3

Section: Tuesdays & Thursdays, 2:20 - 3:40 pm

Summary
	There is one program called ftpc.py that rests on the client side
	and one called ftps.py that rests with the server side. The client
	will transfer a file via the UDP protocol to the server side. The
	client will first send packets to troll which will then be forwarded
	to the server side. The server will receive the file in packets and
	save it in the sub-directory, 'recv'.

Instructions

	Important Note:
		The server program must be used first, then the troll command, followed by
		the client program. 
		
		To execute the server side program ftps.py, use the following command:
			python3 ftps.py <local-port-on-gamma>
		
		An example would be:
			python3 ftps.py 8008
			
		Assuming troll file is downloaded, to execute troll, use the following command:
			./troll -C <IP-address-of-beta> -S <IP-address-of-gamma> -a 8000
				-b <server-port-on-gamma> -r -t -x 0 <troll-port-on-beta>
		
		An example would be:
			./troll -C beta.cse.ohio-state.edu -S gamma.cse.ohio-state.edu -a 8000
				-b 8008 -r -t -x 0 8080
				
		Note: Client port is hard coded with port number 8000. You must use this number.
	
		To execute the client side program ftpc.py, use the following command:
			python3 ftpc.py <IP-address-of-gamma> <remote-port-on-gamma> <troll–port-on-beta>
				<local-file-to-transfer>
				
		An example would be:
			python3 ftpc.py gamma.cse.ohio-state.edu 8008 8080 1.jpg