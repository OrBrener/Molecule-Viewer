# Assignment: CIS*2750 W23 Assignment 2
# Due Date: February 28 2023 EXTENSION OF 72 HOURS
# Name: Or Brener
# Student #: 1140102

import MolDisplay
from molsql import Database
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import urllib
import json
import cgi

# public_files = [ '/index.html', '/style.css', '/script.js' ]

db = Database(reset=True)
db.create_tables()

class MyHandler( BaseHTTPRequestHandler ):

    def do_GET( self ):

        if self.path == '/' or self.path.endswith( '.html' ):
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )

            if (self.path == '/'):
                fp = open( "index.html" )
            else:
                fp = open( self.path[1:] )
            page = fp.read()
            fp.close()

            # create and send headers
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) )

        elif self.path == "/styles.css":
            self.send_response( 200 ); # OK

            self.send_header( "Content-type", "text/css" )

            fp = open( "styles.css" )
            page = fp.read()
            fp.close()

            # create and send headers
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) )

        elif self.path == "/script.js":
            self.send_response( 200 ); # OK

            self.send_header( "Content-type", "text/javascript" )

            fp = open( "script.js" )
            page = fp.read()
            fp.close()

            # create and send headers
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) )

        elif self.path == "/Or_Brener.jpg":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "image/jpg" )

            fp = open( "Or_Brener.jpg",'rb' )
            page = fp.read()
            fp.close()

            # create and send headers
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            # send the contents
            self.wfile.write( page )
        
        else:
            self.send_response( 404 ) # Error
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )
        
    def do_POST( self ):

        if self.path == "/uploadSDF":

            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {"REQUEST_METHOD":"POST"}
            )

            fileItem = form["file"]
            molName = form.getvalue("name")

            # read file in
            fileContent = fileItem.file.read()

            # convert to text
            bytesIO = io.BytesIO(fileContent)
            fileData = io.TextIOWrapper(bytesIO)

            db.add_molecule(molName, fileData)

            # print("\n\nMolecules")
            # print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() )

             
            self.send_response( 200 ); # OK
            self.end_headers()


        else:
            self.send_response( 404 ) # Error
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )


# run the server

db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 )
db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 )
db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 )
db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 )

httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
httpd.serve_forever()
