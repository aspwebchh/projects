from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
import os
import re
import time

rootPath = "C:/Users/宏鸿/Desktop/log"


def getFullPath(path):
    return rootPath + path


def response404(self):
    self.send_response(404)
    self.send_header('Content-type', 'text/html')
    self.end_headers()


def response200(self, content):
    self.send_response(200)
    self.send_header('Content-type', 'text/html;charset=utf8')
    self.end_headers()
    self.wfile.write(content.encode())


def readFileContent(path):
    fp = open(path, mode="r", encoding="utf8")
    content = fp.read()
    fp.close()
    return content


def merge(path, dir):
    if re.search(r'/$', path):
        return path + dir
    else:
        return path + "/" + dir


def getLink(fullPath):
    return str(fullPath).replace(rootPath + "/", "")


def getTimeString( fullPath ) :
    fileLastModifyTime = os.path.getmtime(fullPath)
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(fileLastModifyTime))


def readDirContent(path):
    dirs = os.listdir(path)
    dirs.sort(key=lambda it: os.path.getmtime(merge(path, it)), reverse=1)
    content = ""
    for dir in dirs:
        fullPath = merge(path, dir)
        link = "<tr>"
        link += "<td><a href='" + getLink(fullPath) + "'>" + fullPath +  "<a></td>"
        link += "<td>"+getTimeString(fullPath) +"</td>"
        link += "</tr>"
        content += link
    return "<table>" + content + "</table>"


class ServerHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        fullPath = getFullPath(self.path)
        if not os.path.exists(fullPath):
            response404(self)
            return
        isFile = os.path.isfile(fullPath)
        if isFile:
            response200(self, readFileContent(fullPath))
        else:
            response200(self, readDirContent(fullPath))


httpd = ThreadingHTTPServer(('', 2020), ServerHandler)
httpd.serve_forever()
