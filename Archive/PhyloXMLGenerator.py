from lxml import etree

def buildXml():
    root = etree.Element("root", interesting="totally")
    root.append( etree.Element("child1") )

    etree.SubElement(root, "child").text = "Child 1"
    etree.SubElement(root, "child").text = "Child 2"
    etree.SubElement(root, "another").text = "Child 3"

    #    root.insert(0, etree.Element("Child0"))
    child2 = root[1]


    etree.SubElement(child2, "Child0ofchild2").text = "HelloWorld"
    child0ofChild2 = child2[0]

    etree.SubElement(root, "Inbrackets").text = "Here we go"

    anotherElement = etree.Element("AppedTest")
    anotherElement.text = "Another Text"
    root[1][0].append(anotherElement)

    #    root.text = "TEXT"

    for child in root:
        print child.tag

    print etree.tostring(root, pretty_print=True)

# creates a folder clade and adds it to the passed it parent
def addFolderClade(parent, foldername, uri="", tooltip=""):
    pass

