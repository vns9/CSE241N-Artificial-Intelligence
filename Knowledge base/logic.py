"""
logic.py: Python file defining the logic classes, objects, and functions.
"""


from functools import reduce


class Formula(object):
    """
    Base class for all the objects that will make up a 'Propositional formula'.
    """

    def __eq__(self, other):
        """
        Compare two formulas for equality.
        """

        raise NotImplemented

    def __str__(self):
        """
        Represent the formula as a human readable string.
        """

        raise NotImplemented

    def __repr__(self):
        """
        Represent the formula as in object form.
        """

        return NotImplemented

    def getAtoms(self):
        """
        Returns a set of atoms (unique prepositions) used in this formula.
        """

        raise NotImplemented

    def toCNF(self):
        """
        Convert the formula into conjunctive normal form.
        """

        raise NotImplemented

    def truthValue(self, truthDict):
        """
        Find the value of the expression given the truth values
        in the dictionary truthDict.
        """

        raise NotImplemented


class Atom(Formula):
    """
    Atom is the basic unit of propositional logic. It is usually represented as
    a single capital latin alphabet. Eg. 'P' is a proposition. Of course, we can have
    more complex propositions, like 'Rain' or 'Ram is a good boy'.
    """

    def __init__(self, name):
        if isinstance(name, str):
            self.name = name
        else:
            raise ValueError('Atom is not a string.')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Atom(' + self.name.__repr__() + ')'

    def __hash__(self):
        """
        Hash functions so that atoms can be put into sets.
        """
        return hash(self.__repr__())

    def __eq__(self, other):
        """
        Two atoms are equal if their letters are equal.
        """
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False

    def getAtoms(self):
        if self.name != 'True' and self.name != 'False':
            return {self.name}
        else:
            return set()

    def toCNF(self):

        # BEGIN CODE HERE #

        # Return the CNF form of an elementary proposition/atom

        return Atom(self.__str__())

        # END YOUR CODE HERE #

    def truthValue(self, truthDict):

        # BEGIN YOUR CODE #

        # Return the truth value of the proposition.
        # truthDict is a dictionary containing truth
        # values. For Eg, if the proposition is P, then
        # truthDict['P'] may be True.
        #
        # Check the special cases when the value of the
        # proposition might be a constant, i.e Atom('True')
        # should always return True, similarly for False.

        if self.name == 'True':
            return True
        elif self.name == 'False':
            return False
        else:
            return truthDict[self.name]

        # END YOUR CODE #


TrueConstant = Atom('True')
FalseConstant = Atom('False')


class BinaryFormula(Formula):
    """
    A base class for a binary formula like Or or And.
    """

    def __init__(self, arg1, arg2):
        if isinstance(arg1, Formula) and isinstance(arg2, Formula):
            self.arg1, self.arg2 = arg1, arg2
        else:
            raise ValueError('Arguments are not formulas.')

    def __eq__(self, other):
        """
        A binary formula like (A ^ B) or (A v B) is equal to another binary
        formula if the two arguments are pairwise equal.
        """

        if isinstance(other, self.__class__):
            return (self.arg1 == other.arg1 and self.arg2 == other.arg2) \
                or (self.arg1 == other.arg2 and self.arg2 == other.arg1)
        else:
            return False

    def getAtoms(self):
        return self.arg1.getAtoms().union(self.arg2.getAtoms())

    def flattenArgs(self):
        """
        Flatten a binary formula and return the list of arguments. For example,
        Or(A, Or(B, Or(C, D))) would be flattened into the list [A, B, C, D].
        """

        flattenList = [self.arg1, self.arg2]
        currIndex = 0

        while currIndex < len(flattenList):
            if isinstance(flattenList[currIndex], self.__class__):
                flattenList += [flattenList[currIndex].arg1, flattenList[currIndex].arg2]
                flattenList.pop(currIndex)
            else:
                currIndex += 1

        return flattenList

    @classmethod
    def fromList(cls, args):
        """
        Reverse of flatten. From a list [A, B, C, D] create a expression like
        Or(A, Or(B, Or(C, D))).
        (cls.fromList(obj.flattenArgs()) == obj) should be True for all objects
        of both classes And and Or.
        """

        if len(args) == 0:
            return Atom('False')

        allFormulas = reduce(lambda x, y: x and y, map(lambda x: isinstance(x, Formula), args))

        if allFormulas:
            if len(args) == 0:
                raise ValueError('Empty list for conjunction.')
            elif len(args) == 1:
                return args[0]
            else:
                toReturn = args[-1]

                for i in range(len(args) - 2, -1, -1):
                    toReturn = cls(args[i], toReturn)

                return toReturn


