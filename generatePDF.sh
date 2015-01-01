#!/bin/bash
doxygen
cd doc/latex
make
cd -
mv doc/latex/refman.pdf .

