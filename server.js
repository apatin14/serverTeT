const http = require("http");
var fs = require("fs");

const server = http.createServer((req, res) => {
  function setContent(content) {
    res.setHeader("Content-Type", "text/html");
    res.writeHead(200);
    res.end(content, "utf-8");
  }

  fs.readFile("./" + req.url, function (error, content) {
    if (error) {
      fs.readFile("./404.html", function (error, errorContent) {
        setContent(errorContent);
      });
    } else {
      setContent(content);
    }
  });
});

server.listen(80, "localhost", () => {
  console.log(`Server is running`);
});
