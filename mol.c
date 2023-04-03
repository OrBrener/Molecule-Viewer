// Assignment: CIS*2750 W23 Assignment 3
// Due Date: March 21 2023
// Name: Or Brener
// Student #: 1140102

#include "mol.h"

// This function should copy the values pointed to by element, x, y, and z into the atom stored at atom. 
// You may assume that sufficient memory has been allocated at all pointer addresses.  
// Note that using pointers for the function “inputs”, x, y, and z, is done here to match the function arguments of atomget. 
 
void atomset( atom *atom, char element[3], double *x, double *y, double *z ) {
    
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
    // strcpy takes care of the null-terminating character
    strcpy(atom->element, element);
}

// This function should copy the values in the atom stored at atom to the locations pointed to by element, x, y, and z. 
// You may assume that sufficient memory has been allocated at all pointer addresses.  
// Note that using pointers for the function “input”, atom, is done here to match the function arguments of atomset.

void atomget( atom *atom, char element[3], double *x, double *y, double *z ) {
    
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
    // strcpy takes care of the null-terminating character
    strcpy(element, atom->element);
}

// This function should copy the values pointed to by a1, a2, atoms, and epairs into the corresponding structure attributes in bond. 
// In addition, you should call the compute_coords function (see below) on the bond.

void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ) {
    
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;
    compute_coords(bond);

}

// This function should compute the z, x1, y1, x2, y2, len, dx, and dy values of the bond
// and set them in the appropriate structure member variables.

void compute_coords( bond *bond ) {
    
    bond->x1 = bond->atoms[bond->a1].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;
    // average of the two z values
    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2;
    
    // distance of x and y
    double x =  bond->x2 - bond->x1;
    double y =  bond->y2 - bond->y1;

    // pythagorean theorem 
    bond->len = sqrt(pow(x,2) + pow(y,2));

    bond->dx = x / bond->len;
    bond->dy = y / bond->len;
    

}

// This function should copy the structure attributes in bond to their corresponding arguments: a1, a2, atoms, and epairs.
// You may assume that sufficient memory has been allocated at all pointer addresses.
// Note you are not copying atom structures, only the addresses of the atom structures. 

void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ) {

    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;

}


// This function should return the address of a malloced area of memory, large enough to hold a molecule. 
// The value of atom_max should be copied into the structure; 
// the value of atom_no in the structure should be set to zero; and,  
// the arrays atoms and atom_ptrs should be malloced to have enough memory to hold atom_max atoms and pointers (respectively).  
// The value of bond_max should be copied into the structure; 
// the value of bond_no in the structure should be set to zero; and, 
// the arrays bonds and bond_ptrs should be malloced to have enough memory to hold bond_max bonds and pointers (respectively). 

molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ) {
    
    // NOTE that if malloc fails at any point, I free any malloced space, and return NULL;

    molecule *newMolecule = malloc(sizeof(struct molecule));

    if (newMolecule == NULL) {
        return NULL;
    }

    // set atom values
    newMolecule->atom_max = atom_max;
    newMolecule->atom_no = 0;
    // malloc atom pointers 
    newMolecule->atoms = malloc(sizeof(struct atom) * atom_max);
    newMolecule->atom_ptrs = malloc(sizeof(struct atom*) * atom_max);

    // set bond values
    newMolecule->bond_max = bond_max;
    newMolecule->bond_no = 0;
    // malloc bond pointers
    newMolecule->bonds = malloc(sizeof(struct bond) * bond_max);
    newMolecule->bond_ptrs = malloc(sizeof(struct bond*) * bond_max);

    // if any of the atom or bond pointer mallocs fail, free the one that are successful (if any), and return NULL
    if (newMolecule->atoms == NULL || newMolecule->atom_ptrs == NULL || newMolecule->bonds == NULL || newMolecule->bond_ptrs == NULL) {
        if (newMolecule->atoms != NULL) {
            free(newMolecule->atoms);
        }
        if (newMolecule->atom_ptrs != NULL) {
            free(newMolecule->atom_ptrs);
        }
        if (newMolecule->bonds != NULL) {
            free(newMolecule->bonds);
        }
        if (newMolecule->bond_ptrs != NULL) {
            free(newMolecule->bond_ptrs);
        }
        return NULL;
    }

    // all mallocs are successful

    // assign atoms pointer address to atom_ptrs 
    for (int i = 0; i<atom_max; i++) {
        newMolecule->atom_ptrs[i] = &newMolecule->atoms[i];
    }
    
    // assign bonds pointer address to bond_ptrs 
    for (int i = 0; i<bond_max; i++) {
        newMolecule->bond_ptrs[i] = &newMolecule->bonds[i];
    }

    // return the malloced molecule
    return newMolecule;
}


