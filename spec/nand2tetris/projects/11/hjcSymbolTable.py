"""
hjcSymbolTable.py -- SymbolTable class for Hack computer Jack compiler
Solution provided by Nand2Tetris authors, licensed for educational purposes
Refactored by Janet Davis, April 25, 2016
"""

from hjcError import *

SYMK_STATIC = 0     # Symbol 'kinds' -- also indices for self.count[]
SYMK_FIELD  = 1
SYMK_ARG    = 2
SYMK_VAR    = 3

SYMI_TYPE   = 0     # Indices for symbol data tuple
SYMI_KIND   = 1
SYMI_INDEX  = 2


class SymbolTable(object):

    class Entry(object):
        def __init__(self, type, kind, index):
            self.type = type
            self.kind = kind
            self.index = index

    def __init__(self):
        """
        Create a new empty symbol table.
        """
        self.classSymbols = {}
        self.subroutineSymbols = {}
        self.count = [0, 0, 0, 0] # counts for declarations of kind static, field, arg, var


    def StartSubroutine(self):
        """
        Starts a new subroutine scope.
        """
        self.subroutineSymbols = {}
        self.count[SYMK_ARG] = 0
        self.count[SYMK_VAR] = 0
        

    def Define(self, name, symType, symKind):
        """
        Define a new identifier of a given 'name', 'symType' and 'symKind'.
        'symType' is a builtin type name or a class name.
        'symKind' is SYMK_STATIC, SYMK_FIELD, SYMK_ARG or SYMK_VAR.
        """
        table = self._SelectTable(symKind)
        if name in table:
            message = 'SymbolTable.Define: symbol "%s" already defined' % name
            FatalError(message)
        table[name] = SymbolTable.Entry(symType, symKind, self.count[symKind])
        self.count[symKind] += 1

        
    def _SelectTable(self, symKind):
        """
        Internal routine to select either the class symbol table or the
        subroutine symbol table.
        """
        if symKind in (SYMK_STATIC, SYMK_FIELD):
            return self.classSymbols
        elif symKind in (SYMK_ARG, SYMK_VAR):
            return self.subroutineSymbols
        else:
            message = 'SymbolTable.Define: unknown symKind (%d)' % symKind
            FatalError(message)
        

    def VarCount(self, symKind):
        """
        Return the number of variables of the given 'symKind' already
        defined in the current scope.
        """
        if symKind not in (SYMK_STATIC, SYMK_FIELD, SYMK_ARG, SYMK_VAR):
            message = 'SymbolTable.Define: unknown symKind (%d)' % symKind
            FatalError(message)
        return self.count[symKind]


    def KindOf(self, name):
        """
        Return the 'kind' of identifier 'name' in the current scope.
        If the identifier is unknown in the current scope, returns None.
        """
        return self._ValueOf(name, 'kind')


    def KindOfStr(self, name):
        return ('static','field','arg','var')[self.KindOf(name)]


    def TypeOf(self, name):
        """
        Return the 'type' of identifier 'name' in the current scope.
        If the identifier is unknown in the current scope, returns None.
        """
        return self._ValueOf(name, 'type')


    def IndexOf(self, name):
        """
        Return the 'index' of identifier 'name' in the current scope.
        If the identifier is unknown in the current scope, returns None.
        """
        return self._ValueOf(name, 'index')


    def _ValueOf(self, name, typeKindOrIndex):
        """
        Inernal routine to return a selected value from a symbol.
        """
        if name in self.subroutineSymbols:
            return getattr(self.subroutineSymbols[name], typeKindOrIndex)
        if name in self.classSymbols:
            return getattr(self.classSymbols[name], typeKindOrIndex)
        return None
    
        
    def ScopeOf(self, name):
        """
        Return the scope(s) where identifier 'name' is found.
        """
        scope = ''
        if name in self.subroutineSymbols:
            scope = 'subroutine'
        if name in self.classSymbols:
            if scope:
                scope += '+'
            scope += 'class'
        if not scope:
            scope = 'None'
        return scope


