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

db = Database(reset=True)
db.create_tables()
db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 )
db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 )
db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 )
db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 )


MolDisplay.radius = db.radius()
MolDisplay.element_name = db.element_name()
MolDisplay.header += db.radial_gradients()


class MyHandler( BaseHTTPRequestHandler ):

    def do_GET( self ):

        if (self.path == "/molecule.html"):
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            
            html_string = ""
            with open('emptyMol.html', 'r') as f:
                html_string = f.read()

            name = db.conn.execute("""SELECT Name FROM Molecules;""" ).fetchall()
            for numMol in range(len(name)):
                numAtoms = db.load_mol(name[numMol][0]).atom_no
                numBonds = db.load_mol(name[numMol][0]).bond_no

                # mol = MolDisplay.Molecule()
                mol = db.load_mol(name[numMol][0])
                svg = mol.svg()
                # Find the line number of the </tbody> tag
                tbody_line_number = None
                for i, line in enumerate(html_string.splitlines()):
                    if '<!-- end of molecules -->' in line:
                        tbody_line_number = i
                        break

                # Append a new row right before the </tbody> tag
                if tbody_line_number is not None:
                    new_row = \
            '''          <div class="card">
                <div class="card-header" id="heading%s">
                <h2 class="mb-0">
                    <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse%s" aria-expanded="false" aria-controls="collapse%s">
                    Molecule name %s<br> # bonds = %s <br> # atoms = %s
                    </button>
                </h2>
                </div>
            
                <div id="collapse%s" class="collapse" aria-labelledby="heading%s" data-parent="#accordionExample">
                <div class="card-body">
                    %s
                </div>
                </div>
            </div>'''% (numMol,numMol,numMol,name[numMol][0], numBonds, numAtoms,numMol,numMol,svg)
                    lines = html_string.splitlines()
                    lines.insert(tbody_line_number, new_row)
                    html_string = '\n'.join(lines)
            with open('molecule.html', 'w') as f:
                f.write(html_string)
            fp = open("molecule.html")
            page = fp.read()
            fp.close()

            # create and send headers
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) )
        
        elif (self.path == "/removeElements.html"):
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            
            html_string = ""
            with open('emptyElements.html', 'r') as fpR:
                html_string = fpR.read()

            elements = db.conn.execute("""SELECT * FROM Elements;""" ).fetchall()
            isElements = False
            codes=[]
            for numElement in range(len(elements)):
                isElements = True
                num = elements[numElement][0]
                code = elements[numElement][1]
                name = elements[numElement][2]
                col1 = elements[numElement][3]
                col2 = elements[numElement][4]
                col3 = elements[numElement][5]
                radius = elements[numElement][6]
                codes.append(code)

    
                # Find the line number of the </tbody> tag
                tbody_line_number = None
                for i, line in enumerate(html_string.splitlines()):
                    if '<!-- end of elements -->' in line:
                        tbody_line_number = i
                        break

                # Append a new row right before the </tbody> tag
                if tbody_line_number is not None:
                    new_row = \
                '''          <tr>
                            <th scope="row">%s</th>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                        </tr>'''% (num,code,name,col1,col2,col3,radius)
                    
                    lines = html_string.splitlines()
                    lines.insert(tbody_line_number, new_row)
                    html_string = '\n'.join(lines)
            
            if isElements:
                new_row = \
                    ''' <br>
                    <form>
                    <div class="form-row align-items-center">
                        <div class="col-auto my-1">
                        <label class="mr-sm-2 sr-only" for="inlineFormCustomSelect">Preference</label>
                        <select class="custom-select mr-sm-2" id="deleteCodeInput">
                            <option selected>Choose Element...</option>'''
                for numCode in range(len(codes)):
                    print(numCode)
                    new_row += '''<option value="%s"">%s</option>''' % (numCode, codes[numCode])
                
                new_row += \
                        '''</select>
                        </div>
                        <div class="col-auto my-1">
                        <button type="submit" class="btn btn-primary" id="deleteSubmit">Delete</button>
                        </div>
                    </div>
                    </form> '''
                lines = html_string.splitlines()
                lines.insert(55, new_row)
                html_string = '\n'.join(lines)

            with open('removeElements.html', 'w') as fpW:
                fpW.write(html_string)
            fp = open("removeElements.html")
            page = fp.read()
            fp.close()

            # create and send headers
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) )
        
        elif self.path == '/' or self.path.endswith( '.html' ):
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
             
            self.send_response( 200 ); # OK
            self.end_headers()

        elif self.path == "/elementSubmit":

            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {"REQUEST_METHOD":"POST"}
            )

            num = form.getvalue("num")
            code = form.getvalue("code")
            name = form.getvalue("name")
            col1 = form.getvalue("col1")
            col2 = form.getvalue("col2")
            col3 = form.getvalue("col3")
            radius = form.getvalue("radius")

            db['Elements'] = ( num, code, name, col1, col2, col3, radius )

            # print("Elements")
            # print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() )

             
            self.send_response( 200 ); # OK
            self.end_headers()

        elif self.path == "/deleteSubmit":

            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {"REQUEST_METHOD":"POST"}
            )

            elementCode = form.getvalue("elementCode")
            print(elementCode)

            db.conn.execute( """DELETE FROM Elements WHERE ELEMENT_CODE = '%s';""" % (elementCode) )

            print("Elements")
            print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() )

             
            self.send_response( 200 ); # OK
            self.end_headers()

        else:
            self.send_response( 404 ) # Error
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )


# run the server

httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
httpd.serve_forever()