// This function should return the address of a malloced area of memory, large enough to hold a molecule.
// Additionally, the values of atom_max, atom_no, bond_max, bond_no should be copied from src into the new structure. 
// The arrays atoms, atom_ptrs, bonds and bond_ptrs must be allocated to match the size of the ones in src. 
// Finally, you should use molappend_atom and molappend_bond (below) to add the atoms from the src to the new 
// molecule (note that this will also initialize the corresponding pointer arrays).  
// You should re-use (i.e. call) the molmalloc function in this function.

molecule *molcopy( molecule *src ) {

    if (src == NULL) {
        return NULL;
    }

    // atom_max and bond_max are set in molmalloc

    molecule* copyMolecule = molmalloc(src->atom_max, src->bond_max);

    // atom_no and bond_no are set in molappend functions

    for (int i = 0; i < src->atom_no; i++) {
        molappend_atom(copyMolecule, &src->atoms[i]); 
    }

    for (int i = 0; i < src->bond_no; i++) {
        molappend_bond(copyMolecule, &src->bonds[i]);
    }

    return copyMolecule;
}


// This function should free the memory associated with the molecule pointed to by ptr.
// This includes the arrays atoms, atom_ptrs, bonds, bond_ptrs.

void molfree( molecule *ptr ) {

    if (ptr == NULL) {
        return;
    }

    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);
}

// This function should copy the data pointed to by atom to the first “empty” atom 
// in atoms in the molecule pointed to by molecule, and set the first “empty” pointer in atom_ptrs to the same 
// atom in the atoms array incrementing the value of atom_no.  
// If atom_no equals atom_max, then atom_max must be incremented, and the capacity of the atoms, 
// and atom_ptrs arrays increased accordingly.  
// If atom_max was 0, it should be incremented to 1, otherwise it should be doubled.  
// Increasing the capacity of atoms should be done using realloc so that a larger amount of memory is 
// allocated and the existing data is copied to the new location.  
// IMPORTANT:  After mallocing or reallocing enough memory for atom_ptrs, 
// these pointers should be made to point to the corresponding atoms in the new atoms array 
// (not the old array which may have been freed).

void molappend_atom( molecule *molecule, atom *atom ) {
    
    if (molecule == NULL || atom == NULL) {
        return;
    }
 
    // the first empty atom is atom_no
    int index = molecule->atom_no;

    // if atom_no reached the max
    if (molecule->atom_no == molecule->atom_max) {
        // if atom_max is zero, increment once
        if (molecule->atom_max == 0) {
            molecule->atom_max++;
        }
        // otherwise multiply by 2
        else {
            molecule->atom_max *= 2;
        }

        // realloc for max number of atoms
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*) * molecule->atom_max);

        // if realloc fails
        if (molecule->atoms == NULL || molecule->atom_ptrs == NULL) {
            printf("REALLOC FOR ATOMS/ATOM_PTRS IN molappend_atom failed\nexiting\n");
            exit(1);
        }  

        // reassign atoms pointer (new) address to atom_ptrs 
        for (int i = 0; i<molecule->atom_max; i++) {
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    }
    //atom_no is not at max

    // append the atom to the array
    memcpy(&(molecule->atoms[index]), atom, sizeof(struct atom));
    // link the pointers
    molecule->atom_ptrs[index] = &molecule->atoms[index];
    // increment atom_no
    molecule->atom_no++;
}

// This function should operate like that molappend_atom function, except for bonds

void molappend_bond( molecule *molecule, bond *bond ) {

    if (molecule == NULL || bond == NULL) {
        return;
    }

    // the first empty bond is bond_no
    int index = molecule->bond_no;
    
    // if bond_no reached the max
    if (molecule->bond_no == molecule->bond_max) {
        // if bond_max is zero, increment once
        if (molecule->bond_max == 0){
            molecule->bond_max++;
        }
        else {
            // otherwise multiply by 2
            molecule->bond_max *= 2;
        }

        // realloc for max number of bonds
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*) * molecule->bond_max);

        // if realloc fails
        if (molecule->bonds == NULL || molecule->bond_ptrs == NULL) {
            printf("REALLOC FOR BONDS/BOND_PTRS IN molappend_bond failed\nexiting\n");
            exit(1);
        }

        // reassign bonds pointer (new) address to bond_ptrs 
        for (int i = 0; i<molecule->bond_max; i++) {
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
    }
    //bond_no is not at max

    // append the bond to the array
    memcpy(&(molecule->bonds[index]), bond, sizeof(struct bond));
    // link the pointers
    molecule->bond_ptrs[index] = &molecule->bonds[index];
    // increment atom_no
    molecule->bond_no++;

}

