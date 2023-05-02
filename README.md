# world.ly

## **Configuration Instructions For Windows**

1. Clone the world.ly repository on your local device

2. Install the latest version of Python from the Microsoft Store (Version 3.11 latest as of now)

3. Add Python Installation path to Environment System Variables
    - Search for 'Edit the system environment variables'
    - Click 'Environment Variables' in the botton right corner
    - Then under 'System variables', double-click the 'Path' variable
    - Select 'New' in the top right corner
    - Type the path of the python installation (i.e., C:\Program Files\Python311)
    - Click 'OK', then 'OK' again, and then 'OK' a third time to close all the windows
    - To make sure Python has installed correctly, open a Command Prompt by typing 'Command Prompt' in the search bar
    - Then type
    
            python --version
    - If the version shows, Python has been installed correctly
    
4. Download the Oracle Instant Client package from the Oracle website for Windows (https://www.oracle.com/database/technologies/instant-client/downloads.html)

5. After downloading the Oracle Instant Client, make a new folder called 'Oracle' in your local drive's 'Program Files' (C:\Program Files\Oracle)

6. Extract the contents of the Oracle Instant Client in the 'Oracle' folder (So, should have C:\Program Files\Oracle\instantclient_21_9)

7. Add Oracle Instant Client to Environment System Variables
    - Search for 'Edit the system environment variables'
    - Click 'Environment Variables' in the botton right corner
    - Then under 'System variables', double-click the 'Path' variable
    - Select 'New' in the top right corner
    - Type the path of the oracle installation (C:\Program Files\Oracle\instantclient_21_9)
    - Click 'OK', then 'OK' again, and then 'OK' a third time to close all the windows
    
10. Download Microsoft C++ Build Tools (https://visualstudio.microsoft.com/visual-cpp-build-tools/)

11. Open Visual Studio Installer and click the 'Available' tab

12. Then install 'Visual Studio Community 2022' (latest year available)
    - When propmpted to install workloads, select 'Desktop development with C++' 
    - If this is not prompted, finish installing 'Visual Studio Community 2022'
        - Then go to the 'Installed' tab and select 'Modify' under 'Visual Studio Community 2022'
        - Select the box labled 'Desktop development with C++' and install

13. After installing open a new Command Prompt

14. Navigate to the 'world.ly' repository (i.e., C:\world.ly)

15. Run 
    
    'pip install -r requirements.txt'
    
16. If prompted to, add any new paths in Environment System Variables, then re-run the last step


## **Running On Local Host for Windows**

1. Download UFL VPN, if you do not have (https://net-services.ufl.edu/provided-services/vpn/clients/)

2. Connect to UFL VPN by opening the Cisco AnyConnect Secure Mobility Client

3. Type 'vpn.ufl.edu' in the bar if prompted to and insert ufl credentials

4. Open a Command Prompt and navigate to the world.ly repository (i.e., C:\world.ly)

5. Run

    python main.py
    
6. Open a web browser and type 'http://127.0.0.1:8050' in the URL 

7. Have fun with world.ly!



    
## **Configuration Instructions For Mac**

1. Install the latest version of Python (https://www.python.org/downloads/)
2. Install pip     
    
        python3 get-pip.py
3. Download the Oracle Instant Client package from the Oracle website for your operating system    (https://www.oracle.com/database/technologies/instant-client/downloads.html)

4. After extraction (see download instructions), add the directory containing the Instant Client files to your system's PATH environment variable.

        export DYLD_LIBRARY_PATH="Instant Client Directory"

5. Install the cx_Oracle package

        pip3 install cx_Oracle

6. Install Dash and its required packages

        pip3 install dash dash-renderer dash-html-components dash-core-components




## **Running On Local Host For Mac**

1. Connect to UFL VPN.
2. Set environment variable

        export DYLD_LIBRARY_PATH="Instant Client Directory"
3. In terminal, navigate to project directory and run the Python Dash App 

        python3 app.py
4. Open http://127.0.0.1:8050/ on a web browser
   


### **UFL CISE Oracle Database Server Used**
Username: williamsobczak <br />
Password= REBY7TpizLTdOp5dZHa9qJS0



### **Credits:**
Created by Group 2 
