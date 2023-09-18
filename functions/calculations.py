"""
PROGRAM NAME - Robot Report System
PROGRAMMER - GloomyKuriozity (gloomykuriosity@gmail.com)
LANGUAGE - Python 
SYSTEM - Windows 11
DATE - 15/09/2023
Last Update - 15/09/2023
"""

############# LIBRARIES ##################
from bs4 import BeautifulSoup as bs

from datetime import datetime, timedelta
from tqdm import tqdm

import numpy as np

from functions.globals import *

import os
##########################################

def update_data(session,actual_date,tr_elements):
    """
    Will store the number of success/fail by day in a file
    
    Args:
        session () : cookies from the session
        response (html) : html with page info

    Return:
        None
    """

    minimal_date = actual_date - timedelta(days = 60)
    minimal_date = minimal_date.strftime("%Y-%m-%d")
    mission_date = minimal_date
    array = np.zeros((60,3))
    i = 0

    for i in range(0,60):
        array[i,0] = actual_date-timedelta(days = i)

    actual_date = actual_date.strftime("%Y-%m-%d")

    #Visual progress bar for the processing
    progress_bar = tqdm(total=len(tr_elements)-1,desc="Processing GAIA missions")
    
    #Will check every mission
    for i in range(1,len(tr_elements)):
        #Go through all td(mission details) elements in tr(mission) elements
        td_elements = tr_elements[i].find_all('td')

        #Retreive the date of the mission
        mission_date = datetime.strptime(td_elements[3].text, "%Y-%m-%d %H:%M:%S (%Z)")
        mission_date = mission_date.strftime("%Y-%m-%d")
        
        #Check if the mission is in the date interval and a real mission (no DRIVETO, DOCK, TAKE_MEASUREMENT)
        if td_elements[1].text != "None" and mission_date >= minimal_date:

            #Retreive the link to the mission details
            a_elements = td_elements[0].find('a')
            href = url36_auth + a_elements['href']

            #Parse the mission details page
            response_td = session.get(href, auth=auth36, verify=False)
            soup_td = bs(response_td.text, 'html.parser')

            #Go through tr and td elements to find the end of mission status (SUCCESSFUL, UNSUCCESSFUL, CANCELED)
            tr_elements_td = soup_td.find_all("tr")
            mission_end_status = tr_elements_td[len(tr_elements_td)-1].find_all('td')
            mission_end_status = mission_end_status[4].text

            #Add one to successful
            j = 0
            if mission_end_status == "SUCCESSFUL":
                for j,row in array:
                    if row[0] == mission_date:
                        array[j,1] =  array[j,1] + 1
                        break

            #If canceled before 50% of the mission, it's an error so it's failed. If not, we considered it was needed by the operator
            elif mission_end_status == "CANCELED":
                check_manual = tr_elements_td[int(len(tr_elements_td)/2)].find_all('td')
                check_manual = check_manual[4].text
                if check_manual != 'CANCELED':
                    for j,row in array:
                        if row[0] == mission_date:
                            array[j,1] =  array[j,1] + 1
                            break
                
                else:
                    for j,row in array:
                        if row[0] == mission_date:
                            array[j,2] =  array[j,2] + 1
                            break
            else:
                for j,row in array:
                    if row[0] == mission_date:
                        array[j,2] =  array[j,2] + 1
                        break

        
        progress_bar.update(1)
        i = i+1

    progress_bar.close()


def all_missions_on_2_month_count(session,response):
    """
    Calculate all GAIA missions on the right intervalle (2 months starting last registered date)
    
    Args:
        session () : cookies from the session
        response (html) : html with page info

    Return:
        None
    """

    ############# DECLARES ##################
    num_real_mission = 0
    num_successful_mission = 0
    success_records = np.zeros((60,3))
    #########################################

    #Parse the page to find all the elements inside
    soup = bs(response.text, 'html.parser')

    #Every mission is under "tr" element so we find all of them -- the length of the array will be the number of mission in total --
    tr_elements = soup.find_all("tr")

    #We take the last date has starting point
    actual_date = tr_elements[1].find_all('td')
    actual_date = datetime.strptime(actual_date[3].text, "%Y-%m-%d %H:%M:%S (%Z)")

    #We calculate the date 2 month prior
    minimal_date = actual_date - timedelta(days = 60)
    minimal_date = minimal_date.strftime("%Y-%m-%d")

    #We take the last date has starting point and calculate date 2 months prior.
    last_mission_id = tr_elements[1].find_all('td')
    last_mission_id = tr_elements[0].text

    #Check the last date logged in data
    with open(data_path_gaia, 'r') as file:
        lines = file.readlines()
        row = lines[0].strip()
        elements = row[1:-1].split()
        date_log = elements[0]
        print(date_log)

    #Check the last mission id logged in file
    with open(missions_path_gaia, 'r') as file:
        lines = file.readlines()
        row = lines[0].strip()
        elements = row[1:-1].split()
        id_log = elements[0]

    if date_log == "0.":
        update_data(session,actual_date,tr_elements)
    else:
        if date_log == actual_date:
            if last_mission_id == id_log:
                pass
            else:
                if id_log == 0:
                    #UPDATE DE TOUTES LES MISSIONS DANS MISSION LOG
                    pass #temp
                else:
                    #UPDATE DES MISSIONS DANS MISSION LOG
                    pass #temp
        else:
            #DEPLACEMENT DES VALEURS AVEC LA NOUVELLES DATE CACULE
            pass #temp

    