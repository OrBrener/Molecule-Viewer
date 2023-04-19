CC = clang
CFLAGS = -std=c99 -Wall -pedantic
PYTHON_LANGUAGE_LIB_DIR = /usr/lib/python3.7/config-3.7m-x86_64-linux-gnu
PYTHON_H_DIR = /usr/include/python3.7m

all: libmol.so _molecule.so

clean:
	rm -f *.o *.so

_molecule.so: molecule_wrap.o
	$(CC) molecule_wrap.o -shared -L. -lmol -L$(PYTHON_LANGUAGE_LIB_DIR) -lpython3.7m -dynamiclib -o _molecule.so

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -c molecule_wrap.c -fpic -I$(PYTHON_H_DIR) -o molecule_wrap.o

molecule_wrap%c molecule%py: molecule.i 
	swig -python molecule.i

libmol.so: mol.o
	$(CC) mol.o -shared -lm -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fpic -o mol.o
