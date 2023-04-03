# Assignment: CIS*2750 W23 Assignment 2
# Due Date: February 28 2023 EXTENSION OF 72 HOURS
# Name: Or Brener
# Student #: 1140102

import MolDisplay
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import io

class MyHandler( BaseHTTPRequestHandler ):

    def do_GET( self ):
        if self.path == "/":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len(web_form) )
            self.end_headers()

            self.wfile.write( bytes( web_form, "utf-8" ) )

        else:
            self.send_response( 404 ) # Error
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )
        
    def do_POST( self ):
        if self.path == "/molecule":
            self.send_response( 200 ); # OK

            # get the sdf file from the form (then convert to text)
            bytesSDFFile = io.BytesIO(self.rfile.read(int(self.headers['Content-Length'])))
            textSDFFile = io.TextIOWrapper(bytesSDFFile)

            # skip the first 4 non-necessary lines
            for i in range(4):
                textSDFFile.readline()

            # parse and sort the molecule using the sdf 
            molecule = MolDisplay.Molecule()
            molecule.parse(textSDFFile)
            molecule.sort()
            # generate the svg of the molecule
            svg = molecule.svg()

            self.send_header( "Content-type", "image/svg+xml" )
            self.send_header( "Content-length", len(svg) )
            self.end_headers()

            self.wfile.write( bytes( svg, "utf-8" ) )

        else:
            self.send_response( 404 ) # Error
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )

web_form = """
<html>
    <head>
        <title> File Upload </title>
    </head>
    <body>
        <h1> File Upload </h1>
        <form action="molecule" enctype="multipart/form-data" method="post">
        <p>
            <input type="file" id="sdf_file" name="filename"/>
        </p>
        <p>
            <input type="submit" value="Upload"/>
        </p>
        </form>
    </body>
</html>
"""

# run the server
httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
httpd.serve_forever()
