Overview:
    An http server made almost exclusively using the Python Standard Library.
    This server focuses on controlling external access to source, database and webpage data.
        Private:     Items in the project base and src folders are unavailable to outside requests.
        Conditional: Requests for data from the db folder have extra processing through the server before it is given.
        Public:      Items in the www folder are available to anyone that requests for it by its path.

Dependencies: 
    python3.7+
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

    Configuration options can be set using arguments through the termimal.
        Any key can be set; even new keys that are not part of the program and have no effect.
        These arguments will override any options set though config.json
        From the project src folder enter into a terminal:
            sudo python3 main.py port=80 baseDirectory=/home/admin/server

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

Front-End Instructions
-Create html/script/style files in the www folder to be called from a client browser.
    The only request methods supported are GET, POST and HEAD with HEAD being un-optimized
-GET requests
    To request a file in the www folder simply request it by it's path and filename.
      ex. "/subpage/style.css"
      ex. "/images/banner.jpeg"
    To request data that requires the server to read from the private database, check its state
    or authenticate the user request use the appropriate server action call.
-Server Actions
    To request the server to peform an action send the appropriate url and query argument(s).
    Query arguments are always key/value pairs
      ex. /post?filetype=image
      ex. /get?filetype=image&name=my_image
-POST requests
    Currently the only request body content-types supported are 'multipart/form-data' and 'application/json'
    The content-type of the data sent must either be inferred within the backend or specified through query arguments
     Inferred in the backend
       ex. /post
     Specified in the url
       ex. /post?filetype=image

Back-End Instructions
-Creating Custom Logic for Webpages:
    Create an index.html for the page at an appropiate location within the www folder
    Copy the file /src/pages/pageTemplate.py and rename the copy.
    Open the renamed file and rename the class PageTemplate(..)
    Add custom logic to the overridden performAction function.
    Import the copied file into pageIndex.py
    Register the new page logic in pageIndex.py by creating an instance in the pages dictionary
        www/index.html                    >> YourWebpage("/", "") 
        www/targetpage/index.html         >> YourWebpage("/", "targetpage") 
        www/subpage/targetpage/index.html >> YourWebpage("/subpage/", "targetpage")
        NOTE: when creating the webpage instance the pathname must begin and end with a /
    Call the page where needed through pageIndex.pages[key].process(..)
-Url Parameters
    Url parameters are extracted from the url and added to a dictionary (params).
    These parameters can be accessed within the weblogic files
      ex. "/post?filetype=image" >> "filetype" is called with: params["query"]["filetype"]
-Cookies
    Add cookies the the response header with the "Set-Cookie" attribute in the http response header.
      ex. "Set-Cookie": "value=myData=123; Path=/"
      ex. "Set-Cookie": "value=myData1=123&mydata2=456; Path=/"
    Cookies received through an http request are added to a dictionary (params).
      The values from the previous examples can be accessed in weblogic files using: params["cookies"]["value"]["myData"]
-Non-Cookie Headers
    All non-cookie header values are stored in a dictionary (params).
      ex. to access the "Host" attribute use: params["headers"]["Host"]

Using the Command Interface:
    There are 3 sections the the windowed interface. The status bar, the output display and the command entry.
    The status and output displays are to display relevent information to the user of the interface.
    Commands can be entered into the interface to perform various actions.
        Configuration options can be added, changed and read but this currently has no effect.
        Currently the only useful function of the interface is to quit the program.