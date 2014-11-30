#!/usr/bin/env python
import web
import xml.etree.ElementTree as ET

tree = ET.parse('DHT22_data.xml')
root = tree.getroot()

urls = (
    '/sensors', 'list_sensors',
    '/sensors/(.*)', 'get_sensor'
)

app = web.application(urls, globals())

class list_sensors:        
    def GET(self):
        output = 'sensors:[';
        for child in root:
                print 'child', child.tag, child.attrib
                output += str(child.attrib) + ','
        output += ']';
        return output

class get_sensor:
    def GET(self, sensor):
        for child in root:
                if child.attrib['id'] == sensor:
                    return str(child.attrib)

if __name__ == "__main__":
    app.run()
