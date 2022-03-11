# Team-Network-Tactics
A game for the mandatory assignment.

Group 35

Ola Opdahl

Andreas Mærland

How to run:
   First, install mysql-connector (https://www.codespeedy.com/how-to-install-mysql-connector-in-python/)

   Database (Required: MySQL Worbench or similar, WAMPserver)
1. In MySQL Workbench create a MySQL connection with root username, no password, on localhost.
2. Run WAMPSERVER64
3. Creat schema called champions in connection.
4. Import table (.mwb) in schema and then add table info to it from the csv file.

   Python scripts (Use CLI)
1. Run dbFetcher.py
2. Run server.py
3. Run client.py (Player1)
4. Run client.py (Player2)
