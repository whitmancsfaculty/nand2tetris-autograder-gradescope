"""
hjcCompile.py -- CompileEngine class for Hack computer Jack compiler
Solution provided by Nand2Tetris authors, licensed for educational purposes
Refactored and skeleton-ized by Janet Davis, April 18, 2016
"""

from hjcTokens import *
from hjcTokenizer import *
from hjcOutputFile import *
from hjcSymbolTable import *
from hjcVmWriter import *

xml = True  # Enable _WriteXml...() functions

class CompileEngine(object):

    def __init__(self, inputFileName, outputFileName, xmlOutputFileName, source=True):
        """
        Initializes the compilation of 'inputFileName' to 'outputFileName'.
        If 'source' is True, source code will be included as comments in the
            output.
        """
        self.className = None
        self.labelCounter = 0
        self.inputFileName = inputFileName
        self.source = source
        self.xmlIndent = 0
        self.xmlOutputFile = OutputFile(xmlOutputFileName)
        self.vmWriter = VmWriter(outputFileName)
        self.symbolTable = SymbolTable()
        self.tokenizer = Tokenizer(inputFileName, self.xmlOutputFile, source)
        self._NextToken()


    def Close(self):
        """
        Finalize the compilation and close the output file.
        """
        self.xmlOutputFile.Close()
        

    def CompileClass(self):
        """
        Compiles <class> :=
            'class' <class-name> '{' <class-var-dec>* <subroutine-dec>* '}'

        ENTRY: Tokenizer positioned on the initial keyword.
        EXIT:  Tokenizer positioned after final '}'
        """
        self._WriteXmlTag('<class>\n')
        self._ExpectKeyword(KW_CLASS)
        self._NextToken()

        self.className = self._ExpectIdentifier()
        self._NextToken()

        self._ExpectSymbol('{')
        self._NextToken()

        while True:
            if not self._ExpectKeyword((KW_STATIC, KW_FIELD), lookahead=True, optional=True):
                break
            self._CompileClassVarDec();

        while True:
            if not self._ExpectKeyword((KW_CONSTRUCTOR, KW_FUNCTION, KW_METHOD), lookahead=True, optional=True):
                break
            self._CompileSubroutine();

        self._ExpectSymbol('}')
        self._WriteXmlTag('</class>\n')
        if self.tokenizer.Advance():
            self._RaiseError('Junk after end of class definition')


    def _CompileClassVarDec(self):
        """
        Compiles <class-var-dec> :=
            ('static' | 'field') <type> <var-name> (',' <var-name>)* ';'

        ENTRY: Tokenizer positioned on the initial keyword.
        EXIT:  Tokenizer positioned after final ';'.
        """
        self._WriteXmlTag('<classVarDec>\n')

        storageClass = self._ExpectKeyword((KW_STATIC, KW_FIELD))
        self._NextToken()

        if self._ExpectKeyword((KW_INT, KW_CHAR, KW_BOOLEAN), optional=True):
            variableType = self.tokenizer.KeywordStr()
        else:
            variableType = self._ExpectIdentifier()
        self._NextToken()

        while True:
            variableName = self._ExpectIdentifier()
            self._NextToken()
            if storageClass == KW_STATIC:
                self._DefineSymbol(variableName, variableType, SYMK_STATIC)
            else: 
                self._DefineSymbol(variableName, variableType, SYMK_FIELD)
            if not self._ExpectSymbol(',', optional=True):
                break
            self._NextToken()

        self._ExpectSymbol(';')
        self._NextToken()
        self._WriteXmlTag('</classVarDec>\n')

    def _CompileSubroutine(self):
        """
        Compiles <subroutine-dec> :=
            ('constructor' | 'function' | 'method') ('void' | <type>)
            <subroutine-name> '(' <parameter-list> ')' <subroutine-body>
            
        ENTRY: Tokenizer positioned on the initial keyword.
        EXIT:  Tokenizer positioned after <subroutine-body>.
        """
        self._WriteXmlTag('<subroutineDec>\n')
        self.symbolTable.StartSubroutine()
        self.labelCounter = 0

        subroutineType = self._ExpectKeyword((KW_CONSTRUCTOR, KW_FUNCTION, KW_METHOD))
        self._NextToken()

        if self._ExpectKeyword((KW_INT, KW_CHAR, KW_BOOLEAN, KW_VOID), optional=True):
            returnType = self.tokenizer.KeywordStr()
        else:
            returnType = self._ExpectIdentifier()
        self._NextToken()

        subroutineName = self._ExpectIdentifier()
        if self.className:
            subroutineName = self.className + '.' + subroutineName
        self._NextToken()

        self._ExpectSymbol('(')
        self._NextToken()

        if subroutineType is KW_METHOD:
            self._DefineSymbol('this', self.className, SYMK_ARG)
        self._CompileParameterList()
        
        self._ExpectSymbol(')')
        self._NextToken()

        if subroutineType is KW_CONSTRUCTOR:
            nFields = self.symbolTable.VarCount(SYMK_FIELD)
            self.vmWriter.WriteCall('Memory.alloc', nFields)
            self.vmWriter.WritePop('pointer', 0)
        
        self._CompileSubroutineBody(subroutineName)

        self._WriteXmlTag('</subroutineDec>\n')


    def _CompileParameterList(self):
        """
        Compiles <parameter-list> :=
            ( <type> <var-name> (',' <type> <var-name>)* )?

        ENTRY: Tokenizer positioned on the initial keyword.
        EXIT:  Tokenizer positioned after <subroutine-body>.
        """
        self._WriteXmlTag('<parameterList>\n')

        while True:
            if self._ExpectSymbol(')', lookahead=True, optional=True):
                break;
            
            if self._ExpectKeyword((KW_INT, KW_CHAR, KW_BOOLEAN), optional=True):
                parameterType = self.tokenizer.KeywordStr()
            else:
                parameterType = self._ExpectIdentifier()
            self._NextToken()

            parameterName = self._ExpectIdentifier();
            self._NextToken();

            self._DefineSymbol(parameterName, parameterType, SYMK_ARG)

            if not self._ExpectSymbol(',', optional=True):
                break
            self._NextToken()
            
        # Write close tag
        self._WriteXmlTag('</parameterList>\n')
                

    def _CompileSubroutineBody(self, subroutineName):
        """
        Compiles <subroutine-body> :=
            '{' <var-dec>* <statements> '}'

        The tokenizer is expected to be positioned before the {
        ENTRY: Tokenizer positioned on the initial '{'.
        EXIT:  Tokenizer positioned after final '}'.
        """
        self._WriteXmlTag('<subroutineBody>\n')
        
        self._ExpectSymbol('{')
        self._NextToken()

        while self._ExpectKeyword(KW_VAR, optional=True, lookahead=True):
            self._CompileVarDec()

        nLocals = self.symbolTable.VarCount(SYMK_VAR)
        self.vmWriter.WriteFunction(subroutineName, nLocals)

        self._CompileStatements()

        self._ExpectSymbol('}')
        self._NextToken()
        
        self._WriteXmlTag('</subroutineBody>\n')


    def _CompileVarDec(self):
        """
        Compiles <var-dec> :=
            'var' <type> <var-name> (',' <var-name>)* ';'

        ENTRY: Tokenizer positioned on the initial 'var'.
        EXIT:  Tokenizer positioned after final ';'.
        """
        # Write open tag
        self._WriteXmlTag('<varDec>\n')
        
        storageClass = self._ExpectKeyword(KW_VAR)
        self._NextToken()
        
        if self._ExpectKeyword((KW_INT, KW_CHAR, KW_BOOLEAN), optional=True):
            variableType = self.tokenizer.KeywordStr()
        else:
            variableType = self._ExpectIdentifier()
        self._NextToken()

        while True:
            variableName = self._ExpectIdentifier()
            self._NextToken()
            self._DefineSymbol(variableName, variableType, SYMK_VAR)
            if not self._ExpectSymbol(',', optional=True):
                break
            self._NextToken()

        self._ExpectSymbol(';')
        self._NextToken()
    
        self._WriteXmlTag('</varDec>\n')


    def _CompileStatements(self):
        """
        Compiles <statements> := (<let-statement> | <if-statement> |
            <while-statement> | <do-statement> | <return-statement>)*

        The tokenizer is expected to be positioned on the first statement
        ENTRY: Tokenizer positioned on the first statement.
        EXIT:  Tokenizer positioned after final statement.
        """
        self._WriteXmlTag('<statements>\n')

        kw = self._ExpectKeyword((KW_DO, KW_IF, KW_LET, KW_RETURN, KW_WHILE), lookahead=True)
        while kw:
            if kw == KW_DO:
                self._CompileDo()
            elif kw == KW_IF:
                self._CompileIf()
            elif kw == KW_LET:
                self._CompileLet()
            elif kw == KW_RETURN:
                self._CompileReturn()
            elif kw == KW_WHILE:
                self._CompileWhile()
            kw = self._ExpectKeyword((KW_DO, KW_IF, KW_LET, KW_RETURN, KW_WHILE), lookahead=True, optional=True)
            
        self._WriteXmlTag('</statements>\n')


    def _CompileLet(self):
        """
        Compiles <let-statement> :=
            'let' <var-name> ('[' <expression> ']')? '=' <expression> ';'

        ENTRY: Tokenizer positioned on the first keyword.
        EXIT:  Tokenizer positioned after final ';'.
        """
        self._WriteXmlTag('<letStatement>\n')
        self._ExpectKeyword(KW_LET)
        self._NextToken()

        varName = self._ExpectIdentifier();
        self._NextToken()

        self._WriteSymbol(varName, assign=True)

        if self._ExpectSymbol('[', optional=True):
            self._NextToken()
            self._CompileExpression()
            self._ExpectSymbol(']')
            self._NextToken()

        self._ExpectSymbol('=')
        self._NextToken()

        self._CompileExpression();

        if kind == SYMK_VAR:
            self.vmWriter.WritePop('local', index)
        elif kind == SYMK_ARG:
            self.vmWriter.WritePop('argument', index)

        self._ExpectSymbol(';')
        self._NextToken()

        self._WriteXmlTag('</letStatement>\n')


    def _CompileDo(self):
        """
        Compiles <do-statement> := 'do' <subroutine-call> ';'
        
        <subroutine-call> := (<subroutine-name> '(' <expression-list> ')') |
            ((<class-name> | <var-name>) '.' <subroutine-name> '('
            <expression-list> ')')

        <*-name> := <identifier>

        ENTRY: Tokenizer positioned on the first keyword.
        EXIT:  Tokenizer positioned after final ';'.
        """
        self._WriteXmlTag('<doStatement>\n')

        self._ExpectKeyword(KW_DO)
        self._NextToken()

        self._CompileCall()

        self._ExpectSymbol(';')
        self._NextToken()

        self._WriteXmlTag('</doStatement>\n')


    def _CompileCall(self, subroutineName=None):
        """
        <subroutine-call> := (<subroutine-name> '(' <expression-list> ')') |
            ((<class-name> | <var-name>) '.' <subroutine-name> '('
            <expression-list> ')')

        <*-name> := <identifier>

        ENTRY: Tokenizer positioned on the first identifier.
            If 'objectName' is supplied, tokenizer is on the '.'
        EXIT:  Tokenizer positioned after final ';'.
        """
        objectName = None
        if subroutineName == None:
            subroutineName = self._ExpectIdentifier()
            self._NextToken()
        
        sym = self._ExpectSymbol('.(')
        self._NextToken()
        
        if sym == '.':
            objectName = subroutineName
            subroutineName = self._ExpectIdentifier()
            self._NextToken()
            sym = self._ExpectSymbol('(')
            self._NextToken()

        nArgs = 0
        className = self.symbolTable.TypeOf(objectName)
        if not className:
            # This is a function
            className = objectName
        else:
            # This is a method
            kind = self.symbolTable.KindOf(objectName)
            index = self.symbolTable.IndexOf(objectName)
            
        nArgs += self._CompileExpressionList()
            
        self.vmWriter.WriteCall(className + '.' + subroutineName, nArgs)
        
        self._ExpectSymbol(')')
        self._NextToken()
        

    def _CompileReturn(self):
        """
        Compiles <return-statement> :=
            'return' <expression>? ';'

        ENTRY: Tokenizer positioned on the first keyword.
        EXIT:  Tokenizer positioned after final ';'.
        """
        self._WriteXmlTag('<returnStatement>\n')

        self._ExpectKeyword(KW_RETURN);
        self._NextToken();

        if not self._ExpectSymbol(';', optional=True):
            self._CompileExpression()
            self._ExpectSymbol(';')
        else:
            self.vmWriter.WritePush('constant', 0)
        self._NextToken()

        self.vmWriter.WriteReturn()

        self._WriteXmlTag('</returnStatement>\n')

    def _GetNextLabel(self):
        """
        Get a label that is unique within this subroutine.
        """
        self.labelCounter += 1
        return 'L' + str(self.labelCounter)

    def _CompileIf(self):
        """
        Compiles <if-statement> :=
            'if' '(' <expression> ')' '{' <statements> '}' ( 'else'
            '{' <statements> '}' )?

        ENTRY: Tokenizer positioned on the first keyword.
        EXIT:  Tokenizer positioned after final '}'.
        """
        self._WriteXmlTag('<ifStatement>\n')
        label1 = self._GetNextLabel()
        label2 = self._GetNextLabel()

        self._ExpectKeyword(KW_IF)
        self._NextToken()

        self._ExpectSymbol('(')
        self._NextToken()

        self._CompileExpression()
        self._CompileArithmetic('~')
        self.vmWriter.WriteIf(label1)

        self._ExpectSymbol(')')
        self._NextToken()

        self._ExpectSymbol('{')
        self._NextToken()

        self._CompileStatements()

        self._ExpectSymbol('}')
        self._NextToken()

        self.vmWriter.WriteGoto(label2)
        self.vmWriter.WriteLabel(label1)

        if self._ExpectKeyword(KW_ELSE, optional=True):
            self._NextToken()

            self._ExpectSymbol('{')
            self._NextToken()

            self._CompileStatements()

            self._ExpectSymbol('}')
            self._NextToken()
        
        self.vmWriter.WriteLabel(label2)
        self._WriteXmlTag('</ifStatement>\n')


    def _CompileWhile(self):
        """
        Compiles <while-statement> :=
            'while' '(' <expression> ')' '{' <statements> '}'

        ENTRY: Tokenizer positioned on the first keyword.
        EXIT:  Tokenizer positioned after final '}'.
        """
        self._WriteXmlTag('<whileStatement>\n')
        label1 = self._GetNextLabel()
        label2 = self._GetNextLabel()

        self._ExpectKeyword(KW_WHILE)
        self._NextToken()

        self._ExpectSymbol('(')
        self._NextToken()

        self.vmWriter.WriteLabel(label1)
        self._CompileExpression()
        self._CompileArithmetic('~')
        self.vmWriter.WriteIf(label2)

        self._ExpectSymbol(')')
        self._NextToken()

        self._ExpectSymbol('{')
        self._NextToken()

        self._CompileStatements()
        self.vmWriter.WriteGoto(label1)

        self._ExpectSymbol('}')
        self.vmWriter.WriteLabel(label2)
        self._NextToken()

        self._WriteXmlTag('</whileStatement>\n')


    def _CompileExpression(self):
        """
        Compiles <expression> :=
            <term> (op <term)*

        The tokenizer is expected to be positioned on the expression.
        ENTRY: Tokenizer positioned on the expression.
        EXIT:  Tokenizer positioned after the expression.
        """
        self._WriteXmlTag('<expression>\n')

        self._CompileTerm()
        
        while self._ExpectSymbol("+-*/&|<>=", optional=True):
            op = self.tokenizer.Symbol()
            self._NextToken()
            self._CompileTerm()
            self._CompileArithmetic(op)

        self._WriteXmlTag('</expression>\n')

    def _CompileArithmetic(self, op):
        """
        Writes VM code for the given operation.
        """
        if op == '*':
            self.vmWriter.WriteCall('Math.multiply', 2)
        elif op == '/':
            self.vmWriter.WriteCall('Math.divide', 2)
        else:
            self.vmWriter.WriteArithmetic("+&=><-~|-".find(op))

    def _CompileTerm(self):
        """
        Compiles a <term> :=
            <int-const> | <string-const> | <keyword-const> | <var-name> |
            (<var-name> '[' <expression> ']') | <subroutine-call> |
            ( '(' <expression> ')' ) | (<unary-op> <term>)

        ENTRY: Tokenizer positioned on the term.
        EXIT:  Tokenizer positioned after the term.
        """
        self._WriteXmlTag('<term>\n')

        if self._ExpectConstant(optional=True):
            # Constant value
            if self.tokenizer.TokenType() == TK_INT_CONST:
                self.vmWriter.WritePush('constant', self.tokenizer.IntVal())
            elif self.tokenizer.Keyword() == KW_FALSE:
                self.vmWriter.WritePush('constant', 0)
            elif self.tokenizer.Keyword() == KW_TRUE:
                self.vmWriter.WritePush('constant', 1)
                self._CompileArithmetic('-')
            self._NextToken()
        elif self._ExpectSymbol('(', optional=True):
            # Nested expression
            self._NextToken()
            self._CompileExpression()
            self._ExpectSymbol(')')
            self._NextToken()
        elif self._ExpectSymbol('-~', optional=True):
            # Unary operation
            op = self.tokenizer.Symbol()
            self._NextToken()
            self._CompileTerm()
            self._CompileArithmetic(op)
        else:
            ident = self._ExpectIdentifier(optional=True)
            self._NextToken()
            if self._ExpectSymbol('.(', lookahead=True, optional=True):
                # Subroutine call
                self._CompileCall(ident)
            else:
                # Variable
                self._WriteSymbol(ident, assign=False)
                if self._ExpectSymbol('[', optional=True):
                    # Array access
                    self._NextToken()
                    self._CompileExpression()
                    self._ExpectSymbol(']')
                    self._NextToken()

        self._WriteXmlTag('</term>\n')


    def _CompileExpressionList(self):
        """
        Compiles <expression-list> :=
            (<expression> (',' <expression>)* )?

        Returns number of expressions compiled.

        ENTRY: Tokenizer positioned on the first expression.
        EXIT:  Tokenizer positioned after the last expression.
        """
        self._WriteXmlTag('<expressionList>\n')

        count = 0
        while True:
            if self._ExpectSymbol(')', lookahead=True, optional=True):
                break
            self._CompileExpression()
            count += 1

            if not self._ExpectSymbol(',', optional=True):
                break
            self._NextToken()
        
        self._WriteXmlTag('</expressionList>\n')
        return count


    def _ExpectKeyword(self, keywords, lookahead=False, optional=False):
        """
        Parse the next token.  It is expected to be one of 'keywords'.
        'keywords' may be a keywordID or a tuple of keywordIDs.

        Unless the lookahead flag is set, the symbol will be written to the XML file.

        If an expected keyword is parsed, returns the keyword.
        If no keyword is parsed and the optional flag is set, returns False.
        Otherwise raises an error.
        """
        if not self.tokenizer.TokenType() == TK_KEYWORD:
            if optional:
                return False
            self._RaiseError('Expected '+self._KeywordStr(keywords)+', got '+
                             self.tokenizer.TokenTypeStr())
        if type(keywords) != tuple:
            keywords = (keywords,)
        if self.tokenizer.Keyword() in keywords:
            if not lookahead: 
                self._WriteXml('keyword', self.tokenizer.KeywordStr())
            return self.tokenizer.Keyword()
        if optional:
            return False
        self._RaiseError('Expected '+self._KeywordStr(keywords)+', got '+
                         self._KeywordStr(self.tokenizer.Keyword()))


    def _ExpectIdentifier(self, lookahead=False, optional=False):
        """
        Parse the next token.  It is expected to be an identifier.

        Unless the lookahead flag is set, the symbol will be written to the XML file.

        Returns the identifier parsed or raises an error.
        """
        if not self.tokenizer.TokenType() == TK_IDENTIFIER:
            if optional:
               return False
            self._RaiseError('Expected <identifier>, got '+
                             self.tokenizer.TokenTypeStr())
        if not lookahead: 
            self._WriteXml('identifier', self.tokenizer.Identifier())
        return self.tokenizer.Identifier()
        

    def _ExpectSymbol(self, symbols, lookahead=False, optional=False):
        """
        Parse the next token.  It is expected to be one of 'symbols'.
        'symbols' is a string of one or more legal symbols.

        Unless the lookahead flag is set, the symbol will be written to the XML file.

        If an expected symbol is parsed, returns the symbol.
        If no such symbol is parsed and the optional flag is set, returns False.
        Otherwise raises an error.
        """
        if not self.tokenizer.TokenType() == TK_SYMBOL:
            if optional: 
                return False
            self._RaiseError('Expected '+self._SymbolStr(symbols)+', got '+
                             self.tokenizer.TokenTypeStr())
        if self.tokenizer.Symbol() in symbols:
            if not lookahead:
                self._WriteXml('symbol', self.tokenizer.Symbol())
            return self.tokenizer.Symbol()
        if optional:
            return False
        self._RaiseError('Expected '+self._SymbolStr(symbols)+', got '+
                         self._SymbolStr(self.tokenizer.Symbol()))


    def _ExpectConstant(self, lookahead=False, optional=False):
        """
        Parse the next token.  It is expected to be one of TK_INT_CONST, 
        TK_STRING_CONST, KW_FALSE, KW_NULL, KW_THIS, or KW_TRUE.

        Unless the lookahead flag is set, the symbol will be written to the XML file.

        If an expected token is parsed, returns True.
        If no such token is parsed and the optional flag is set, returns False.
        Otherwise raises an error.
        """
        if self.tokenizer.TokenType() == TK_INT_CONST:
            self._WriteXml('integerConstant', str(self.tokenizer.IntVal()))
            return True
        elif self.tokenizer.TokenType() == TK_STRING_CONST:
            self._WriteXml('stringConstant', self.tokenizer.StringVal())
            return True
        elif self._ExpectKeyword((KW_FALSE, KW_NULL, KW_THIS, KW_TRUE), optional=True):
            return True
        if optional:
            return False
        self._RaiseError('Expected a constant, got ' + self.tokenizer.TokenTypeStr())
        

    def _RaiseError(self, error):
        message = '%s line %d:\n  %s\n  %s' % (
                  self.inputFileName, self.tokenizer.LineNumber(),
                  self.tokenizer.LineStr(), error)
        raise HjcError(message)
        

    def _KeywordStr(self, keywords):
        if type(keywords) != tuple:
            return '"' + self.tokenizer.KeywordStr(keywords) + '"'
        ret = ''
        for kw in keywords:
            if len(ret):
                ret += ', '
            ret += '"' + self.tokenizer.KeywordStr(kw) + '"'
        if len(keywords) > 1:
            ret = 'one of (' + ret + ')'
        return ret
        
        
    def _SymbolStr(self, symbols):
        if type(symbols) != tuple:
            return '"' + symbols + '"'
        ret = ''
        for symbol in symbols:
            if len(ret):
                ret += ', '
            ret += '"' + symbol + '"'
        if len(symbols) > 1:
            ret = 'one of (' + ret + ')'
        return ret
        
        
    def _NextToken(self):
        if not self.tokenizer.Advance():
            self._RaiseError('Premature EOF')

    
    def _WriteXmlTag(self, tag):
        if xml:
            if tag[1] == '/':
                self.xmlIndent -= 1
            self.xmlOutputFile.Write('  ' * self.xmlIndent)
            self.xmlOutputFile.Write(tag)
            if '/' not in tag:
                self.xmlIndent += 1


    def _WriteXml(self, tag, value):
        if xml:
            self.xmlOutputFile.Write('  ' * self.xmlIndent)
            self.xmlOutputFile.WriteXml(tag, value)


    def _DefineSymbol(self, name, type, kind):
        """
        Adds a new symbol to the symbol table.
        """
        self.symbolTable.Define(name, type, kind)


    def _LookupSymbol(self, name):
        """
        Returns a tuple (type, kind, index)
        """
        return (self.symbolTable.TypeOf(name), 
                self.symbolTable.KindOf(name),
                self.symbolTable.IndexOf(name))


    def _WriteSymbol(self, name, assign=False):
        """
        Writes an XML tag for a symbol table entry.
        """
        type, kind, index = self._LookupSymbol(name)
        self._WriteXmlTag('<tableEntry assign="%s", "type="%s" kind="%s" index="%s"/>\n' % (assign, type, kind, index))
        if type is SYMK_STATIC:
            pass
        elif type is SYMK_FIELD:
            pass
        elif type is SYMK_ARG:
            segment = 'argument'
        elif type is SYMK_VAR:
            segment = 'local'
        if assign:
            self.vmWriter.WritePop(segment, index)
        else:
            self.vmWriter.WritePush(segment, index)

    def _WriteBinaryOperation(self, symbol):
        """
        Translates a symbol to the corresopnding opcode.
        """
