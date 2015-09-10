# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 17:06:40 2015

@author: gabrielantao
"""

#-------------------------------------------------------------------------------
# Name:        GUI para pygame
# Author:      Gabriel Antao
# Created:     Jan 2015
# Copyright:   ---
# Licence:     ---
#-------------------------------------------------------------------------------
import pygame
from pygame.locals import *
import json

# TODO: Tratar a excecao no carregamento no modulo que usa essas funcoes
# Carrega o arquivo contendo os estilos
def load_style(filename):
    data = open(filename, "r")  # abre o arquivo com os dados
    style = json.loads(data.read(), "utf-8")   # le o arquivo .json
    data.close()
    return style


# Carrega o arquivo com os estilos
# TODO: transformar em list
STYLES = load_style("styles.json")

class Container(object):
    """
    Classe que serve de container para todos os widgets tomarem como referencia ao ser desenhados.
    Contem metodos para alinhar e gerenciar a geometria dos widgets que estao dentro deste container,
    atraves do algnments, paddings e margins. O gerenciamente evita tambem que os widgets se
    sobreponham.
    """
    _default_alignments = ("N", "S", "E", "W", "NE", "SE", "NW", "SW", "CENTER")

    def __init__(self, x, y, width, height, surface=None):
        self.parent = None
        self.__pos = (x, y)

        self.__maxsize = (-1, -1) # -1 nao possui tamanho maximo
        self.__minsize = (-1, -1) # -1 nao possui tamanho minimo
        self.__resizable = False  # container redimensionavel

        self.__surface = surface
        self.__widgets =  set([]) # Armazena os widgets deste container

        # gera o rect para o container
        self.set_rect()

        # Indica se a tela precisa ser atualizada
        self.dirty= True

    # Adiciona widget
    def add(self, *widgets):
        for widget in widgets:
            self.__widgets.add(widget)
            widget.parent = self

    # Remove todos os widgets
    def clear(self):
        self.__widgets.clear()

    # Remove um widget do container
    def remove(self, *widgets):
        for widget in widgets:
            self.__widgets.remove(widget)

    # Verifica se mouse esta dentro do rect
    def mouse_inside(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    # Define um rect para o widget
    def set_rect(self):
        rect = self.__surface.get_rect()
        if isinstance(self.parent, pygame.Surface): #se for window
            self.rect = rect
            self.rect.x, self.rect.y = self.__pos
        else:
            if self.parent == None: # se for um widget sem parent ainda
                self.rect = rect
            else: # se for um widget ja associado a um parent
                rect.x = self.parent.pos[0] + self.__pos[0]
                rect.y = self.parent.pos[1] + self.__pos[1]
                self.rect = self.parent.rect.clip(rect) #somente parte dentro da surface do parent

    # Retorna a posicao local do container
    @property
    def pos(self):
        return self.__pos

    # Retorna a surface do container
    @property
    def surface(self):
        return self.__surface

##    # Retorna widgets
##    @property
##    def widgets(self):
##        return self.__widgets

    # Define a posicao do label
    # TODO: verificar se fica dirty, verificar a posicao rect
    def move(self, x, y):
        self.__pos = (x, y)

    # define alinhamento do label de acordo com o conteiner que ele esta
    # altera os valoers de alinhamento chamando o metodo que gera o alinhamento do container
    # altera os valores de x e y usando set_pos
    def set_align(self, align):
        pass

    # Empacota de acordo com uma orientacao definida
    def pack(self, align=""):
        pass

    # Esquema de tabela para organizar seu conteudo interno (os widgets)
    def grid(self, align=""):
        pass

    # Esquema arbitrario de organizacao dos widgets no container
    # faz verificacao para que os widgets nao vao colidir
    # esse eh o padrao de organizacao da janela
    def place(self):
        pass

    # Desenha a superficie no widget pai (recursivo)
    def draw(self):
        for widget in self.__widgets:
            self.__surface.blit(widget.surface, widget.pos)
            widget.draw()

    # Atualiza a superficie do container (recursivo)
    def update(self, surface):
        self.__surface = surface
        self.set_rect()
        self.dirty = False
        for widget in self.__widgets:
            widget.update()

    # teste se contem o widget no window
    def __contains__(self, item):
        pass


class Frame(Container):
    def __init__(self, x, y, width, height, contents = [], image = ""):
##        super(Frame, self).__init__(self)

        self.__contents = contents

        if image != "":
            pass
        self.__bg_color = (200, 12, 200)

        self.fill(self.__bg_color)
        self.set_colorkey(self.__bg_color)

    # imprimir informacao sobre a janela
    def __repr__(self):
        return ""


class Window(Container):
    """
    Classe Window base para criacao de janelas.

    parent: endereco da surface do pygame
    x : posicao x da janela na janela principal do pygame
    y : posicao y da janela na janela principal do pygame
    width : largura da janela na janela principal do pygame
    height: altura da janela na janela principal do pygame
    style : arquivo json propriedades para criacao da janela
    """
    _default_states = ("active", "inactive")

    def __init__(self, parent, x, y, width, height, title="", style="default"):
        # TODO: colocar aqui a condição para a largura nao ser menor que o titulo da janela mais o tamanho dos icones de minimizar maximizar fechar e so aceitar numeros positivos
        self.__width = width
        self.__height = height
        self.__title = title

##        self.__layout = pygame.image.load(layout) #ARQUIVO JSON
        self.__style = STYLES["Window"][style]
        self.__state = "active"


        # atributos modificados por configure
        # TODO: Verificar se nao eh melhor por em dicionarios esses atributos.
        self.__opacity = 255   # opacidade
        self.__title_buttons = {"minimize": True, "restore": True, "close": True} # botoes habilitados
        self.__fix_position = True  # posicao fixa da janela
        # TODO: implementar redimensionamento
        self.__maxsize = [-1, -1]   # tamanho maximo para a janela ser redimensionada
        self.__minsize = [-1, -1]   # tamanho mínimo para a janela ser redimensionada
        self.__resizable = [False, False] # redimensiona horizontalmente e verticalmente

        # surface teste
        surf = pygame.Surface((100,100))
        surf.fill((255,255,60))
        super(Window, self).__init__(x, y, width, height, surf)
        self.parent = parent



    # define valores para atributos da janela
    def configure(self, **kwargs):
        pass

    # Destroi a janela
    def destroy(self):
        pass

    # Retorna o title da janela
    @property
    def title(self):
        return self.__title

    # Redefine texto do title
    def set_title(self, value):
        pass

    # define titulo para a janela
    # salvar as propriedades em dicionario
    def configure_title(self, style="default", **kwargs):
##        title = Label(self, self.__titletext, 0, 0, style, **kwargs)
        pass

    # define um icone para a janela
    # position (esquerda,centro ou direita)
    def set_icon(self, filename, mask, align):
        pass

    # define se a janela esta ativa ou inativa
    def set_active(self, value):
        self.__active = value

    # retorna se a janela esta ativa ou inativa
    def get_active(self):
        return self.__active

##    # move janela para uma posicao definida
##        # FIXME: AJEITAR ESSE METODO PARA POS
##    def move(self, x, y):
##        self.__x = x
##        self.__y = y

    # redimensiona janela
    def resize(self, width, height):
        pass

    # TODO: trocar esses nomes
    def minimizar(self):
        pass

    def maximizar(self):
        pass

    def fechar(self):
        pass


    # remove widget
    def remove_widget(self):
        pass

    # Atualiza a janela
    # TODO: ajeitar metodo para atualizar com superficie real
    def update(self):
        surf = pygame.Surface((100,100), SRCALPHA)
        surf.fill((255,255,60))
        super(Window, self).update(surf)

    def draw(self):
        super(Window, self).draw()
        self.parent.blit(self.surface, self.pos)







    # imprimir informacao sobre a janela
    def __repr__(self):
        return "MEU WINDOW"


class ImageLabel(Container):
    """Classe para gerar imagens para uso em outros widgets por exemplo dividir um checkbox com texto e imagem"""
    # Sobrescreve metodos e levanta erro se provocar acesso
    def add(self, widget):
        raise NotImplementedError("Label do not have add() method")
    def clear(self):
        raise NotImplementedError("Label do not have clear() method")
    def remove(self, widget):
        raise NotImplementedError("Label do not have remove() method")

class Label(Container):
    """Classe que gera labels (etiquetas) para serem usadas na janela.

    text : texto a ser escrito no label
    status : indica se o label esta em evidencia ou nao (mouse sobre ele)
    style : armazena o dicionario com o estilo atual
    mouse_abled: indica se o mouse esta habilitado para trocar o status ou nao
    attributes : caracteristicas do label quando esta ativo ou inativo
    style : armazena o dicionario que deve ser usado para gerar os estilos do label
    """

    _default_states = ("active", "normal")
    _default_attributes = ("font","size","bold","italic","underline","color","bg_color","antialias")

    def __init__(self, text, x, y, style="default", **kwargs):
        self.__text = str(text)
        self.__status = "normal"
        self.__style = STYLES["Label"][style]

        self.__mouse_abled = True

        # valores para dos atributos
        self.__attributes = self.__style[self.__status]

        # define os atributos passados pelo usuario
        self.configure(self.__status, **kwargs)

        # cria a superficie que contem o label
        surface = self.__generate_surface()
        width, height = surface.get_size()
        super(Label, self).__init__(x, y, width, height, surface)

    # Gera surface baseado nos atributos
    def __generate_surface(self):
        font = pygame.font.SysFont(self.__attributes["font"], self.__attributes["size"],
                                    self.__attributes["bold"], self.__attributes["italic"])
        font.set_underline(self.__attributes["underline"])

        if self.__attributes["bg_color"] == None:
            surface = font.render(self.__text, self.__attributes["antialias"],
                                self.__attributes["color"])
        else:
            surface = font.render(self.__text, self.__attributes["antialias"],
                                self.__attributes["color"], self.__attributes["bg_color"])
        return surface

    # Sobrescreve metodos
    def add(self, widget):
        raise NotImplementedError("Label do not have add() method")
    def clear(self):
        raise NotImplementedError("Label do not have clear() method")
    def remove(self, widget):
        raise NotImplementedError("Label do not have remove() method")

    # Retorna valores dos atributos
    @property
    def attributes(self):
        return self.__attributes

    # Define valores para atributos da janela
    # NOTE: Esse metodo lanca excecao caso nao exista uma das chaves passadas como parametro, mas
    # nao lanca excecao para valores de chave incorretos isso ficara a cargo do modulo do pygame
    def configure(self, status, **kwargs):
        if (status in Label._default_states) == False:
            raise ValueError("Label status cannot be \"%s\". Status must be %s."%(status, Label._default_states))

        # preenche os atributos definidos para o label
        for key, value in kwargs.items():
            if (key in Label._default_attributes):
                if self.__attributes[key] != value: # se o valor for diferente do atual
                    self.__attributes[key] = value
                    self.dirty = True
            else:
                raise ValueError("Label do not have the attribute \"%s\". Attribute must be %s." %(key, Label._default_attributes))


    # Retorna conteudo do texto
    @property
    def text(self):
        return self.__text

    # Define conteudo do texto
    @text.setter
    def text(self, text):
        if text != self.__text:
            self.__text = str(text)
            self.dirty = True

    # Retorna se o mouse esta habilitado para alterar o label
    @property
    def mouse_abled(self):
        return self.__mouse_abled

    # Define se o mouse esta habilitado para alterar o label
    @mouse_abled.setter
    def mouse_abled(self, value):
        if isinstance(value, bool):
            self.__mouse_abled = value
        else:
            raise ValueError("Mouse_abled must be boolean.")

    # Retorna status do label
    @property
    def status(self):
        return self.__status


    # Atualiza o conteudo do label quando estiver ativo ou normal
    def update(self):
        if self.__mouse_abled == True:
            if self.mouse_inside() == True:
                current_status = "active"
            elif self.mouse_inside() == False:
                current_status = "normal"

            if self.__status != current_status:
                self.__status = current_status
                self.__attributes = self.__style[self.__status]
                self.dirty = True

        if self.dirty:
            super(Label, self).update(self.__generate_surface())


    # Imprimir informacao sobre o label
    def __repr__(self):
##        string = json.dumps(self.__style, indent=2, sort_keys=True)
        return "< [Label] \"%s\" >" %self.__text


class ImageTextLabel:
    """Composicao de label e imagem em um mesmo widget."""
    pass

class ProgressBar(Container):

    _default_orientations = ("horizontal", "vertical") # orientacao possivel
    _default_senses = ("regular", "reverse") # direcao regular de incremento/decremento ou invertida
    _default_states = ("empty", "full", "incomplete")

    # Retirar esses gets e colocar tudo no configure. aqui so inicializar os valores padrao e depois
    # os configure lida com o preenchumento
    def __init__(self, x, y, style="default", **kwargs):
        self.__limits = kwargs.get("limits", (0, 100))
        self.__unit = kwargs.get("unit", "%")
        self.__value = kwargs.get("value", 0) # porcentagem
        self.__step = kwargs.get("step", 1)  # passso em pixels
        self.__text = str(kwargs.get("text", self.__value)) + " " + self.__unit
        self.__style = STYLES["Progress Bar"][style]

        surface = self.__generate_surface()
        width, height = surface.get_size()
        super(Label, self).__init__(x, y, width, height, surface)

    def __generate_surface(self):
        image = pygame.image.load(self.__style["filename"])
        surface = pygame.Surface((self.__style["empty"][2],self.__style["empty"][3]), SRCALPHA)
        surface.blit(image, (0, 0), self.__style["empty"])
        if self.__value > 0:
            # calcular aqui as barras para ficar certo
            pass
        dim = (self.__style["full"][0],self.__style["full"][1], 20, self.__style["full"][3])
        surface.blit(image, (0, 0), self.__style["full"])
        # blitar o texto aqui se nao for sting vazia ""
        return surface

    def configure(self, **kwargs):
        pass

    # Incrementa (ou decrementa) um valor em porcentagem da barra
    def increment(self, value=1):
        value = int(value)
        current_percent = self.__value
        if -100 <= value <= 100:
            self.__value += value
            if self.__value >= 100:
                self.__value = 100
            elif self.__value <= 0:
                self.__value = 0
        if current_percent != self.__value:
            self.dirty = True

    @property
    def limits(self):
        return self.__limits

    @limits.setter
    def limits(self, newvalue):
        if isinstance(newvalue, tuple) or isinstance(newvalue, list):
            self.__limits = newvalue
        else:
            raise ValueError("Limits must be tuple or list.")

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, newvalue):
        newvalue = str(newvalue)
        self.__unit = newvalue
        self.dirty = True

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, value):
        value = int(value)
        if value > 0:
            self.__step = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if value != self.__text:
            self.__text = str(value)
            self.dirty = True

    def update(self):
        if self.dirty:
            super(ProgressBar, self).update(self.__generate_surface())

class CheckBox(Container):
    """Classe que modela widgets do tipo checkbox"""

    _default_states = ("checked", "unchecked","checked disabled","unchecked disabled")
    def __init__(self, parent, x, y, text="", image="", state="unchecked", style="default", **kwargs):
        if text == "" and image == "":
            content = []
        super(CheckBox, self).__init__(parent, x, y, width, height)
        self.__text = text
        self.__image = image
        self.__state = state
        self.__style = STYLES["CheckBox"][style]
        # aproveita a heranca para chamar metodo da superclasse para organizar o proprio conteudo


class ToolTip:
    """Widget que mostra dicas de dicas ao manter o mouse um tempo determinado sobre um widget."""
    pass

class Button(Container):
    # estados possiveis para os botoes
    __default_states = ("normal", "hover", "down", "focus", "disabled")

    def __init__(self, x, y, width, height, **kwargs):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

        self.__state = "normal" # estado atual do botao

        self.configure(self, **kwargs)

    # define valores para atributos da janela
    def configure(self, **kwargs):
        pass

    # define o estado do botao
    # estados: normal, hover, down, focus, disabled
    def set_state(self, value):
        self.__state = value

    # retorna estado do botao
    def get_state(self):
        return self.__state

    # atualiza o estado do botao
    def update(self):
        pass

    # imprimir informacao sobre o botao
    def __repr__(self):
        return ""

if __name__ == "__main__":
    print "TESTE TESTE TESTE"
    print json.dumps(STYLES["Label"]["style2"], indent=2, sort_keys=True)