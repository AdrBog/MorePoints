# Creating the FTP server

In case you do not have any FTP server ready. The **server.py** file will generate an FTP server for you quickly.

> [!NOTE]
> Before running **server.py**, configure the points in the More Points administration panel (/admin).

Run server.py

```bash
python server.py
```
in case of error, try running as sudo
```bash
sudo python server.py
```

**server.py** will look in **config/points** to see the points you have configured, and create the respective users with passwords and permissions.

If there have been no errors, the users have been created and the FTP server is active, you will see an output like this in the terminal.

```txt
>>> starting FTP server on 127.0.0.1:21, pid=xxxx <<<
```

You do not need to use More Points to access the FTP server, you can access it using the ftp command or the browser.

