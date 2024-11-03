# CS4450_5450_PA-2
ASU CS 4450/5450 Networking Class Programming Assignment 2 

I. Introduction

A  proxy server (web cache) is a program that acts as a middleman between a web browser and an origin server. Instead of contacting the origin server directly to get a web page, the browser contacts the proxy, which forwards the request to the origin server. When the origin server replies to the proxy, the proxy sends the reply to the browser.  In addition, the proxy server caches the response from the server so that the next time a request arrives for that page, the proxy server can respond without contacting the origin server.

Proxies are used for many purposes. Sometimes proxies are used in firewalls so that the proxy is the only way for a browser inside the firewall to contact an origin server outside the firewall. The proxy may do a translation on the page, for instance, to make it viewable on a Web-enabled cell phone. Proxies are also used for privacy.  By stripping a request of all identifying information, a proxy can make the browser anonymous to the end server.

For this assignment, you will write (chiefly) the client portion of the proxy.  Your proxy will:

Accept a URL as a command-line argument.
If the object is not cached, establish a TCP connection with the server and send an HTTP request to the server. If the status of the HTTP response is 200, it should then cache the object.
Display the HTTP response (either the one from the server or the cached one).


II. Getting Started

Log into GitHub and visit the following URL. 

https://classroom.github.com/a/_c-n70hS

This will create for you a private repository on GitHub.  Log into student2.cs.appstate.edu, get into your 4450 or 5450 directory, and use the clone command to create the repository on the student2 machine.  The only thing provided for you is a .gitignore file and the file proxy.py that contains the main.  This code references two classes, proxyClient, and cacheDir.  You can rename these classes, use more classes, write the code in a procedural way instead of object-oriented, etc.   You are required to write easy to read, well-documented code, with small single-purpose functions.


III. Sample Outputs

1) First access to a page.  The object will come from the server. Print a message indicating the object is coming from the server, the response header, and the response body.  Don't print response body if it is binary.

student> ./proxy.py http://www.cs.appstate.edu/~can/4450/page1.html
---RETURNING OBJECT FROM SERVER---
HTTP/1.1 200 OK
Date: Mon, 17 Sep 2018 00:28:26 GMT
Server: Apache/2.2.31 (Unix) mod_ssl/2.2.31 OpenSSL/1.0.1e-fips DAV/2 PHP/5.6.25 mod_wsgi/4.5.5 Python/2.6.6 mod_perl/2.0.9 Perl/v5.10.1
Last-Modified: Mon, 17 Sep 2018 00:20:35 GMT
ETag: "8c8012-6a-5760624553ac0"
Accept-Ranges: bytes
Content-Length: 106
Vary: Accept-Encoding
Connection: close
Content-Type: text/html

<HTML>
<HEAD>
<TITLE>Page One</TITLE>
</HEAD>

<BODY>
<p>
<b>
This is page one.
</b>
</p>
</BODY>
</HTML>

2) Second access to a page.  The object will come from the cache. Print a message indicating it is from the cache. Notice the header is not the same as the header that came from the server.  It is a header that was built from information in the cache.

student2> ./proxy.py http://www.cs.appstate.edu/~can/4450/page1.html
---RETURNING OBJECT FROM CACHE---
HTTP/1.1 200 OK
Connection: close
Last-Modified: Mon, 17 Sep 2018 00:20:35 GMT
Content-Length: 106
Content-Type: text/html


<HTML>
<HEAD>
<TITLE>Page One</TITLE>
</HEAD>

<BODY>
<p>
<b>
This is page one.
</b>
</p>
</BODY>
</HTML>

3) An access to an image file will only cause the header to be displayed.

student2> ./proxy.py http://www.cs.appstate.edu/~can/4450/picture1.png
---RETURNING OBJECT FROM SERVER---
HTTP/1.1 200 OK
Date: Mon, 17 Sep 2018 00:33:11 GMT
Server: Apache/2.2.31 (Unix) mod_ssl/2.2.31 OpenSSL/1.0.1e-fips DAV/2 PHP/5.6.25 mod_wsgi/4.5.5 Python/2.6.6 mod_perl/2.0.9 Perl/v5.10.1
Last-Modified: Mon, 17 Sep 2018 00:17:11 GMT
ETag: "8c800e-25b43-57606182c6fc0"
Accept-Ranges: bytes
Content-Length: 154435
Connection: close
Content-Type: image/png

Content is binary

