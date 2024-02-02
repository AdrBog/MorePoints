# Connecting to an external FTP server

You do not need to run **server.py** to use More Points.

More Points can connect to other FTP servers, in this article you will learn how to do that.

> [!IMPORTANT]
> You will obviously need to know the user credentials of the FTP server you want to connect to first.

## Configuring the point

Let's suppose we have the following FTP server:
```txt
FTP SERVER
Host:           192.168.100.2:21
User:           john
Password:       password123
```

- Go to the More Points control panel ( /admin ) and create a new point.

- Enter the point configuration ( /admin/edit_point/POINT_NAME )

- Go to **FTP** Section

- In **Host**, enter the address where the FTP server is hosted. In this case, **192.168.100.2**

- In **User**, enter the address where the FTP server is hosted. In this case, **john**

- And in **Password**, enter the user's password. In this case, **password123**
> [!IMPORTANT]
> More Points will never share your password with any person or agency.

> [!NOTE]
> Configuring **Root** and **Permissions** does not make sense in this case because we are talking about an FTP server that has not been created with **server.py**.
- Save changes

If everything has been done correctly, you should be able to connect to the external FTP server using More Points

