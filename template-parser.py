class Template:
    """Class of objects that define a number of operations to perform on a Template (specified when object is initialised) to generate an output """
    """FUTURE CHANGE SUGGESTIONS: Get rid of lines / words methods. Make variables specified by '$' and uppercase, so we don't need to include spaces either side."""    
    """ This whole class could probably be deleted in favor of some simple function defintion."""
    def __init__(self, template):
        self.template = template
        self.contents = open(template,'r')
        self.data = self.docData()
        
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
    def docData(self):
        """store the document in some datastructure. This runs only once on initializing the class"""
        lines = []
        for line in self.contents:
            words = []
            for word in line.split():
                words.append(word)
            lines.append(words)
        return lines
    def replaceVariable(self,variable,replacement):
        """Replace all occurences of a variable in a document with the string 'replacement'"""
        for line in self.data:
            for word in line:
                if word == variable:
                    line.insert(line.index(variable),replacement)
                    line.remove(variable)
    def replaceList(self,replacement_list):
        """A replacement list is a list of variables along with what they should be replaced with as tuples"""
        """    Example: example_replacement_list = [['$variable1', 'replacement1'],['$variable2','replacement2']] """
        for replacement in replacement_list:
            self.replaceVariable(replacement[0],replacement[1])
    def outputDoc(self, outputname):
        """ This method returns the document datastructure as a string formated as HTML. 'outputname' is the name of the file to output to"""
        output = open(outputname, 'a')
        for line in self.data:
            lineout = ""
            for word in line:
                lineout=lineout+word 
            output.write(lineout + '\n')
