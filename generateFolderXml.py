import lxml

__author__ = 'Tomithy'

# Written for demostration purposes for GSOC 2012

# This script uses the schema defined by PhyloXML which is available at http://www.phyloxml.org/

# Suggested improvements:
    # 1. Use a dict to store and retrieve ancestor instead of the current recursive functions
    # 2. Change the generate clade method to have no side effects in lieu of the FP style, easier testing?

import os
import sys
from lxml import etree

rootdir = os.getcwd() + "/Galaxy_scripts"      #"directory which is rendered to PhyloXML"


OUTFILE_NAME = "scripts.xml"
BRANCH_LENGTH = 5.0 #determines how far/how deep each directory is

def buildDirXml():

    print rootdir
    rootString = "/".join(rootdir.split("/")[:-1])

    phyloroot = buildGenericPhyloXMLStructure()
    claderoot = phyloroot[1]

    folderCount = 0     #folder stats
    fileList = []
    fileSize = 0

    for folderDir, subFolders, files in os.walk(rootdir):

        folderCount += len(subFolders)
        parentNode = getFolderParentNode(claderoot, rootString, folderDir)

        folderName = folderDir.split("/")[-1]

        #generating 2 nodes over here because we need one to serve as internal node, with names, and the other to display to the user on the phylogeny tree
        folderInternalNode = generateClade(parentNode, folderName)
        folderActualNode = generateClade(folderInternalNode, "Folder:" + folderName, tooltip="Folder has no filesize" )

        for file in files:

            if file == ".DS_Store":
                continue
            if file [-3:] == ".py":
                componentType = "python"
            elif file [-3:] == ".sh":
                componentType = "bash"
            else:
                componentType = "others"
            f = os.path.join(folderDir,file)
            fileSize = fileSize + os.path.getsize(f)
            fileSize = float(fileSize) / 1024
            tooltipFS = "Filesize: " + str(fileSize) + " kb"
            fileNode = generateClade(folderInternalNode, file, chartIntensity=fileSize, componentType=componentType,tooltip=tooltipFS )

            fileList.append(f)
            print file


    print etree.tostring(phyloroot, pretty_print=True)

    xmlOutFile = open (OUTFILE_NAME, "wt")

    xmlOutString = etree.tostring(phyloroot)
    xmlOutString = addPhyloXMLroot(xmlOutString)

    print xmlOutString
    xmlOutFile.write(xmlOutString)
    xmlOutFile.close()

    print("Total Size is {0} bytes".format(fileSize))
    print("Total Files" , len(fileList))
    print("Total Folders ", folderCount)


# Important: we are guranteed that parent would be created before child, because os.walk's default is walking from top-down
def getFolderParentNode(phyloRoot, rootString, folderDir):
    parentNode = phyloRoot
    relativePath = folderDir[len(rootString) + 1:]  # using the same property that all subfolders
    parentNodeTagXPathTextList = relativePath.split("/")[:-1]
#    print parentNodeTagXPathTextList
    for text in parentNodeTagXPathTextList:
        XpathExpression = 'clade/name[text()="' + text + '"]/..'
#        print XpathExpression
        parentNodeList = parentNode.xpath(XpathExpression)
#        print "Parent Node list", parentNodeList
        if len(parentNodeList) != 0 :
            parentNode = parentNodeList[0]
    return parentNode



def addPhyloXMLroot(xmlString):
    #remove newline from xmlString
    xmlString = '<phyloxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.phyloxml.org http://www.phyloxml.org/1.10/phyloxml.xsd" xmlns="http://www.phyloxml.org">' + xmlString + "</phyloxml>"
    return xmlString

def buildGenericPhyloXMLStructure(rooted="false"):

    root = etree.Element("phylogeny", rooted=rooted)        # We use the unique child as root first since the true root contains attribute that cannot be added by lxml
    root = addRenderAttributes(root)
    etree.SubElement(root, "clade")

    return root



def addRenderAttributes(root):

    render = etree.SubElement(root, "render")

    parameters = etree.SubElement(render, "parameters") # now we add parameters to it
    circular = etree.SubElement(parameters, "circular")
    bufferRadius = etree.SubElement(circular, "bufferRadius")
    bufferRadius.text = "0.5"

    rectangular = etree.SubElement(parameters, "rectangular")
    alignRight = etree.SubElement(rectangular, "alignRight")
    alignRight.text = "1"
    bufferX = etree.SubElement(rectangular, "bufferX")
    bufferX.text = "300"

    charts = etree.SubElement(render, "charts") #Adding chart display options
    component = etree.SubElement(charts, "content", type="bar", fill="#666", width="0.2")
    component = etree.SubElement(charts, "component", type="binary", thickness="10")



    styles = etree.SubElement(render, "styles") # Adding Styles
    styles.append (generateStyle("bash", "#6633FF", "#DDD"))
    styles.append (generateStyle("python", "#FF6600", "#DDD"))   #to highligh python code
    styles.append (generateStyle("others", "#d7e3bc", "#DDD"))   #to highligh others
    etree.SubElement(styles, "barChart", fill='#000')

    return root


def generateStyle( tag="", fill="#000", stroke="#FFF"):
    style = etree.Element(tag, fill=fill, stroke=stroke )
    print style
    return style

def generateClade(parent, name="", branchLen=BRANCH_LENGTH, tooltip="", uri="", componentType=None, bg="", chartIntensity=0 ):

    node = etree.SubElement(parent, "clade")

    if name is not "":
        nameNode = etree.SubElement(node, "name")
        nameNode.text = name
        nameNode.set("bgStyle", bg)

    branchLenNode = etree.SubElement(node, "branch_length")
    branchLenNode.text = str(branchLen)

    #adding annotation
    annotationNode = etree.SubElement(node, "annotation")
    descNode = etree.SubElement(annotationNode, "desc")
    descNode.text = tooltip
#    uriNode = etree.SubElement(annotationNode, "uri")
#    uriNode.text = uri


    chart = etree.SubElement(node, "chart")
    content = etree.SubElement(chart, "content")
    content.text = str(chartIntensity)
    component = etree.SubElement(chart, "component")
    component.text = componentType

    return node



if __name__ == '__main__':
#    buildXml()
    buildDirXml()