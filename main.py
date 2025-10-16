import re

lista_definicoes = [
    ('palavras_chave',      r'\bint|float|double|char|void|short|long|if|else|while|for|switch|break|continue|typedef|return|struct|const|extern|static|sizeof|unsigned|signed|case|auto|default|do|enum|goto|register|volatile|union\b'),
    ('comentario',          r'\/\/.*?$|\/\*(.|\n)*?\*\/'),
    ('pre_processador',     r'#.*'),
    ('number',      r'\b[0-9]+(\.\d*([eE][+-]?\d+)?|\d+[eE][+-]?\d+)?\b'),
    ('char',                r'\'([^\\\'\n]|\\.)\''),
    ('strings',             r'"([^"\\]|\\.)*"'),
    ('identificadores',     r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('operadores_atribuicao', r'\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|='),
    ('operadores_gerais',   r'->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%<>&|!^~?]'),
    ('pontuacao',           r'[(){}\[\].,:?]'),
    ('final_linha',         r';'),
    ('quebra_linha',        r'\n'),
    ('pular_espacamentos',  r'[ \t]+'),
    ('erro',                r'.') 
]

partes_regex = []
for nome, padrao in lista_definicoes:
    partes_regex.append(f'(?P<{nome}>{padrao})')
regex_principal = '|'.join(partes_regex)

token_regex = re.compile(regex_principal, re.MULTILINE) #estudar isso


class Token:
    """Classe para representar um token de forma mais estruturada."""
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        if "id" in self.tipo:
            return f"{self.tipo}"
        elif "number" in self.tipo:
            return f"{self.tipo}, {self.valor.strip()}"
        else:
            return f"{self.valor.strip()}"


class TabelaSimbolos:
    """Classe para gerenciar a tabela de símbolos."""
    def __init__(self):
        self.simbolos = []
        self.proximo_id = 1

    def adicionar(self, simbolo_texto):
        """Adiciona um símbolo à tabela APENAS se ele ainda não existir."""
        encontrado = False
        for _, texto_existente in self.simbolos:
            if simbolo_texto == texto_existente:
                encontrado = True
                break
        
        if not encontrado:
            self.simbolos.append((self.proximo_id, simbolo_texto))
            self.proximo_id += 1
            
    def __repr__(self):
        return str(self.simbolos)


def analisar(codigo_fonte):
    """
    Função principal que realiza a análise léxica.
    Recebe o código como uma string e retorna a lista de tokens e a tabela de símbolos.
    """
    tokens = []
    tabela_simbolos = TabelaSimbolos()
    
    for match in token_regex.finditer(codigo_fonte):
        tipo = match.lastgroup
        valor = match.group()

        if tipo in ['quebra_linha', 'pular_espacamentos', 'comentario']:
            continue
        elif tipo == 'erro':
            print(f"Erro Léxico: Caractere inesperado '{valor}'")
            continue

        if tipo == 'identificadores':
            tabela_simbolos.adicionar(valor)
            for id_simbolo, simbolo in tabela_simbolos.simbolos:
                if simbolo==valor:
                    tipo=f"id, {id_simbolo}"


        tokens.append(Token(tipo, valor))

    return tokens, tabela_simbolos


if __name__ == "__main__":
    nome_arquivo = input("Digite o nome do arquivo (ex: teste.c): ")
    
    try:
        with open(f'{nome_arquivo}', 'r', encoding='utf-8') as reader:
            codigo = reader.read()
            
            lista_de_tokens, tabela_de_simbolos = analisar(codigo)

            print("\n--- LISTA DE TOKENS ---")
            for token in lista_de_tokens:
                print(token)
            
            print("\n--- TABELA DE SÍMBOLOS ---")
            print("ID | Símbolo")
            print("---+--------")
            for id_simbolo, simbolo in tabela_de_simbolos.simbolos:
                print(f"{id_simbolo:^2} | {simbolo}")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")