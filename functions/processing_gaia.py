"""
PROGRAM NAME - Robot Report System
PROGRAMMER - GloomyKuriozity (gloomykuriosity@gmail.com)
LANGUAGE - Python 
SYSTEM - Windows 11
DATE - 15/09/2023
Last update - 15/09/2023
"""

############# LIBRARIES ##################
from functions.globals import *
from functions.connect_to_FMS import *
from functions.calculations import *

import os
##########################################


def processing_gaia():
    """
    Calculate all GAIA data
    
    Args:
        None

    Return:
        None
    """

    #Check if the data log is there
    if os.path.exists(data_path_gaia):
        print("Data log exists")

    else:
        print("File creation for GAIA...")

        #Create calculations file for GAIA
        array = np.zeros((60,3))
        with open(data_path_gaia, 'w') as file:
            for item in array:
                file.write(str(item) + "\n")

    
    #Check if the mission log is there
    if os.path.exists(missions_path_gaia):
        print("File exists")
    
    else:
        print("File creation for GAIA...")

        #Create missions list file for GAIA
        with open(missions_path_gaia, 'w') as file:
            file.write(str("[0. 0. 0.]") + "\n")
            

    #Connection to FMS
    session,response = connect_to_FMS(url36,auth36)

    #Connection to GAIA mission page
    response = session.get("https://10.48.45.36/basic/fleet/www/status/missions/gaia",auth=auth36, verify=False)

    #Start calculations
    if response.status_code == 200:
        print('Connection to GAIA status mission successful!')
        all_missions_on_2_month_count(session,response)
        
    else:
        print('Connection to GAIA status mission failed!')