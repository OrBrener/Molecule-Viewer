# Assignment: CIS*2750 W23 Assignment 3
# Due Date: March 21 2023
# Name: Or Brener
# Student #: 1140102

import molecule

# constants:

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
footer = """</svg>"""
offsetx = 500
offsety = 500
radius = {}
element_name = {}

class Atom():

    def __init__( self, c_atom ):
        self.atom = c_atom
        self.z = c_atom.z

    def __str__( self ):
        # for testing purposes
        return '''ATOM '%s': x=%f y=%f, z=%f''' % (self.atom.element, self.atom.x, self.atom.y, self.atom.z)

    def svg( self ):
        # x and y values need to be scaled and summed with the offset
        x = (self.atom.x * 100.0) + offsetx
        y = (self.atom.y * 100.0) + offsety

        # get radius and color from the tables
        # added in default values 
        r = radius.get(self.atom.element, 30)
        color = element_name.get(self.atom.element, "default")

        # return svg string
        return ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (x, y, r, color)


class Bond():

    def __init__( self, c_bond ):
        self.bond = c_bond
        self.z = c_bond.z

    def __str__( self ):
        # for testing purposes
        return '''BOND: %.2f,%.2f %.2f,%.2f z=%.2f len=%.2f dx=%.2f dy=%.2f''' % (self.bond.x1, self.bond.y1, self.bond.x2, self.bond.y2, self.bond.z, self.bond.len, self.bond.dx, self.bond.dy)

    def svg( self ):

        # x and y values of the four corners of the rectangle
        topRightX = ((self.bond.x1 * 100.0) + offsetx) - (self.bond.dy * 10.0)
        topRightY = ((self.bond.y1 * 100.0) + offsety) - (self.bond.dx * 10.0) 
        topLeftX = ((self.bond.x2 * 100.0) + offsetx) - (self.bond.dy * 10.0)
        topLeftY = ((self.bond.y2 * 100.0) + offsety) - (self.bond.dx * 10.0)
        bottomRightX = ((self.bond.x1 * 100.0) + offsetx) + (self.bond.dy * 10.0)
        bottomRightY = ((self.bond.y1 * 100.0) + offsety) + (self.bond.dx * 10.0)
        bottomLeftX = ((self.bond.x2 * 100.0) + offsetx) + (self.bond.dy * 10.0)
        bottomLeftY = ((self.bond.y2 * 100.0) + offsety) + (self.bond.dx * 10.0)

        #return svg string
        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (topRightX, bottomRightY, bottomRightX, topRightY, bottomLeftX, topLeftY, topLeftX, bottomLeftY)


class Molecule( molecule.molecule ):

    def __str__( self ):
        # for testing purposes
        return '''NEED TO FINISH %s''' % ("LATER")

    def svg( self ):
        # svg output starts with the header (constant)
        output = header

        # sort the atoms and bonds, and append them to the svg output:
        
        i = j = 0
        # Go through the atoms and bonds
        while i < self.atom_no and j < self.bond_no:
            currentAtom = Atom(self.get_atom(i))
            currentBond = Bond(self.get_bond(j))

            if currentAtom.z <= currentBond.z:
                output += currentAtom.svg()
                i += 1
            else:
                output += currentBond.svg()
                j += 1
  
        # Checking if any element were left
        while i < self.atom_no:
            currentAtom = Atom(self.get_atom(i))
            output += currentAtom.svg()
            i += 1
        while j < self.bond_no:
            currentBond = Bond(self.get_bond(j))
            output += currentBond.svg()
            j += 1

        # svg output ends with the footer (constant)
        output += footer
        return output
    
    def parse( self, file ):
        numAtoms = 0
        numBonds = 0

        # get the number of atoms and bonds from the 4th line (constant)
        for i in range(4):        
            line = file.readline()

        #extract the number of atoms and bonds
        data = []
        numbers = line.split(" ")
        for i in range(len(numbers)):
            if (numbers[i] != ''):
                    data.append(numbers[i])
        numAtoms = int(data[0])
        numBonds = int(data[1])

        # append all the atoms
        for i in range(numAtoms):
            data = []        
            line = file.readline()
            numbers = line.split(" ")
            for i in range(len(numbers)):
                if (numbers[i] != ''):
                    data.append(numbers[i])
            self.append_atom(data[3], float(data[0]), float(data[1]), float(data[2]))

        # append all the bonds
        for i in range(numBonds): 
            data = []       
            line = file.readline()
            numbers = line.split(" ")
            for i in range(len(numbers)):
                if (numbers[i] != ''):
                    data.append(numbers[i])
            # A3 FIX: -1 for the atom indices so that we can append from database
            self.append_bond(int(data[0])-1, int(data[1])-1, int(data[2]))
