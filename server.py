# Assignment: CIS*2750 W23 Assignment 4
# Due Date: April 5 2023 EXTENSION OF 48 HOURS
# Name: Or Brener
# Student #: 1140102

import MolDisplay
from molsql import Database
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import cgi

# initialize a connection to a database
db = Database(reset=True)
db.create_tables()

# for testing purposes
# db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 )
# db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 )
# db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 )
# db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 )


# default element
db['Elements'] = ( -1, '--', 'default', 'FFFFFF', 'FFFFFF', 'FFFFFF', 30 )

# create a connection of the radius and element_name to the database 
# so that it can be dynamically added to and subtracted from
MolDisplay.radius = db.radius()
MolDisplay.element_name = db.element_name()
MolDisplay.header += db.radial_gradients()


class MyHandler( BaseHTTPRequestHandler ):

    def do_GET( self ):
        
        # GET all the molecules in the database
        if (self.path == "/molecule.html"):
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            
            html_string = ""
            # start with a webpage where there are no molecules in the database
            with open('emptyMol.html', 'r') as fpR:
                html_string = fpR.read()

            # get all the molecules and their data from the database
            name = db.conn.execute("""SELECT Name FROM Molecules;""" ).fetchall()

            # for each molecule, extract the name, and number of atoms/bonds
            for numMol in range(len(name)):
                numAtoms = db.load_mol(name[numMol][0]).atom_no
                numBonds = db.load_mol(name[numMol][0]).bond_no

                # get the svg of the molecule
                mol = db.load_mol(name[numMol][0])
                svg = mol.svg()

                # Find the line number of the <!-- end of molecules --> comment
                lineNumber = None
                for i, line in enumerate(html_string.splitlines()):
                    if '<!-- end of molecules -->' in line:
                        lineNumber = i
                        break

                # Append a new molecule before the <!-- end of molecules --> comment
                if lineNumber is not None:
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
                    
                    # add it to the htmlString
                    lines = html_string.splitlines()
                    lines.insert(lineNumber, new_row)
                    html_string = '\n'.join(lines)

            # finished appending all the molecules, post molecule.html 
            with open('molecule.html', 'w') as fpW:
                fpW.write(html_string)
            fp = open("molecule.html")
            page = fp.read()
            fp.close()

            # create and send headers
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) )
        
        # GET all the elements in the database
        elif (self.path == "/removeElements.html"):
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            
            html_string = ""
            # start with a webpage where there are no elements in the database
            with open('emptyElements.html', 'r') as fpR:
                html_string = fpR.read()

            # get all the elements from the database
            elements = db.conn.execute("""SELECT * FROM Elements;""" ).fetchall()
            
            # are there elements in the database?
            isElements = False

            # store all the (unique) element codes
            codes=[]

            # for each element, extract all it's data
            for numElement in range(0,len(elements)):
                # if there are more than just the default element (cannot be deleted)
                if numElement > 0:
                    isElements = True
                num = elements[numElement][0]
                code = elements[numElement][1]
                name = elements[numElement][2]
                col1 = elements[numElement][3]
                col2 = elements[numElement][4]
                col3 = elements[numElement][5]
                radius = elements[numElement][6]

                # do not do anything for the constant default molecule
                if code == '--':
                    continue

                codes.append(code)

    
                # Find the line number of the <!-- end of elements --> comment
                lineNumber = None
                for i, line in enumerate(html_string.splitlines()):
                    if '<!-- end of elements -->' in line:
                        lineNumber = i
                        break

                # Append a new row right before the <!-- end of elements --> tag
                if lineNumber is not None:
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
                    
                    # add it to the htmlString
                    lines = html_string.splitlines()
                    lines.insert(lineNumber, new_row)
                    html_string = '\n'.join(lines)

            # only if there are elements in the table, show the choice form for deleting
            if isElements:
                # form header
                new_row = \
                    ''' <br>
                    <form>
                    <div class="form-row align-items-center">
                        <div class="col-auto my-1">
                        <label class="mr-sm-2 sr-only" for="inlineFormCustomSelect">Preference</label>
                        <select class="custom-select mr-sm-2" id="deleteCodeInput">
                            <option selected>Choose Element...</option>'''
                # for all the element codes, give an option to select them
                for numCode in range(len(codes)):
                    new_row += '''<option value="%s">%s</option>''' % (numCode, codes[numCode])
                # form footer
                new_row += \
                        '''</select>
                        </div>
                        <div class="col-auto my-1">
                        <button type="submit" class="btn btn-primary" id="deleteSubmit">Delete</button>
                        </div>
                    </div>
                    </form> '''
                
                # add it to the htmlString (before the table (constant line number in HTML))
                lines = html_string.splitlines()
                lines.insert(55, new_row)
                html_string = '\n'.join(lines)

            # update the radius and element dictionary based on the new set of elements
            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()

            # finished appending all the molecules, post molecule.html 
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
        
        # GET home page and all other .html pages
        elif self.path == '/' or self.path.endswith( '.html' ):
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )

            if (self.path == '/'):
                fp = open( "index.html" )
            else:
                # ignore the leading "/"
                fp = open( self.path[1:] )
            page = fp.read()
            fp.close()

            # create and send headers
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) )

        # GET all the other files needed for the webserver 

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

        # POST an SDF to the database (converted to a molecule)
        if self.path == "/uploadSDF":
            
            # create form metadata
            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {"REQUEST_METHOD":"POST"}
            )

            # get the file and molecule name (AJAX response)
            fileItem = form["file"]
            molName = form.getvalue("name")

            # read file in
            fileContent = fileItem.file.read()

            # convert to text
            bytesIO = io.BytesIO(fileContent)
            fileData = io.TextIOWrapper(bytesIO)

            # add the molecule to the database based on the SDF file
            db.add_molecule(molName, fileData)
             
            self.send_response( 200 ); # OK
            self.end_headers()

        # POST a element to the database
        elif self.path == "/elementSubmit":

            # create form metadata
            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {"REQUEST_METHOD":"POST"}
            )

            # get data from the form (AJAX response)
            num = form.getvalue("num")
            code = form.getvalue("code")
            name = form.getvalue("name")
            col1 = form.getvalue("col1")
            col2 = form.getvalue("col2")
            col3 = form.getvalue("col3")
            radius = form.getvalue("radius")

            # add the new element to the database
            db['Elements'] = ( num, code, name, col1, col2, col3, radius )

            # print("Elements")
            # print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() )

             
            self.send_response( 200 ); # OK
            self.end_headers()
        
        # DELETE an element from the database
        elif self.path == "/deleteSubmit":

            # create form metadata
            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {"REQUEST_METHOD":"POST"}
            )

            # get data from the form (AJAX response)
            elementCode = form.getvalue("elementCode")

            # delete the element from the database
            db.conn.execute( """DELETE FROM Elements WHERE ELEMENT_CODE = '%s';""" % (elementCode) )

            # print("Elements")
            # print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() )

             
            self.send_response( 200 ); # OK
            self.end_headers()

        else:
            self.send_response( 404 ) # Error
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )


# run the server
httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
httpd.serve_forever()
