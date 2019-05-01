import http.server
import http.client
import json
import socketserver

PORT=8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("search.html") as search:
                archivo = search.read()
            self.wfile.write(bytes(archivo, "utf8"))


        elif "searchDrug" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            buscador = self.path.split("=")
            try:
                if buscador[2] != "":
                    medicamento = buscador[1] + "=" + buscador[2]
                else:
                    medicamento = buscador[1] + "=" + "10"
            except IndexError:
                medicamento = buscador[1] + "&limit=10"

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=active_ingredient:%s" % medicamento, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)["results"]
            drug = ["<h1>Lista de farmacos con el ingrediente activo solicitado</h3><br>"]
            for n in repos:
                try:
                    drug.append("<li>" + n["openfda"]["generic_name"][0] + "</li>")
                except KeyError:
                    drug.append("<li>Desconocido</li>")

            string = "".join(drug)
            self.wfile.write(bytes(string, "utf8"))

        elif "searchCompany" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            buscador = self.path.split("=")
            try:
                if buscador[2] != "":
                    medicamento = buscador[1] + "=" + buscador[2]
                else:
                    medicamento = buscador[1] + "=" + "10"
            except IndexError:
                medicamento = buscador[1] + "&limit=10"

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=openfda.manufacturer_name:%s" % medicamento, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)["results"]
            drug = ["<h1>Lista de farmacos de la empresa solicitada</h1><br>"]
            for n in repos:
                try:
                    drug.append("<li>" + n["openfda"]["generic_name"][0] + "</li>")
                except KeyError:
                    drug.append("<li>Desconocido</li>")

            string = "".join(drug)
            self.wfile.write(bytes(string, "utf8"))

        elif "listDrugs" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            buscador = self.path.split("=")
            limite = buscador[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % limite, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)["results"]
            drug =["<h1>Lista de farmacos solicitada</h1><br>"]
            for n in repos:
                try:
                    drug.append("<li>" + n["openfda"]["generic_name"][0] + "</li>")
                except KeyError:
                    drug.append("<li>Desconocido</li>")

            string = "".join(drug)
            self.wfile.write(bytes(string, "utf8"))

        elif "listCompanies" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            buscador = self.path.split("=")
            limite = buscador[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" %limite, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)["results"]
            drug = ["<h1>Lista de empresas solicitadas</h1><br>"]
            for n in repos:
                try:
                    drug.append("<li>"+ n["openfda"]["manufacturer_name"][0]+ "</li>")
                except KeyError:
                    drug.append("<li>Desconocido</li>")

            string = "".join(drug)
            self.wfile.write(bytes(string, "utf8"))


        elif "listWarnings" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            buscador = self.path.split("=")
            medicamento = buscador[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % medicamento, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)["results"]
            drug = ["<h1>Lista de advertencias</h1><br>"]
            for n in repos:
                try:
                    drug.append("<li>"+ n["warnings"][0]+ "</li>")
                except KeyError:
                    drug.append("<li>Desconocido</li>")

            string = "".join(drug)
            self.wfile.write(bytes(string, "utf8"))

        elif "secret" in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', "Basic realm = DENIED")
            self.end_headers()

        elif "redirect"  in self.path:
            self.send_response(301)
            self.send_header("Location","http://localhost:8000")
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            with open("error.html", "r") as s:
                error = s.read()
            self.wfile.write(bytes(error, "utf8"))



        return


# Para reservar la ip y el puerto donde el servidor va a escuchar. Permite que se renueve el puerto ya usado. Esta instrucción sirve para cambiar el puerto cuando está pillado y poderlo reutilizarlo.
socketserver.TCPServer.allow_reuse_address= True

# Handler: manejador, es una instancia de la clase, sabe responder ante un do get, manejador de http.
# El manejador no está siempre ejecutando. Cada vez que llegue algo al puerto, este se encarga de gestionar la respuesta.
Handler = testHTTPRequestHandler

# Asocia una ip y un puerto al manejador de peticiones. Cuando llegue una petición a la ip y al puerto el programa le dice a nuestro manejador que atienda.
httpd = socketserver.TCPServer(('', PORT), Handler)
print("Corriendo en el puerto: ", PORT)
# Forever: Es la línea para que empiece a funcionar el programa.
httpd.serve_forever()
