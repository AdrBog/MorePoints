# Creating the FTP server

In case you do not have any FTP server to connect. The **server.py** file will generate an FTP server for you quickly.

Users are configured in **config/ftp_users.json** <br>

Once you configured the users, run server.py
```bash
python server.py
```
in case of error, try running as sudo
```bash
sudo python server.py
```

If there have been no errors, the users have been created and the FTP server is active, you will see an output like this in the terminal.

```txt
>>> starting FTP server on 127.0.0.1:21, pid=xxxx <<<
```

You do not need to use More Points to access the FTP server, you can access it using the ftp command or the browser.

