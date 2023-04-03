// Assignment: CIS*2750 W23 Assignment 3
// Due Date: March 21 2023
// Name: Or Brener
// Student #: 1140102

#ifndef _MOL_H
#define _MOL_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/* ---------- Structs ---------- */

// describes an atom and its position in 3D space
typedef struct atom 
{ 
  char element[3]; // null-terminated string representing the element name of the atom
  double x, y, z; // double precision floating point numbers describing the position in Angstroms (Å) of the atom relative to a common origin for a molecule
} atom;

// represents a co-valent bond between two atoms
typedef struct bond 
{  
  unsigned short a1, a2; // indicies of the two atoms (within an array with address atoms)
  unsigned char epairs; // number of electron pairs in the bond
  atom *atoms; // address of a1 & a2
  double x1, x2, y1, y2, z, len, dx, dy; // x1, y1, x2, y2 will store the x and y coordinates of atoms a1 and a2 respectively. 
                                         // z will store the average z value of a1 and a2. 
                                         // len will store the distance from a1 to a2. 
                                         // dx and dy will store the differences between the x and y values of a2 and a1 divided by the length of the bond.
} bond;

// represents a molecule which consists of zero or more atoms, and zero or more bonds
typedef struct molecule 
{ 
  unsigned short atom_max, atom_no; // atom_max is a non-negative integer that records the dimensionality of an array pointed to by atoms
                                    // atom_no is the number of atoms currently stored in the array atoms
  atom *atoms, **atom_ptrs; // responsible for allocating enough memory to the atoms pointer
                            // atom_ptrs array of pointers,  dimensionality will correspond to the atoms array. The pointer in the pointer array will be initialized to point to the atom structure
  unsigned short bond_max, bond_no; // bond_max is a non-negative integer that records the dimensionality of an array pointed to by bonds
                                    // bond_no is the number of bonds currently stored in the array bonds
  bond *bonds, **bond_ptrs; // responsible for allocating enough memory to the bonds pointer
                            // // bond_ptrs array of pointers,  dimensionality will correspond to the bonds array. The pointer in the pointer array will be initialized to point to the bond structure
} molecule; 

/* ---------- Structs ---------- */

// represents a 3-d affine transformation matrix 
typedef double xform_matrix[3][3];

typedef struct mx_wrapper
{
  xform_matrix xform_matrix;
} mx_wrapper;

/* ---------- Function Prototypes ---------- */

void atomset( atom *atom, char element[3], double *x, double *y, double *z );
void atomget( atom *atom, char element[3], double *x, double *y, double *z );
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs );
void compute_coords( bond *bond );
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs );
molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ); 
molecule *molcopy( molecule *src );
void molfree( molecule *ptr );
void molappend_atom( molecule *molecule, atom *atom );
void molappend_bond( molecule *molecule, bond *bond );
void molsort( molecule *molecule );
void xrotation( xform_matrix xform_matrix, unsigned short deg );
void yrotation( xform_matrix xform_matrix, unsigned short deg );
void zrotation( xform_matrix xform_matrix, unsigned short deg );
void mol_xform( molecule *molecule, xform_matrix matrix );

// helper functions
int atom_comp( const void *a, const void *b );
int bond_comp( const void *a, const void *b );


/* ---------- Function Prototypes ---------- */

typedef struct rotations
{
  molecule *x[72];
  molecule *y[72];
  molecule *z[72];
} rotations;

rotations *spin( molecule *mol );
void rotationsfree( rotations *rotations );

#endif
