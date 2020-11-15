# Source code modified from @tremlab: https://github.com/tremlab/morseCodeTranslator
# a python module that builds a populated binary tree for morse code values, with a method to easily translate a morse code string to its letter.

class Morse_Code_Bin_Tree(object):
    def __init__(self):
        """
        Summary: Class that initializes and populates a binary tree for translating morse code strings into letters.
        """

        self.head = Node("*")
        letters = "ETIANMSURWDKGOHVF*L*PJBXCYZQ**54*3***2**+****16=/*****7***8*90"
        current = self.head
        nexts = []
        # populate tree
        for char in letters:
            if current.left == None:
                current.left = Node(char)
            else:
                if current.right == None:
                    current.right = Node(char)
                else:
                    nexts.append(current.left)
                    nexts.append(current.right)
                    current = nexts.pop(0)
                    current.left = Node(char)

    def translate_mc_to_letter(self, mc_ltr_str):
        """
        Summary: translates string of morse code into a corresponding letter/number
        Args:
            mc_ltr_str (string): string containing morse code with "." and "-"
        """
        if mc_ltr_str == "":
            return ""
        current = self.head
        try:
            for char in mc_ltr_str:
                if char == ".":
                    current = current.left
                else:
                    current = current.right

            return current.val
        except AttributeError:
            print("No such letter exists")


class Node(object):
    """
    Summary: class that represents a node in the binary tree
    """
    def __init__(self, char):
        self.val = char
        self.left = None
        self.right = None