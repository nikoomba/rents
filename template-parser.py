filey = open('test-parser.html','r')

class Document:
    def __init__(self, filename):
        self.filename = filename
        self.contents = open(filename,'r')
    def lines(self):
        """ list the lines in a document """
        l = []
        for line in self.contents:
            l.append(line)
        return l
    def words(self):
        """list the words in a document"""
        w = []
        for line in self.contents:
            for word in line.split():
                w.append(word)
        return w
    def variables(self):
        """ list all of the variables in a document"""
        v = []
        for line in self.contents:
            for word in line.split():
                if word[0]=='$':
                    v.append(word)
        return v
"""    def replaceVariable(self,variable,replacement):
        for line in self.contents:
            for word in line.split():
                if word == variable:
                    line
   """     

test = Document('test-parser.html')



