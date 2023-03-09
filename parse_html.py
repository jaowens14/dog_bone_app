import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


def parse_report(report):
    """
    parse_report takes a html file as its input 
    and returns first a dict w
    """
    #########################################################
    ### Processing HTML for force and displacement data
    # read the file in
    report_content = report.read()
    # create the soup to process the html report
    soup = BeautifulSoup(report_content, 'html.parser')
    # create a list of strings from every tag that contains 'table'
    table = [x.get_text() for x in soup.find_all("table")]
    # split the string by the double space between the data points
    table = table[1].split("\n\n")
    # create an empty list to store data
    data = []
    for element in table:
        # remove the leading '\n' from the elements
        element = element.lstrip("\n")
        # collect nonzero elements
        if element != '':
            data.append(element.split("\n"))
    # creating data frame from the list of text data
    force_disp_dataframe = pd.DataFrame(data[1:], columns=['Reading Number', 'Load [N]', 'Travel [mm]', 'Time [sec]'])
    
    #########################################################
    ### Processing HTML for data header

    '''
    # get the text and split the lines by space
    text = soup.get_text().splitlines()
    # check the sections for the Build number
    for section in text:
        if "BUILD" in section:
            # once we have that section split it by the comma 
            header = section.split(", ")
    # create dict to hold info
    header_dict = {}
    # for the fields in the header split and store into a dict
    for field in header:
        k,v = field.split(": ")
        header_dict[k] = v
    '''
    return force_disp_dataframe




