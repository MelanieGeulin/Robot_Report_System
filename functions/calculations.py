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
##########################################


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

    #Inside the tr elements, there are td elements with the second one having the date. We take the last date has starting point and calculate date 2 months prior.
    minimal_date = tr_elements[1].find_all('td')
    minimal_date = datetime.strptime(minimal_date[3].text, "%Y-%m-%d %H:%M:%S (%Z)") - timedelta(days = 60)
    minimal_date = minimal_date.strftime("%Y-%m-%d")

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

            #Add one mission to the total mission count in 2 months
            num_real_mission = num_real_mission + 1

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
            if mission_end_status == "SUCCESSFUL":
                num_successful_mission = num_successful_mission+1

            #If canceled before 50% of the mission, it's an error so it's failed. If not, we considered it was needed by the operator
            elif mission_end_status == "CANCELED":
                check_manual = tr_elements_td[int(len(tr_elements_td)/2)].find_all('td')
                check_manual = check_manual[4].text
                if check_manual != 'CANCELED':
                    num_successful_mission = num_successful_mission+1
        
        progress_bar.update(1)

    progress_bar.close()

    print(f'Number of REAL missions made by GAIA in the last 2 months: {num_real_mission}')
    print(f'Number of successful missions: {num_successful_mission}')
    print(f'Number of failed missions: {num_real_mission-num_successful_mission}')