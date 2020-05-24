from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from urllib.parse import urlparse
import pycurl as c
from io import BytesIO
import xml.etree.ElementTree as xml
from time import sleep

IP = '192.168.100.2'
# Default credentals for built in digest auth
#USER = 'admin'
#PASS = 'admin'
SWITCHER_URI = '/v1/dictionary?key=switcher'
SHORTCUT_URI = '/v1/shortcut?name='

# Note:
# load_from_emem 0-8
# load_from_compbin 1-9

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def get_status(self, bus):
        """Get main bus status. Bus can be 'main_source' or 'preview_source'."""
        url = 'http://'+IP+SWITCHER_URI
        buffer = BytesIO()
        curl = c.Curl()
#        curl.setopt(c.HTTPAUTH, c.HTTPAUTH_DIGEST)
#        curl.setopt(c.USERPWD, USER+":"+PASS)
        curl.setopt(c.TIMEOUT, 5)
        curl.setopt(c.URL, url)
        curl.setopt(c.WRITEDATA, buffer)
        curl.perform()
        curl.close()

        body = buffer.getvalue()
        root = xml.fromstring(body)
        bus_source = root.attrib.get(bus).lower()

#        curr_pgm = root.attrib.get('main_source')
#        curr_pvw = root.attrib.get('preview_source')

        return bus_source

    def set_comp_on_bus(self, bus, compNumber):
        url = 'http://'+IP+SHORTCUT_URI+bus+"_load_compbin&value="+compNumber
        print("set_comp_on_bus: "+url)
        buffer = BytesIO()
        curl = c.Curl()
#        curl.setopt(c.HTTPAUTH, c.HTTPAUTH_DIGEST)
#        curl.setopt(c.USERPWD, USER+":"+PASS)
        curl.setopt(c.TIMEOUT, 5)
        curl.setopt(c.URL, url)
        curl.setopt(c.WRITEDATA, buffer)
        curl.perform()
        curl.close()
        return

    def set_preset_on_bus(self, bus, presetNumber):
        presetBase0 = str(int(presetNumber)-1)
        url = 'http://'+IP+SHORTCUT_URI+bus+"_load_from_emem&value="+presetBase0
        print("set_preset_on_bus: "+url)
        buffer = BytesIO()
        curl = c.Curl()
#        curl.setopt(c.HTTPAUTH, c.HTTPAUTH_DIGEST)
#        curl.setopt(c.USERPWD, USER+":"+PASS)
        curl.setopt(c.TIMEOUT, 5)
        curl.setopt(c.URL, url)
        curl.setopt(c.WRITEDATA, buffer)
        curl.perform()
        curl.close()
        return

    def set_source_on_row(self, row, sourceName):
        url = 'http://' + IP + SHORTCUT_URI + "main_" + row + "_row_named_input&value=" + sourceName
        print("set_source_on_row: " + url)
        buffer = BytesIO()
        curl = c.Curl()
        #        curl.setopt(c.HTTPAUTH, c.HTTPAUTH_DIGEST)
        #        curl.setopt(c.USERPWD, USER+":"+PASS)
        curl.setopt(c.TIMEOUT, 5)
        curl.setopt(c.URL, url)
        curl.setopt(c.WRITEDATA, buffer)
        curl.perform()
        curl.close()
        return

    def set_comp_on_bus_on_preview(self, compNumber):
        print("in setting comp on preview")
        bus_source = self.get_status("preview_source")
        self.set_comp_on_bus(bus_source, compNumber)
        return

    def set_comp_on_bus_on_program(self, compNumber):
        print("in setting comp on program")
        bus_source = self.get_status("main_source")
        self.set_comp_on_bus(bus_source, compNumber)
        return

    def set_preset_on_bus_on_preview(self, presetNumber):
        bus_source = self.get_status("preview_source")
        print("in setting preset on preview:" + bus_source + " " + presetNumber)
        self.set_preset_on_bus(bus_source, presetNumber)
        return

    def set_preset_on_bus_on_program(self, presetNumber):
        bus_source = self.get_status("main_source")
        print("in setting preset on program:" +bus_source+" "+presetNumber)
        self.set_preset_on_bus(bus_source, presetNumber)
        return

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        print(query_components)
        comp = ""
        bus = ""
        preset = ""
        row = ""
        sourcename = ""

        if 'bus' in query_components:
            bus = query_components["bus"][0]
            print("bus in query: " + bus)

            if 'comp' in query_components:
                comp = query_components["comp"][0]
                print("comp in query: "+comp)
                if bus == "program":
                    print("setting comp on program")
                    self.set_comp_on_bus_on_program(comp)
                elif bus == "preview":
                    print("setting comp on preview")
                    self.set_comp_on_bus_on_preview(comp)

            if 'preset' in query_components:
                preset = query_components["preset"][0]
                print("preset in query: "+preset)
                if bus == "program":
                    print("setting preset on program")
                    self.set_preset_on_bus_on_program(preset)
                elif bus == "preview":
                    print("setting preset on preview")
                    self.set_preset_on_bus_on_preview(preset)

            if 'preset' in query_components and 'comp' in query_components:
                preset = query_components["preset"][0]
                comp = query_components["comp"][0]
                print("preset & comp in query: " + preset + " " + comp)
                if bus == "program":
                    self.set_preset_on_bus_on_program(preset)
                    sleep(0.1)
                    self.set_comp_on_bus_on_program(comp)
                elif bus == "preview":
                    self.set_preset_on_bus_on_preview(preset)
                    sleep(0.1)
                    self.set_comp_on_bus_on_preview(comp)

        if 'row' in query_components:
            row = query_components["row"][0]
            print("row in query: " + row)
            if 'sourcename' in query_components:
                print("setting input on row")
                self.set_source_on_row(row, sourcename)

        self.send_response(200)
        self.end_headers()

#        print("pgm: "+self.get_status("main_source"))
#        print("pvw: "+self.get_status("preview_source"))
#        html_response = f"Set comp={comp}, bus={bus}, preset={preset}"
#        xml_response = self.getSource("test")
#        self.wfile.write(bytes(html_response, "utf8"))
#        self.wfile.write(bytes(xml_response, "utf8"))

httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()
