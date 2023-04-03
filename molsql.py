# Assignment: CIS*2750 W23 Assignment 3
# Due Date: March 21 2023
# Name: Or Brener
# Student #: 1140102

from MolDisplay import Atom, Bond, Molecule #import the specific classes so that I don't need to do ex: MolDisplay.Atom() 
import MolDisplay
import sqlite3
import os

class Database():

    def __init__( self, reset = False ):
        # if reset it true: delete the existing database and start a new one
        if reset:
            if os.path.exists( 'molecules.db' ):
                os.remove( 'molecules.db' )
        # conn = database connection
        self.conn = sqlite3.connect( 'molecules.db' )

    def create_tables( self ):
        
        # Elements Table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Elements
                            (   ELEMENT_NO      INTEGER NOT NULL,
                                ELEMENT_CODE    VARCHAR(3) NOT NULL,
                                ELEMENT_NAME    VARCHAR(32) NOT NULL,
                                COLOUR1         CHAR(6) NOT NULL,
                                COLOUR2         CHAR(6) NOT NULL,
                                COLOUR3         CHAR(6) NOT NULL,
                                RADIUS          DECIMAL(3) NOT NULL,
                                PRIMARY KEY (ElEMENT_CODE) );""" )
        
        # Atoms Table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Atoms
                            (   ATOM_ID         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                ELEMENT_CODE    VARCHAR(3) NOT NULL,
                                X               DECIMAL(7,4) NOT NULL,
                                Y               DECIMAL(7,4) NOT NULL,
                                Z               DECIMAL(7,4) NOT NULL,
                                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements );""" )
        
        # Bonds Table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Bonds
                            (   BOND_ID         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                A1              INTEGER NOT NULL,
                                A2              INTEGER NOT NULL,
                                EPAIRS          INTEGER NOT NULL);""" )

        # Molecules Table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Molecules
                            (   MOLECULE_ID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                NAME            TEXT UNIQUE NOT NULL);""" )

        # MoleculesAtom Table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeAtom
                            (   MOLECULE_ID     INTEGER NOT NULL,
                                ATOM_ID         INTEGER NOT NULL,
                                PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                                FOREIGN KEY (ATOM_ID) REFERENCES Atoms );""" )
        
        # MoleculesBond Table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeBond
                            (   MOLECULE_ID     INTEGER NOT NULL,
                                BOND_ID         INTEGER NOT NULL,
                                PRIMARY KEY (MOLECULE_ID, BOND_ID),
                                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                                FOREIGN KEY (BOND_ID) REFERENCES Bonds );""" )
        
        # Save all the changes to the database
        self.conn.commit()

    def __setitem__( self, table, values ):
        
        # set values in the table (using indexing)
        self.conn.execute( """INSERT INTO %s VALUES %s;""" % (table, values) )

        # Save all the changes to the database
        self.conn.commit()

    def add_atom( self, molname, atom ):
        
        # insert the atom data into the database
        self.conn.execute( """INSERT INTO Atoms ( ELEMENT_CODE, X, Y, Z ) VALUES ('%s', %s, %s, %s);""" % (atom.element, atom.x, atom.y, atom.z) )
        
        # extract the atomId from Atoms table
        atomId = self.conn.execute("""SELECT MAX (ATOM_ID) FROM Atoms;""" ).fetchall()[0][0]
        # extract the moleculeId of the molecule
        moleculeId = self.conn.execute("""SELECT MOLECULE_ID FROM Molecules WHERE NAME = '%s';""" % (molname) ).fetchall()[0][0]
        
        # insert the molecule and atom Id into the MoleculeAtom table
        self.conn.execute("""INSERT INTO MoleculeAtom ( MOLECULE_ID, ATOM_ID ) VALUES (%s, %s);""" % (moleculeId, atomId) )
        
        # Save all the changes to the database
        self.conn.commit()


    def add_bond( self, molname, bond ):
        
        # insert the bond data into the database
        self.conn.execute( """INSERT INTO Bonds ( A1, A2, EPAIRS ) VALUES (%s, %s, %s);""" % (bond.a1, bond.a2, bond.epairs) )
        
        # extract the bondId from Bonds table
        bondId = self.conn.execute("""SELECT BOND_ID, MAX (BOND_ID) FROM Bonds;""" ).fetchall()[0][0]
        # extract the moleculeId of the molecule
        moleculeId = self.conn.execute("""SELECT MOLECULE_ID FROM Molecules WHERE NAME = '%s';""" % (molname) ).fetchall()[0][0]
        
        # insert the molecule and bond Id into the MoleculeBond table
        self.conn.execute( """INSERT INTO MoleculeBond ( MOLECULE_ID, BOND_ID ) VALUES (%s, %s);""" % (moleculeId, bondId) )
        
        # Save all the changes to the database
        self.conn.commit()


    def add_molecule( self, name, fp ):
        # add a molecule to the database

        # create a molecule
        mol = Molecule()
        # parse it with the given file
        mol.parse(fp)

        # insert the molecule into the database
        self.conn.execute( """INSERT INTO Molecules ( NAME ) VALUES ('%s');""" % (name) )
        
        # for all atoms in the molecule
        for i in range(mol.atom_no):
            # add the atoms into the molecule
            self.add_atom(name, mol.get_atom(i))

        # for all the bonds in the molecule
        for i in range(mol.bond_no):
            # add the bonds into the molecule
            self.add_bond(name, mol.get_bond(i))

        # Save all the changes to the database
        self.conn.commit()


    def load_mol( self, name ):
        # get a molecule from the database
        # retrieves all atoms and bonds of the molecule = name, and appends them to a Molecule() and return it

        # create a molecule
        mol = Molecule()

        # Atoms

        # get the Atoms element_code, X, Y, Z from the molecule = name
        atomData = self.conn.execute( """SELECT Atoms.ELEMENT_CODE, X, Y, Z FROM 
                                        Atoms JOIN MoleculeAtom JOIN Molecules WHERE
                                        Molecules.name = ('%s') AND 
                                        Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID AND
                                        Atoms.ATOM_ID = MoleculeAtom.ATOM_ID 
                                        ORDER BY Atoms.ATOM_ID;""" % (name) ).fetchall()
        
        # for all atoms of that molecule
        for i in range(len(atomData)):
            # append the atoms (with their data)
            mol.append_atom(atomData[i][0],atomData[i][1],atomData[i][2],atomData[i][3])

        # Bonds

        # get the Bonds A1, A2, EPAIRS from the molecule = name
        bondData = self.conn.execute( """SELECT A1, A2, EPAIRS FROM 
                                        Bonds JOIN MoleculeBond JOIN Molecules WHERE
                                        Molecules.name = ('%s') AND 
                                        Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID AND
                                        Bonds.BOND_ID = MoleculeBond.BOND_ID 
                                        ORDER BY Bonds.BOND_ID;""" % (name) ).fetchall()
        # for all bonds of that molecule
        for i in range(len(bondData)):
            # append the bonds (with their data)
            mol.append_bond(bondData[i][0],bondData[i][1],bondData[i][2])
        
        # Save all the changes to the database
        self.conn.commit()

        # returned the molecule (with the database data (bonds and atoms))
        return mol

    def radius( self ):

        # return a dictionary for the radius size
        data = self.conn.execute( """SELECT ELEMENT_CODE, RADIUS FROM Elements;""" ).fetchall()
        return dict(data)

    def element_name( self ):

        # return a dictionary for the element name
        data = self.conn.execute( """SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements;""" ).fetchall()
        return dict(data)
    
    def radial_gradients( self ):
        # add the radial_gradients to the header file

        # get all the element name and colors from the database 
        data = self.conn.execute( """SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements;""" ).fetchall()
        
        # start the return sting
        radialGradientSVG = "\n"

        # for each element in the database:
        for i in range (len(data)):
            # add a radialGradient svg string (with it's data)
            radialGradientSVG += """<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
            <stop offset="0%%" stop-color="#%s"/>
            <stop offset="50%%" stop-color="#%s"/>
            <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>\n """ % (data[i][0],data[i][1],data[i][2],data[i][3])

        # return the concatenated string of radialGradients for all elements
        return radialGradientSVG