// This function should sort the atom_ptrs array in place in order of increasing z value.  
// I.e. atom_ptrs[0] should point to the atom that contains the lowest z value 
// and atom_ptrs[atom_no-1] should contain the highest z value.   
// It should also sort the bond_ptrs array in place in order of increasing “z value”.  
// Since bonds don’t have a z attribute, their z value is assumed to be the average z value of their two atoms.  
// I.e. bond_ptrs[0] should point to the bond that has the lowest z value 
// and bond_ptrs[atom_no-1] should contain the highest z value.Hint: use qsort.

void molsort( molecule *molecule ) {

    if (molecule == NULL) {
        return;
    } 

    // sort the atoms
    if (molecule->atom_no != 0) {
        qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom**), atom_comp);
    }
    // sort the bonds
    if (molecule->bond_no != 0) {
        qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond**), bond_comp);
    }

}

// compare atoms based on there z value

int atom_comp( const void *a, const void *b ) {
  
  double first = (*(atom **)a)->z;
  double second = (*(atom **)b)->z;

  return (first > second) - (first < second);
}

// compare bonds based on the average atom z value

int bond_comp( const void *a, const void *b ) {

  double first =  (*(bond **)a)->z;
  double second = (*(bond **)b)->z;

  return (first > second) - (first < second);
}

// This function will set the values in an affine transformation matrix, 
// xform_matrix, corresponding to a rotation of deg degrees around the x-axis.
// https://en.wikipedia.org/wiki/Rotation_matrix

void xrotation( xform_matrix xform_matrix, unsigned short deg ) {

    // convert degrees to radians
    double radian = deg * (M_PI / 180.0);

    xform_matrix[0][0] = 1.0;
    xform_matrix[0][1] = 0.0;
    xform_matrix[0][2] = 0.0;

    xform_matrix[1][0] = 0.0;
    xform_matrix[1][1] = cos(radian);
    xform_matrix[1][2] = 0.0 - sin(radian);

    xform_matrix[2][0] = 0.0;
    xform_matrix[2][1] = sin(radian);
    xform_matrix[2][2] = cos(radian);

}

// This function will set the values in an affine transformation matrix, 
// xform_matrix, corresponding to a rotation of deg degrees around the y-axis.
// https://en.wikipedia.org/wiki/Rotation_matrix

void yrotation( xform_matrix xform_matrix, unsigned short deg ) {
    
    // convert degrees to radians
    double radian = deg * (M_PI / 180.0);

    xform_matrix[0][0] = cos(radian);
    xform_matrix[0][1] = 0.0;
    xform_matrix[0][2] = sin(radian);

    xform_matrix[1][0] = 0.0;
    xform_matrix[1][1] = 1.0;
    xform_matrix[1][2] = 0.0;

    xform_matrix[2][0] = 0.0 - sin(radian);
    xform_matrix[2][1] = 0.0;
    xform_matrix[2][2] = cos(radian);

}

// This function will set the values in an affine transformation matrix, 
// xform_matrix, corresponding to a rotation of deg degrees around the z-axis.
// https://en.wikipedia.org/wiki/Rotation_matrix

void zrotation( xform_matrix xform_matrix, unsigned short deg ) {

    // convert degrees to radians
    double radian = deg * (M_PI / 180.0);

    xform_matrix[0][0] = cos(radian);
    xform_matrix[0][1] = 0.0 - sin(radian);
    xform_matrix[0][2] = 0.0;

    xform_matrix[1][0] = sin(radian);
    xform_matrix[1][1] = cos(radian);
    xform_matrix[1][2] = 0.0;

    xform_matrix[2][0] = 0.0;
    xform_matrix[2][1] = 0.0;
    xform_matrix[2][2] = 1.0;

}

// This function will apply the transformation matrix to all the atoms of the molecule
// by performing a vector matrix multiplication on the x, y, z coordinates. 
// https://www.varsitytutors.com/hotmath/hotmath_help/topics/multiplying-vector-by-a-matrix

void mol_xform( molecule *molecule, xform_matrix matrix ) {

    double xAtom, yAtom, zAtom;

    for (int i = 0; i < molecule->atom_no; i++) {

        xAtom = molecule->atoms[i].x;
        yAtom = molecule->atoms[i].y;
        zAtom = molecule->atoms[i].z;

        molecule->atoms[i].x = matrix[0][0] * xAtom + matrix[0][1] * yAtom + matrix[0][2] * zAtom;
        molecule->atoms[i].y = matrix[1][0] * xAtom + matrix[1][1] * yAtom + matrix[1][2] * zAtom;
        molecule->atoms[i].z = matrix[2][0] * xAtom + matrix[2][1] * yAtom + matrix[2][2] * zAtom;

    }

    for (int i = 0; i < molecule->bond_no; i++) {
        compute_coords(&molecule->bonds[i]);
    }

}
