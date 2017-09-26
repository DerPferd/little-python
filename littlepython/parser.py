from __future__ import unicode_literals

from littlepython.ast import Block, Assign, If, ControlBlock, Var, BinaryOp, UnaryOp, Int, GetArrayItem, SetArrayItem
from littlepython.feature import Features
from littlepython.tokenizer import TokenTypes


class Parser(object):
    def __init__(self, tokenizer, features=Features.ALL):
        self.tokenizer = tokenizer
        self.cur_token = next(tokenizer)
        self.features = features

    def error(self, msg=""):
        raise Exception("Invalid syntax: " + msg)

    def eat(self, token_type):
        if self.cur_token.type == token_type:
            self.cur_token = next(self.tokenizer)
        else:
            self.error("Excepted token type {} got {}".format(token_type, self.cur_token.type))

    def program(self):
        """program : (newline) statement
                   | program statement
        """
        statements = []
        if self.cur_token.type == TokenTypes.NEW_LINE:
            self.eat(TokenTypes.NEW_LINE)
        while self.cur_token.type != TokenTypes.EOF:
            statements += [self.statement()]
        return Block(statements)

    def statement(self):
        """
        statement   : variable ASSIGN expression
                    | control
                    | empty
        Feature Type Array adds:
                    | variable SETITEM expression
        """
        if self.cur_token.type == TokenTypes.VAR:
            left = self.variable()
            op = self.cur_token
            self.eat(TokenTypes.ASSIGN)
            right = self.expression()
            if Features.TYPE_ARRAY in self.features and isinstance(left, GetArrayItem):
                # Remake this as a setitem.
                return SetArrayItem(left.left, left.right, right)
            else:
                return Assign(op, left, right)
        elif self.cur_token.type in TokenTypes.control(self.features):
            return self.control()

    def control(self):
        """
        control    : 'if' ctrl_exp block ('elif' ctrl_exp block)* ('else' block)
        """
        self.eat(TokenTypes.IF)
        ctrl = self.expression()
        block = self.block()
        ifs = [If(ctrl, block)]
        else_block = Block()
        while self.cur_token.type == TokenTypes.ELIF:
            self.eat(TokenTypes.ELIF)
            ctrl = self.expression()
            block = self.block()
            ifs.append(If(ctrl, block))
        if self.cur_token.type == TokenTypes.ELSE:
            self.eat(TokenTypes.ELSE)
            else_block = self.block()
        return ControlBlock(ifs, else_block)

    def block(self):
        """
        block      : { (newline) statements } (newline)
        """
        statements = []
        self.eat(TokenTypes.LBRACE)
        if self.cur_token.type == TokenTypes.NEW_LINE:
            self.eat(TokenTypes.NEW_LINE)
        while self.cur_token.type != TokenTypes.RBRACE:
            statements.append(self.statement())
        self.eat(TokenTypes.RBRACE)
        if self.cur_token.type == TokenTypes.NEW_LINE:
            self.eat(TokenTypes.NEW_LINE)
        return Block(statements)

    def variable(self):
        """
        variable    : variable
        Feature Type Array adds:
        variable    : variable[expression]
        """
        var = Var(self.cur_token)
        self.eat(TokenTypes.VAR)
        if Features.TYPE_ARRAY in self.features:
            while self.cur_token.type == TokenTypes.LBRACKET:
                self.eat(TokenTypes.LBRACKET)
                # Start passed the logical ops.
                expr = self.operator_expression(level=2)
                self.eat(TokenTypes.RBRACKET)
                var = GetArrayItem(left=var, right=expr)
        return var

    def expression(self):
        node = self.operator_expression()
        if self.cur_token.type == TokenTypes.NEW_LINE:
            self.eat(TokenTypes.NEW_LINE)
        return node

    def operator_expression(self, level=0):
        levels = ({TokenTypes.OR, TokenTypes.AND},
                  {TokenTypes.NOT},
                  {TokenTypes.EQUAL, TokenTypes.NOT_EQUAL, TokenTypes.GREATER, TokenTypes.GREATER_EQUAL, TokenTypes.LESS, TokenTypes.LESS_EQUAL},
                  {TokenTypes.ADD, TokenTypes.SUB},
                  {TokenTypes.DIV, TokenTypes.MULT, TokenTypes.MOD})

        # If out of level then grab factor instead.
        if level >= len(levels):
            return self.factor()

        if next(iter(levels[level])) in TokenTypes.BINARY_OPS:
            node = self.operator_expression(level+1)
        else:
            node = None

        while self.cur_token.type in levels[level]:
            token = self.cur_token
            self.eat(token.type)

            if token.type in TokenTypes.BINARY_OPS:
                node = BinaryOp(op=token, left=node, right=self.operator_expression(level+1))
            if token.type in TokenTypes.UNARY_OPS:
                node = UnaryOp(op=token, right=self.operator_expression(level+1))

        if node is None:
            node = self.operator_expression(level+1)

        return node

    def factor(self):
        token = self.cur_token
        if token.type == TokenTypes.ADD:
            self.eat(TokenTypes.ADD)
            return UnaryOp(token, self.factor())
        elif token.type == TokenTypes.SUB:
            self.eat(TokenTypes.SUB)
            return UnaryOp(token, self.factor())
        elif token.type == TokenTypes.INT:
            self.eat(TokenTypes.INT)
            return Int(token)
        elif token.type == TokenTypes.LPAREN:
            self.eat(TokenTypes.LPAREN)
            node = self.expression()
            self.eat(TokenTypes.RPAREN)
            return node
        elif token.type == TokenTypes.VAR:
            # self.eat(TokenTypes.VAR)
            return self.variable()
        else:
            self.error("Excepted a factor type got {}".format(self.cur_token.type))
