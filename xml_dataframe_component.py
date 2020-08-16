import xml.etree.ElementTree as et
import pandas as pd
import os


def xml_data_extract(filename):
    '''
    This function will take in a filename argument and parse any xml file that matches the filename passed in, if it lies in the given path.
    This function will utilize xml.etree.ElementTree module to parse the xml data, and pandas module to create a dataframe
    '''

    # parse xml data from file and get the root from the parsed data.
    tree = et.parse(local_folder+filename+'.xml')
    root = tree.getroot()

    # cols is a list of all the columns that will be used later on to form the dataframe
    cols = ["TechRcrdId", "Id", "FinInstrmClssfctn", "FrDt", "ToDt", "Lqdty", "PreTradLrgInScaleThrshld",
            "PstTradLrgInScaleThrshld", "PreTradInstrmSzSpcFcThrshld", "PstTradInstrmSzSpcfcThrshld", "TtlNbOfTxsExctd", "TtlVolOfTxsExctd"]

    # rows is an empty list that will hold our data
    rows = []

    # Since this particular xml data has namespaces, ns is a dictionary tht will represenet the prefix to reduce rewriting code.
    # Default_data represents the tags that have the common URI, xsi represents the exception tags that have a different URI.
    ns = {"default_data": "urn:iso:std:iso:20022:tech:xsd:auth.045.001.02",
          "xsi": "http://www.w3.org/2001/XMLSchema-instance"}

    def getNodeText(node):
        '''
        The getNodeText function will take in a node or element object and check if it is a None value. 
        If it is return none, if not return the element's text
        '''
        if node is not None:
            return node.text
        else:
            return None

    # loop through the tree at index 0 of index 1 of the root. This will save processing time as it
    # reduces the amount of elements that it has to loop over.
    for r in root[1][0]:

        # loop through all the elements that have tag of 'default_data:NonEqtyTrnsprncyData',
        # remember that 'default_data' is used as part of the namespace we defined earlier in the code
        for nodes in r.findall('default_data:NonEqtyTrnsprncyData', ns):

            # Here we set variables for different sub-elements in the NonEqtyTrnsprncyData element
            TechID = nodes.find('default_data:TechRcrdId', ns)
            ID = nodes.find('default_data:Id', ns)
            FinInstrm = nodes.find('default_data:FinInstrmClssfctn', ns)

            # if the particular sub-element has their own sub-elements we check to see if it exists
            # in that particular instance of NonEqtyTrnsprncyData. This is to prevent an error
            # when we index that element. Cannot index an element that is a NoneType
            if nodes.find('default_data:RptgPrd', ns) != None:
                FrDt = nodes.find('default_data:RptgPrd', ns)[0][0]
                ToDt = nodes.find('default_data:RptgPrd', ns)[0][1]
            else:
                FrDt = None
                ToDt = None

            Lqdty = nodes.find('default_data:Lqdty', ns)

            if nodes.find('default_data:PreTradLrgInScaleThrshld', ns) != None:
                PreTradLrgInScaleThrshld = nodes.find(
                    'default_data:PreTradLrgInScaleThrshld', ns)[0]
            else:
                PreTradLrgInScaleThrshld = None
            if nodes.find('default_data:PstTradLrgInScaleThrshld', ns) != None:
                PstTradLrgInScaleThrshld = nodes.find(
                    'default_data:PstTradLrgInScaleThrshld', ns)[0]
            else:
                PstTradLrgInScaleThrshld = None
            if nodes.find('default_data:PreTradInstrmSzSpcfcThrshld', ns) != None:
                PreTradInstrmSzSpcfcThrshld = nodes.find(
                    'default_data:PreTradInstrmSzSpcfcThrshld', ns)[0]
            else:
                PreTradInstrmSzSpcfcThrshld = None
            if nodes.find('default_data:PstTradInstrmSzSpcfcThrshld', ns) != None:
                PstTradInstrmSzSpcfcThrshld = nodes.find(
                    'default_data:PstTradInstrmSzSpcfcThrshld', ns)[0]
            else:
                PstTradInstrmSzSpcfcThrshld = None

            if nodes.find('default_data:Sttstcs', ns) != None:
                TtlNbOfTxsExctd = nodes.find('default_data:Sttstcs', ns)[0]
                TtlVolOfTxsExctd = nodes.find('default_data:Sttstcs', ns)[1]
            else:
                TtlNbOfTxsExctd = None
                TtlVolOfTxsExctd = None

            # we append to the rows list all the variables of this particular loop iteration as a dictionary where the keys are the a string of the element tag name
            # and the value is the variable passed into our getNodeText function which will return the element's text value
            rows.append({"TechRcrdId": getNodeText(TechID), "Id": getNodeText(ID), "FinInstrmClssfctn": getNodeText(FinInstrm), "FrDt": getNodeText(FrDt), "ToDt": getNodeText(ToDt), "Lqdty": getNodeText(Lqdty), "PreTradLrgInScaleThrshld": getNodeText(PreTradLrgInScaleThrshld),
                         "PstTradLrgInScaleThrshld": getNodeText(PstTradLrgInScaleThrshld), "PreTradInstrmSzSpcFcThrshld": getNodeText(PreTradInstrmSzSpcfcThrshld), "PstTradInstrmSzSpcfcThrshld": getNodeText(PstTradInstrmSzSpcfcThrshld), "TtlNbOfTxsExctd": getNodeText(TtlNbOfTxsExctd), "TtlVolOfTxsExctd": getNodeText(TtlVolOfTxsExctd)})

    # we utilize pandas dataframe method to create a dataframe which consists of the rows of data
    # and our columns which we defined earlier
    dataFrame = pd.DataFrame(rows, columns=cols)

    # the dataframe is exported to a csv file format through the to_csv method available to us through the pandas module.
    dataFrame.to_csv(r''+local_folder + filename +
                     '.csv', index=0, header=True)


# a path is defined which takes the users profile in order to get the desktop path
# followed by the directory we created in the extract_raw_data component.
local_folder = os.path.join(os.environ['USERPROFILE'], "Desktop\\FIRDS_Data\\")

# we loop through each file in our path and pass that filename into our xml_data_extract function
for filename in os.listdir(local_folder):
    if filename.endswith(".xml"):
        filename = filename.split('.xml')[0]
        xml_data_extract(filename)
