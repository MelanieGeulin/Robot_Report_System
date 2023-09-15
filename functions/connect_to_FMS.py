"""
PROGRAM NAME - connect_to_FMS
PROGRAMMER - GloomyKuriozity (gloomykuriosity@gmail.com)
LANGUAGE - Python 
SYSTEM - Windows 11
DATE - 15/09/2023
NDP - None :)
"""
############# LIBRARIES ##################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import requests
from  requests.packages.urllib3.exceptions import InsecureRequestWarning
##########################################

def connect_to_FMS(url,auth):
    """
    Open connection to Fleet Manager System
    
    Args:
        url (str) : url to FMS
        auth (array of str): credentials for FMS

    Return:
        session (): cookies stocked for this page
        response (html): content of the page to be parsed
    """

    #Neglect warnings about certificate --we could add a certificate for optimization --
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    #Open a webpage in the background to the FMS
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    #Pass the security check from Chrome of the FMS --BEWARE! if the website suddenly become secure, those steps will become problematic --
    button = driver.find_element(By.XPATH,'/html/body/div/div[2]/button[3]')
    driver.execute_script("arguments[0].click();", button)
    button = driver.find_element(By.XPATH,'/html/body/div/div[3]/p[2]/a')
    driver.execute_script("arguments[0].click();", button)

    #Stock cookies for the rest of the program
    session = requests.Session()

    #Authentification HTTP -- BEWARE! This is not secure AT ALL. If they change it for a post, those steps will become problematic --
    response = session.get(url,auth=auth, verify=False)

    #Response analysis
    if response.status_code == 200:
        print('Logged in succesfully!')     
    else:
        print('Access Denied!')


    #Return cookies and html
    return session,response