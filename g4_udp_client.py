# Message Board Project CSNETWK S11
# Authors:  AGULTO, Juliana Marie B.
#           NORONA, Yeohan Lorenzo M.
# Group 4

import socket, sys, json, os

# -- Checks the server return code to client --
def checkUser(data):
    if ((data["command"] == "ret_code") and (data["code_no"] == 401)):
        print("Registered successfully.")
        return True
    elif ((data["command"] == "ret_code") and (data["code_no"] == 201)):
        print("Command parameters incomplete.")
    elif ((data["command"] == "ret_code") and (data["code_no"] == 301)):
        print("Command unknown.")
    elif ((data["command"] == "ret_code") and (data["code_no"] == 501)):
        print("User not registered in messages server, message rejected. Exiting...")
    elif ((data["command"] == "ret_code") and (data["code_no"] == 502)):
        print("User account already exists in chat room!")  
    else:
        return False
    
    return False
#----------------------------------------------

# -- Checks the server return code to client --
def checkMessage(data):
    if ((data["command"] == "ret_code") and (data["code_no"] == 501)):
        print("User not registered in messages server, message rejected.  Exiting...")
        return False
    elif ((data["command"] == "ret_code") and (data["code_no"] == 401)):
        print("Message sent succesfully.")
    return True
#----------------------------------------------

# -- Main function of the program --
def main():
    isConnected = True     # To check if user is connected

    # Client command codes to server 
    cmdRegister = {"command" : "register"}
    cmdDeregister = {"command" : "deregister"}
    cmdMsg = {"command" : "msg"}

    # Set variables for server address and destination port
    serverHost = input("Enter IP address of message board server: ")
    destPort = input("Enter destination port number of message board server: ").strip()

    # Condition to check if the destination port entered is a integer.
    while not destPort.isdigit() or int(destPort) <= 0:
        print("Invalid port number.")
        destPort = input("Enter destination port number of message board server: ").strip()

    destPort = int(destPort)

    # Sets the username for message board
    username = input("Enter preferred username: ")
    if (username != ""):
        cmdRegister["username"] = username
        cmdDeregister["username"] = username
        cmdMsg["username"] = username
    else:
        cmdRegister["username"] = ""
        cmdDeregister["username"] = ""
        cmdMsg["username"] = ""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # To create a UDP socket
    message = json.dumps(cmdRegister)       # Form JSON protocol format and send to server

    try:        
        if (username != ""):
            print (f"Registering username {username}")  # Prints the username
        else:
            print ("Registering username anonymous")  # Prints the username
        send = sock.sendto(bytes(message,"utf-8"), (serverHost,destPort))   # Sending the data. Converts the string to 'bytes'.
        data, server = sock.recvfrom(1024)      # Waiting for the server to return the data
    finally:
        jdata = json.loads(data)    # Used to parse a valid JSON string and convert it into a Python Dictionary
        isConnected = checkUser(jdata)   # Checks the server return code to client
        if (isConnected != True):
            print("Unsucessful registration. Exiting...")

    while isConnected:
        try:
            try:
                msg = input("Enter message: ")
                cmdMsg["message"] = msg
                message = json.dumps(cmdMsg)
                send = sock.sendto(bytes(message,"utf-8"), (serverHost,destPort))
            except:
                print()
                try:
                    sys.exit(0)
                except:
                    os._exit(0)
        finally:
                data, server = sock.recvfrom(1024)      # Waiting for the server to return the data
                jdata = json.loads(data)
                if msg == "bye":
                    print("Disconnecting...")
                    message = json.dumps(cmdDeregister)
                    send = sock.sendto(bytes(message,"utf-8"), (serverHost,destPort))
                    isConnected = False
                else:
                    isConnected = checkMessage(jdata)   # Checks the server return code to client
#----------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except:
        try:
            print()
            sys.exit(0)
        except:
            os._exit(0)