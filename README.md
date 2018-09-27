Overview:
    An http server made almost exclusively using the Python Standard Library.

Dependencies: 
    python3.6+
    python3-bcrpyt

Setup:
    Clone the repository. 
    In the project base directory create a database folder named: db
    Create a config.json. (see Creating config.json)
    Set
    Set firewall permissions to allow tcp connections on the chosen port.
    If on a local network:
        Create routing rules on the routing device to direct messages
        on the chosen port to the hosting device.

Running the Server:
    From the project src folder enter into a terminal:
        sudo python3 main.py
    If no config.json exists the server will run on localhost port 80 by default.

Accessing the Server's Services:
    In a browser enter the domain name or ip address of the host/router of the device running the server

Creating config.json:
    config.json is a simple json file containing key/value pairs to be imported when the server is started.
    See file configAllKeys to see all available keys along with their type/description.
    
    For config.json to be found it must be located in the project's 
      base directory where the src, www, and db folders are located

    The following is an example of config.json where the host is on a local network
    and main.py is located at /home/admin/server/src/main.py
    {
           "baseDirectory": "/home/admin/server",
           "ip4host": "192.168.1.XXX",
           "port": 80
    }