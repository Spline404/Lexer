class Tokens:
    EOF = "EOF"
    INT = "INT"
    FLOAT = "FLOAT"
    QW = "QW"
    WORD = "WORD"
    CONST = "CONST"
    LET = "LET"
    DECLAR = "DECLAR"
    SYM = "SYM"
    DOT = "DOT"
    STR = "STR"


tokens = []


class Token:
    __slots__ = ("t", "v")

    def __init__(self, t, v):
        self.t = t
        self.v = v

    def __repr__(self):
        return f"Token(<T> = ({self.t}); <V> = ({self.v}))"


class Lexer:
    __slots__ = ("data", "pos", "l")

    def __init__(self, data):
        with open(data, "r") as f:
            self.data = f.read()
        self.pos = 0
        self.l = len(self.data)

    def get_tok(self):
        return self.data[self.pos]

    def next_pos(self):
        self.pos += 1

    def push_tok(self, t, v):
        tokens.append(Token(t, v))

    def peek_tok(self):
        if self.pos + 1 < self.l:
            return self.data[self.pos + 1]
        return None

    def tokinaize(self):
        while self.pos < self.l:
            tok = self.get_tok()
            if tok in (" ", "\n", "\t"):
                self.next_pos()
                continue
            if tok == "#":
                self.next_pos()
                while self.get_tok() != "\n":
                    self.next_pos()
                continue

            if tok == "=":
                self.push_tok(Tokens.QW, tok)
                self.next_pos()
                continue
            if tok == "+" or tok == "-":
                self.push_tok(Tokens.SYM, tok)
                self.next_pos()
                continue
            if tok == ".":
                self.push_tok(Tokens.DOT, tok)
                self.next_pos()
                continue
            if tok == "'" or tok == '"':
                q = tok
                m = tok
                self.next_pos()
                while self.get_tok() != q:
                    m += self.get_tok()
                    self.next_pos()
                if self.pos < self.l:
                    m += self.get_tok()
                    self.next_pos()
                self.push_tok(Tokens.STR, m)
                continue              

            if tok.isdigit():
                n = tok
                while self.peek_tok() and self.peek_tok().isdigit():
                    self.next_pos()
                    n += self.get_tok()
                if self.peek_tok() == ".":
                    self.next_pos()
                    tok = self.get_tok()
                    n += tok 
                    while self.peek_tok() and self.peek_tok().isdigit():
                        self.next_pos()
                        n += self.get_tok()
                    self.push_tok(Tokens.FLOAT, n)
                    self.next_pos()
                    continue
                self.push_tok(Tokens.INT, n)
                self.next_pos()
                continue

            if tok.isalpha():
                t = tok
                while self.peek_tok() and self.peek_tok().isalpha():
                    self.next_pos()
                    t += self.get_tok()
                if t == "let":
                    self.push_tok(Tokens.LET, t)
                    self.next_pos()
                    continue
                if t == "const":
                    self.push_tok(Tokens.CONST, t)
                    self.next_pos()
                    continue
                if t == "declar":
                    self.push_tok(Tokens.DECLAR, t)
                    self.next_pos()
                    continue
                self.push_tok(Tokens.WORD, t)
                self.next_pos()
                continue


lexer = Lexer("f.txt")
lexer.tokinaize()
print(lexer.data)
for c in tokens:
    print(c)

_nodes = []

class VAR:
    ___slots__ = ("n", "v", "t")

    def __init__(self, n, v, t):
        self.n = n
        self.v = v
        self.t = t
    
    def __repr__(self):
        return f"Node VAR: <n: {self.n}; v: {self.v}; t: {self.t}>"
    
class Parser:
    __slots__ = ("tl", "pos", "l")

    def __init__(self, tl):
        self.tl = tl
        self.pos = 0
        self.l = len(self.tl)
    
    def get_tok(self):
        return self.tl[self.pos]

    def next_pos(self):
        self.pos += 1
    
    def peek_tok(self):
        if self.pos + 1 < self.l:
            return self.tl[self.pos + 1]
        return None

    def create_node(self, cls):
        _nodes.append(cls)
    
    def is_Token(self, t, itf):
        if t.t == itf:
            return True
        return False

    def is_Value(self, t):
        if t.t in (Tokens.INT, Tokens.STR, Tokens.FLOAT):
            return True
        return False
    
    def check_value_type(self, targ):
        match targ.t:
            case Tokens.FLOAT: return "flt"
            case Tokens.INT: return "int"
            case Tokens.STR: return "str"
            case _: "notype"

    def analize(self):
        while self.pos < self.l:
            tok = self.get_tok()
            value = None
            if self.is_Token(tok, Tokens.WORD):
                name = tok.v
                self.next_pos()
                if self.is_Token(self.get_tok(), Tokens.QW): 
                    self.next_pos()
                    t = self.get_tok()
                    if self.is_Value(t):
                        value = t.v
                        v_type = self.check_value_type(t)
                    self.create_node(VAR(name, value, v_type))
            self.next_pos()

parser = Parser(tokens)
parser.analize()
for n in _nodes:
    print(n)
