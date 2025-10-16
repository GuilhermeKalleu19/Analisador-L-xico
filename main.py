import re

lista = [
    ('palavras_chave',       r'\bint|float|double|char|void|short|long|if|else|while|for|switch|break|continue|typedef|return|struct|const|extern|static|sizeof|unsigned|signed|case|auto|default|do|enum|goto|register|volatile|union\b'),
    ('comentario',      r'//.*?$|/\*.*?\*/'),
    ('pre_processador',     r'#.*'),
    ('int',      r'\b\d+\b'),
    ('char',        r'\'([^\\\'\n]|\\.)\''),
    ('float',        r'\d+\.\d*([eE][+-]?\d+)?|\d+[eE][+-]?\d+'),
    ('strings',      r'"([^"\\]|\\.)*"'),
    ('identificadores',        r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('operadores_atribuicao',        r'\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|='),
    ('operadores_gerais',        r'->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%<>&|!^~?]'),
    #('operadores',        r'->|==|!=|<=|>=|&&|\|\||\+\+|--|[-+*/%=<>&|!^~]'),
    ('pontuacao',        r'[(){}\[\].,:?]'),
    ('final_linha',        r';'),
    ('pular_espacamentos',      r'[ \t]+'),
    ('quebra_linha',     r'\n'),
    ('erro',     r'.')
]

class listaTokens:
    def __init__(self):
        self.tokens = []


class tabelaSimbolos:
    def __init__(self):
        self.simbolos = []
        self.proximo_id = 1

    def adicionar(self, simbolo):
        for id, texto_repetido in self.simbolos:
            if simbolo == texto_repetido:
                flag = True
                break
        if flag:
            self.simbolos.append((self.proximo_id, simbolo))
            self.proximo_id += 1