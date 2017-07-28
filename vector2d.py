#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Gabriel
#
# Created:     27/06/2014
# Copyright:   (c) Gabriel 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import math

class Vector:
    """Esta classse define o objeto vetor e as operações possíveis com esse tipo"""

    def __init__(self, i=0, j=0, pos_x=0, pos_y=0):
        self.i = i
        self.j = j
        self.pos_x = pos_x
        self.pos_y = pos_y

    # soma dois vetores
    def __add__(self, vetor):
        return Vector(self.i + vetor.i, self.j + vetor.j)

    # subtrai dois vetores
    def __sub__(self, vetor):
        return Vector(self.i - vetor.i, self.j - vetor.j)

    # produto por um escalar. é preciso as duas formas para que nao "unsupported operand type(s) *: int 'instance'" vewr documentação language reference > data model
    def __mul__(self, escalar):
        return Vector(self.i * escalar, self.j * escalar)
    def __rmul__(self, escalar):
        return Vector(self.i * escalar, self.j * escalar)

    # divisão por escalar
    def __div__(self, escalar):
        return Vector(self.i/escalar, self.j/escalar)

    # vetor oposto chamado quando -vetor
    def __neg__(self):
        return Vector(-self.i, -self.j)

    # calcula modulo
    def modulo(self):
        return math.sqrt(self.i**2 + self.j**2)

    # calcula produto vetorial a partir das componentes
    # embora o retorno deveria ser um vetor so interessa por ora o seu valor
    def p_vetorial(self, vetor):
        return self.i*vetor.j - self.j*vetor.i

    def __repr__(self):
        return "Vector({}, {})".format(self.i, self.j)