class And(BinaryFormula):
    """
    Logical and of two formulas.
    """

    def __str__(self):
        return '(' + reduce(lambda x, y: x + ' ^ ' + y,
                            map(lambda x: x.__str__(), self.flattenArgs())) + ')'

    def __repr__(self):
        return 'And(' + self.arg1.__repr__() + ', ' + self.arg2.__repr__() + ')'

    def toCNF(self):
        # Convert arguments into CNF form.
        temp1 = self.arg1.toCNF()
        temp2 = self.arg2.toCNF()

        # BEGIN YOUR CODE HERE #

        # Special edge cases and simplification
        # Modify the return statements to return the
        # correct value for the given cases

        if temp1 == FalseConstant or temp2 == FalseConstant:
            return Atom('False')
        elif temp1 == TrueConstant:
            return temp2
        elif temp2 == TrueConstant:
            return temp1
        elif temp1 == temp2:
            return temp1

        # temp1 and temp2 contain formulas in CNF form.
        # Use those to calculate the CNF form of the expression
        # temp1 ^ temp2.
        #
        # Hint: Look at function BinaryFormula.flattenArgs() for help.
        #       You may take help from the PDF/Links sent via email.

        first = And(Atom('True'), temp1).flattenArgs()
        second = And(Atom('True'), temp2).flattenArgs()
        first.remove(Atom('True'))
        second.remove(Atom('True'))
        first = first + second 
        return And.fromList(first)

        # END YOUR CODE #

    def truthValue(self, truthDict):

        # BEGIN YOUR CODE #

        # Return the truth value of the And expression
        #
        # truthDict is a dictionary containing truth
        # values. For Eg, if the formula contains P, then
        # truthDict['P'] may be true.

        return self.arg1.truthValue(truthDict) * self.arg2.truthValue(truthDict)

        # END YOUR CODE #

class Or(BinaryFormula):
    """
    Logical or of two formulas.
    """

    def __str__(self):
        return '(' + reduce(lambda x, y: x + ' v ' + y,
                            map(lambda x: x.__str__(), self.flattenArgs())) + ')'

    def __repr__(self):
        return 'Or(' + self.arg1.__repr__() + ', ' + self.arg2.__repr__() + ')'

    def toCNF(self):
        # Convert args into CNF form.
        temp1 = self.arg1.toCNF()
        temp2 = self.arg2.toCNF()

        # BEGIN YOUR CODE #

        # Special edge cases and simplification.
        # Fill the return values corresponding to the condition
        if temp1 == TrueConstant or temp2 == TrueConstant:
            return Atom('True')
        elif temp1 == FalseConstant:
            return temp2
        elif temp2 == FalseConstant:
            return temp1
        elif temp1 == temp2:
            return temp1


        # temp1 and temp2 contain expression in CNF form.
        # Use those to find the CNF of temp1 v temp2.
        # Hint: Look at function BinaryFormula.flattenArgs().
        # (you may take help from the PDF sent via email)
        first = And(TrueConstant, temp1).flattenArgs()
        second = And(TrueConstant, temp2).flattenArgs()
        first.remove(TrueConstant)
        second.remove(TrueConstant)

        resultant = list()
        for i in range(len(first)):
            for j in range(len(second)):
                resultant.append(Or(first[i], second[j]))

        return And.fromList(resultant)

        # END YOUR CODE #

    def truthValue(self, truthDict):
        # BEGIN YOUR CODE #

        # Return the truth value of the Or expression.
        #
        # truthDict is a dictionary containing truth
        # values. For Eg, if the formula contains P, then
        # truthDict['P'] may be true.
        
        return self.arg1.truthValue(truthDict) or self.arg2.truthValue(truthDict)

        # END YOUR CODE #


class Not(Formula):
    """
    Logical negation of a formula.
    """

    def __init__(self, arg):
        if isinstance(arg, Formula):
            self.arg = arg
        else:
            print(arg)
            raise ValueError('Arguments are not formulas.')

    def __str__(self):
        return '~' + self.arg.__str__()

    def __repr__(self):
        return 'Not(' + self.arg.__repr__() + ')'

    def __hash__(self):
        if isinstance(self.arg, Atom):
            return hash(self.__repr__())
        else:
            raise ValueError('Only simple expressions can be hashed.')

    def __eq__(self, other):
        """
        A this formula is only equal if the other expression is a
        Not and the arg is equal.
        """

        if isinstance(other, self.__class__):
            return self.arg == other.arg
        else:
            return False

    def getAtoms(self):
        return self.arg.getAtoms()

    def toCNF(self):
        # BEGIN YOUR CODE #

        # For each case, fill in the correct expression,
        # Don't forget to call .toCNF() on the obtained expression.

        if self.arg == TrueConstant:
            return FalseConstant
        elif self.arg == FalseConstant:
            return TrueConstant
        elif isinstance(self.arg, Atom):
            return Not(self.arg)
        elif isinstance(self.arg, Not):
            return self.arg.arg.toCNF()
        elif isinstance(self.arg, And):
            return Or(Not(self.arg.arg1), Not(self.arg.arg2)).toCNF()
        elif isinstance(self.arg, Or):
            return And(Not(self.arg.arg1), Not(self.arg.arg2)).toCNF()
        else:
            raise ValueError('Unrecognised type of formula.')

        # END YOUR CODE #

    def truthValue(self, truthDict):
        # BEGIN YOUR CODE #

        # Return the truth value of the Not expression.
        #
        # truthDict is a dictionary containing truth
        # values. For Eg, if the proposition is P, then
        # truthDict['P'] may be True or False.

        return not self.arg.truthValue(truthDict)

        # END YOUR CODE #


def Equivalence(arg1, arg2):
    """
    A convenience funtion to represent an equivalence formula.
    """

    # BEGIN YOUR CODE #

    # Return the value of implies expression in terms of And, Or and Not
    return And(Implies(arg1, arg2),Implies(arg2, arg1))


    # END YOUR CODE #


def Implies(arg1, arg2):
    """
    A convenience function to implement a implies formula.
    """

    # BEGIN YOUR CODE #

    # Return the value of the equivalence expression in terms of And, Or and Not
    return Or(Not(arg1), arg2)

    # END YOUR CODE #