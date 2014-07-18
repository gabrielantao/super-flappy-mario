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
import pygame.draw, pygame.surface, pygame.transform # somente o modulo de interesse


class Vetor:
    """Esta classse define o objeto vetor e as operações possíveis com esse tipo"""

    def __init__(self, i=0, j=0, pos_x=0, pos_y=0):
        self.i = i
        self.j = j
        self.pos_x = pos_x
        self.pos_y = pos_y

    # soma dois vetores
    def __add__(self, vetor):
        return Vetor(self.i + vetor.i, self.j + vetor.j)

    # subtrai dois vetores
    def __sub__(self, vetor):
        return Vetor(self.i - vetor.i, self.j - vetor.j)

    # produto por um escalar. é preciso as duas formas para que nao "unsupported operand type(s) *: int 'instance'" vewr documentação language reference > data model
    def __mul__(self, escalar):
        return Vetor(self.i * escalar, self.j * escalar)
    def __rmul__(self, escalar):
        return Vetor(self.i * escalar, self.j * escalar)

    # divisão por escalar
    def __div__(self, escalar):
        return Vetor(self.i/escalar, self.j/escalar)

    # vetor oposto chamado quando -vetor
    def __neg__(self):
        return Vetor(-self.i, -self.j)

    # calcula modulo
    def modulo(self):
        return math.sqrt(self.i**2 + self.j**2)

    # calcula produto vetorial a partir das componentes
    # embora o retorno deveria ser um vetor so interessa por ora o seu valor
    def p_vetorial(self, vetor):
        return self.i*vetor.j - self.j*vetor.i

    # calcula angulo em graus entre um vetor e o eixo +Ox
    # a orientação horaria é positiva e anti-horaria negativa devido posicionamento dos eixos
    # foi usada atan2 que retorna valores entre pi e -pi ver documentacao
    # faz uma aproximação para nao obter valores com muitas casas decimais desnecessarias
    def angulox(self):
        return round( math.degrees(math.atan2(self.j,self.i)), 2 )



#editado para testar a sincronização com o local...

