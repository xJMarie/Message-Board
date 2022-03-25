# Message Board Project CSNETWK S11
# Authors:  AGULTO, Juliana Marie B.
#           NORONA, Yeohan Lorenzo M.
# Group 4

import socket, sys, json, os

def commandfuncs(users, jdata):
    numCommand = 401
    
    if "command" not in jdata:
        numCommand = 301
    elif jdata["command"] == "register":
        if jdata["username"] not in users:
            if (jdata["username"] != ""):
                users.append(jdata["username"])
                print(f"Users in message board: {users}")
        else:
            numCommand = 502 # Register failed User already exists
    elif jdata["command"] == "deregister":
        if (jdata["username"] != ""):
            users.remove(jdata["username"])
            print(f"User {jdata['username']} exiting...")
            print(f"Users in message board: {users}")
    elif jdata["command"] == "msg":
        if jdata["username"] == "":
            numCommand = 501 # Message failed: User does not exist
        else: 
            print(f"from {jdata['username']} : {jdata['message']}")
    else:
        numCommand = 201
    return numCommand

# -- Main function of the program --
def main():
    users = [] 
    ipaddress = input("Input listening IP address: ")
    port = input("Input listening port number: ")

    while not port.isdigit() or int(port) <= 0:
        print("Invalid port number.")
        port = input("Enter destination port number of message board server: ").strip()

    port = int(port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"Server starting up on {ipaddress} port {port}")
    sock.bind(('', port))
    print('\nServer started waiting to receive message')

    while True:
        data, address = sock.recvfrom(1024)
        jdata =json.loads(data)
        num = commandfuncs(users, jdata)  
        commands = {
                    401 : {"command" : "ret_code", "code_no" : 401},
                    501 : {"command" : "ret_code", "code_no" : 501},
                    502 : {"command" : "ret_code", "code_no" : 502},
                    201 : {"command" : "ret_code", "code_no" : 201},
                    301 : {"command" : "ret_code", "code_no" : 301}
                    }
        
        if data:
            msg = json.dumps(commands[num])
            send = sock.sendto(bytes(msg,"utf-8"), address)
#----------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except:
        print()
        try:
            sys.exit(0)
        except:
            os._exit(0)