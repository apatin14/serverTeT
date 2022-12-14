const http = require("http");
const url = require('url');
var fs = require("fs");

const server = http.createServer((req, res) => {
  function setContent(content) {
    res.setHeader("Content-Type", "text/html");
    res.writeHead(200);
    res.end(content, "utf-8");
  }

  if (req.method === "GET") {
    if( req.headers || url.parse(req.url, true).query)console.log("Opción o Valor Desconocido")
    fs.readFile("./" + req.url, function (error, content) {
      if (error) {
        fs.readFile("./404.html", function (error, errorContent) {
          setContent(errorContent);
        });
      } else {
        setContent(content);
      }
    });
  } else {
    setContent('<body> <h1> La solictud no es soportada, para mayor informacion puedes dar click <a href="https://riptutorial.com/http/example/30553/http-0-9">aca</a></h1> </body>')
  }
}).listen((process.env.PORT || 80));
