import socket
import mimetypes

host, port = '127.0.0.1', 8888

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
serversocket.listen(1)
print('servidor en el puerto', port)

while True:
    connection, address = serversocket.accept()
    request = connection.recv(1024).decode('utf-8')
    # print(request)
    string_list = request.split(' ')
    method = string_list[0]
    requesting_file = string_list[1]
    mimeType = "text/html"

    print('Client request', requesting_file)

    myfile = requesting_file.split('?')[0]
    myfile = myfile.lstrip('/')

    def mimeType(type):
        return mimetypes.types_map[type]

    if(myfile == ''):
        myfile = 'index.html'

    try:
        file = open(myfile, 'rb')
        response = file.read()
        if(myfile.split('.')[1]):
            db = mimetypes.MimeTypes()
            db.readfp(file, True)
            types = db.types_map[True]
            mimeType = (
                "text/html", types["."+myfile.split('.')[1]])[types["."+myfile.split('.')[1]]]
        print(mimeType)
        file.close()

        header = 'HTTP/1.1 200 OK\n'
        header += 'Content-Type: '+mimeType+'\n\n'

    except Exception as e:
        print("-")
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body>Error 404: File not found</body></html>'.encode(
            'utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
