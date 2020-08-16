import os
import requests
import io
import zipfile
import xml.etree.ElementTree as et


def download_file(url, path):
    '''
    The download_file function will take in url and path parameters. Then it will access the url through the request module. 
    Read the zipfile through the zip module and extract and save all files in the zip file to the passed in path.
    The zipfile module allows us to work with zipfiles by giving us the ability to read  and write zipfiles.
    '''
    # makes a request to the url and retrieves a response
    request = requests.get(url)

    # BytesIo allows the request to be used as an object and passed directly into the zipfile method.
    # This saves time and reduces space consumed.
    zipDocument = zipfile.ZipFile(io.BytesIO(request.content))

    # extract all contents in the zipDocument to path argument.
    zipDocument.extractall(path)


def create_directory(path):
    '''
    The create_directory function will take in a path parameter, and check if the path exists.
    If the path exists it will print a statement, if not it will create the path through the "makedirs" method.
    The os module is used to check and create directories on a user's operating system
    '''

    # check if path exists already if not then create the path, if it exists then print a statement to console.
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print("The folder exists")


def extract_url_links(web_url):
    '''
    The xml.etree.ElementTree module allows us to represent the whole xml document as a tree.
    The extract_url_links funtcion will take in a web_url parameter to access through the requests module.
    It will then get the xml data on the page through the xml.etree.ElementTree module "fromstring" since a text object is being passed in.
    Once it has parsed the data it will loop through the xml elements and find the element that matches the attribute "download_link".
    This element holds the link that when accessed, will download the raw data in a zip file.
    It will then call the download_file function passing in the link as an argument.
    '''

    # get the api page through passing the web_url argument in the requests module get method
    api_page = requests.get(web_url)

    # create an empty list to store the links
    links = []

    # use the xml.etree.ElementTree to format the data into an xml
    root = et.fromstring(api_page.text)

    # loop through the 2nd root in our element tree and for each of those elements check if the attribute
    # of the element has an attribute called name, and if that name is equal to "download_link".
    # Then check if that element's text is has the string "FULNCR_20200808_D_" in it.
    # If it does then add that element's text to the links list we created earlier
    for node in root[1]:
        for el in node:
            if el.attrib.get("name") == "download_link":
                if "FULNCR_20200808_D_" in el.text:
                    links.append(el.text)

    # loop through the links list and pass it as an argument in our download_file function
    for link in links:
        download_file(link, r""+local_folder)


# We define 2 variables we will be utilizing in certain functions.
# We define the web_url as the url we will find the links in, and the local_folder as the directory we wish to store our files.
# We then call the create_directory function to create the directory path, and the extract_url_links to extract the files.
web_url = "https://registers.esma.europa.eu/solr/esma_registers_fitrs_files/select?q=%2a&fq=creation_date:%5b2020-08-08T00:00:00Z+TO+2020-08-13T23:59:59Z%5d&wt=xml&indent=true&start=0&rows=100"
local_folder = os.path.join(os.environ['USERPROFILE'], "Desktop\\FIRDS_Data\\")
create_directory(local_folder)
extract_url_links(web_url)
