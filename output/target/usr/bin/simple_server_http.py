import time
import BaseHTTPServer
import datetime
import platform
import re
import os


HOST_NAME = '192.168.1.10' # !!! 192.168.1.10
PORT_NUMBER = 8000


class InfoCPU():
    def getDate(self):
        return datetime.datetime.now().strftime('%d/%m/%Y %H:%M')


    def getUpTime(self):
        with open("/proc/uptime", "r") as f:
            uptime = f.read().split(" ")[0].strip()
        
        return float(uptime)


    def getInfoCPU(self):
        informations = ""
        with open("/proc/cpuinfo", "r")  as f:
            info = f.readlines()

        cpuinfo = [x.strip().split(":")[1] for x in info if "model name"  in x]
        for index, item in enumerate(cpuinfo):
            informations += "    "+ item
        
        return informations


    def getCPUCapacity(self):
        with open("/proc/loadavg", "r") as f:
            load = f.read().strip()
        
        return load


    def getRAMTotal(self):
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()

        total = filter(str.isdigit, lines[0])
        return int(total)/1000


    def getRAMUsed(self):
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()

        total = filter(str.isdigit, lines[0])
        free = filter(str.isdigit, lines[1])
        return (int(total) - int(free))/1000

    
    def getVersionSystem(self):
        system = platform.system()
        dist = platform.dist()

        return (system + " ") + (" ").join(x for x in dist)


    def getProcessList(self):
        processList = list()
        
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        for pid in pids:
            try:
                if(os.path.exists(os.path.join('/proc', pid, 'cmdline'))):
                    # line = [processName, --option1, --option2, ]
                    line = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read().split('\0')
                    if(len(line) > 0 and len(line[0]) > 0):
                        processList.append([pid , line[0]])
            except IOError:
                continue
        
        return processList



class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        
        infos = InfoCPU()

        s.wfile.write("<html>")
        s.wfile.write("<head><title>Trabalho I</title></head>")
        s.wfile.write("<body>")
        s.wfile.write("<h1>Trabalho I da disciplina de Laboratorio de Sistemas operacionais</h1>")
        s.wfile.write("<h3>Gabriel Vaz e Marcio Goes</h3>")
        s.wfile.write("<p>Data e hora: %s</p>" % infos.getDate())
        s.wfile.write("<p>Update em segundos: %s</p>" % infos.getUpTime())
        s.wfile.write("<p>Modelo do processador e velocidade: %s</p>" % infos.getInfoCPU())
        s.wfile.write("<p>Capacidade ocupada do processador: %s</p>" % infos.getCPUCapacity())
        s.wfile.write("<p>Quantidade de memoria RAM total/usada (MB): %s / %s</p>" % (infos.getRAMTotal(), infos.getRAMUsed()))
        s.wfile.write("<p>Versao do sistema: %s</p>" % infos.getVersionSystem())
        s.wfile.write("<p>Lista de processos em execucao (pid e nome):</p>")
        
        # css table
        s.wfile.write("<style>")
        s.wfile.write("body{font-family: Verdana,sans-serif;font-size: 15px;line-height: 1.5;}")
        s.wfile.write("table, td, th{border: 1px solid #ddd;text-align: left;border-collapse: collapse;}")
        s.wfile.write("td, th{padding: 15px;}")
        s.wfile.write("</style>")
        # print table of process
        processList = infos.getProcessList()
        s.wfile.write("<table width='100%'>")
        s.wfile.write("<thead><tr><th width='30%'>Pid</th><th>Nome do processo</th></tr></thead>")
        s.wfile.write("<tbody>")
        for i in processList:
            s.wfile.write("<tr><td>%s</td><td>%s</td></tr>" % (i[0], i[1]))
        s.wfile.write("<tbody>")
        s.wfile.write("</table>")
        
        s.wfile.write("</body>")
        s.wfile.write("</html)")



if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

