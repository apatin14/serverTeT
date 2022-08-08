import socket
import re
import magic
import os


host, port, header, response = '127.0.0.1', os.getenv('PORT'), "", ""

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
serversocket.listen(1)

print('Conection alive on: ', port)

while True:
    connection , address = serversocket.accept()
    data = connection.recv(1024)
    request = data.decode('utf-8')

    if (str.__contains__(request, 'GET')):
        fileName = "." + re.search('GET(.+?)HTTP', request).group(1).replace(' ', '')
        
        body = request.split('\r\n\r\n')[1]
        

        def setHeaders(partition):
            headers = {}
            for k, v in [i.split(':', 1) for i in partition[1:-1]]:
                headers[k.strip()] = v.strip()
            return headers

        
        def fileHandler(fileReadName, message):
            buferFile = open(fileReadName, 'rb')
            response = buferFile.read()
            buferFile.close()
            mime = magic.Magic(mime=True)
            mimeType = mime.from_file(fileReadName)
            header = 'HTTP/1.1 200 OK\n'+ 'Content-Type: '+mimeType+'\n\n'
            print("GET ", fileName, "HTTP/0.9 "+ message)
            return {'response': response, 'header': header} 

        if(fileName != './'):
            try:
                responseData = fileHandler(fileName, "Sucess")
                response = responseData['response']
                header = responseData['header']

            except Exception as e:
                responseData = fileHandler('./404.html', "ErrorFileName")
                response = responseData['response']
                header = responseData['header']
            if(body):
                request = request.replace(body, "")
                print("------Warning-------- Body is not Allowed")
            if(setHeaders([i.strip() for i in request.splitlines()])):
                print("------Warning-------- Headers are not Allowed")
                
        else:
            responseData = fileHandler('./404.html', "ErrorFileRoute")
            response = responseData['response']
            header = responseData['header']

    else:
        print("GET ", fileName, "HTTP/0.9 Error")
        header = 'HTTP/1.1 200 OK\n'
        header += 'Content-Type: '+"text/html"+'\n\n'
        response = '<body> <h1>Metodo no soportado. mas informacion <a href="https://riptutorial.com/http/example/30553/http-0-9">acá</a></h1> </body>'.encode('utf-8')    

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