4) If the url is invalid, the http response status code will not be 200.  Don't cache the object, but still display the header and the body.

student2> ./proxy.py http://www.cs.appstate.edu/~can/4450/badfile.html
---RETURNING OBJECT FROM SERVER---
HTTP/1.1 404 Not Found
Date: Mon, 17 Sep 2018 00:35:40 GMT
Server: Apache/2.2.31 (Unix) mod_ssl/2.2.31 OpenSSL/1.0.1e-fips DAV/2 PHP/5.6.25 mod_wsgi/4.5.5 Python/2.6.6 mod_perl/2.0.9 Perl/v5.10.1
Vary: Accept-Encoding
Content-Length: 220
Connection: close
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL /~can/4450/badfile.html was not found on this server.</p>
</body></html>

IV. Cache
The cache consists of two components.  A directory file will be used to connect each object to the file used to store the object.  In addition, the directory can be used to hold the most important header lines.  For example, after the accesses made in Part II, the directory might contain this:

student2> more cacheDir.txt
www.cs.appstate.edu/~can/4450/page1.html|Last-Modified: Mon, 17 Sep 2018 00:20:35 GMT|Content-Length: 106|Content-Type:
text/html|1
www.cs.appstate.edu/~can/4450/picture1.png|Last-Modified: Mon, 17 Sep 2018 00:17:11 GMT|Content-Length: 154435|Content-T
ype: image/png|2

Each line represents a single object.  The fields of a line are separated by the | character.  The last field (1 and 2) is the name of the file containing the object. Thus, the directory containing the code also contains the files: cacheDir.txt, 1, and 2.  If another, different object is accessed, the cacheDir.txt file will be modified and the file 3 will be created.

In addition, the proxy program should also accept a clean option instead of a URL.  The clean option will cause the cache directory and files to be deleted.

student2> proxy.py clean
Cleaning
Removing 1
Removing 2
Removing cacheDir.txt

V. Implementation Details

Your instructor's implementation used two classes.  The cacheDir class manages the cache.  It opens up the directory file and reads the contents into a list.  It has methods that check to see if a particular object has been cached, add an object to the cache (updates the list, the cache directory file, and creates a file to contain the object), clean the cache, build the http response header from the cache directory, and build the http response body from the object file. 

The proxyClient class has methods to parse the URL to get the host, build an HTTP request, contact the server, get and display an object from either the cache or the origin server. 

You can come up with your design.  

The most important tasks to be performed are the following:

1. Contacting the origin server. 
You'll need to parse the URL to grab the host. For example, the host within http://www.cs.appstate.edu/~can/4450/picture1.png is www.cs.appstate.edu.  The host and port 80 will be passed to the call to connect. The HTTP request will need to contain a GET with the input URL, a Host: header, and a Connection: close header.  You will need to encode the header using 'utf-8' before sending it the server, for example:
clientSocket.send(request.encode('utf-8'))
Since the length of the response is unknown, you'll need to read it in a loop, for example:
responseAll = bytearray();
while 1:
         response = clientSocket.recv(1024)
         if not response: break
         responseAll += response;

2. Caching the object.
Do not cache the response unless the status code is 200. The response from the server is a sequence of bytes.  Your code will need to separate the response into the header component and the body component.  Recall that the header and body is separated by "\r\n\r\n".  The header portion can be decoded and output to the display.  The encoded body portion (the bytes) should be stored in a file.  If you do this correctly, you'll see that the size of the file is the same as the value in the Content-Length.  Because you will be storing binary data, you will need to use the "wb" option to open for writing the object to the file. 

3. Updating the cache directory.
When the program starts, read the cache directory into a list structure.  Then it will be easy to check to see if an object is cached by going through that list.  Caching an object will require updating both the list and the cache directory stored in a file.  You can update the file by opening it with the "a" option (append).  

VI. Final Notes
You can test your code on the following:

http://www.cs.appstate.edu/~can/4450/page1.html

http://www.cs.appstate.edu/~can/4450/page2.html

http://www.cs.appstate.edu/~can/4450/page3.html

http://www.cs.appstate.edu/~can/4450/picture1.png

http://www.cs.appstate.edu/~can/4450/picture2.jpg

http://www.cs.appstate.edu/~can/4450/picture3.jpg

You don't need to handle any content types other than: text/html, image/png, and image/jpeg.

Start early and ask questions when you need help.



The program will be accepted up to one week late with a penalty of 5 points per day.

