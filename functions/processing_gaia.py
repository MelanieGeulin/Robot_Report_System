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
##########################################


def processing_gaia():
    """
    Calculate all GAIA data
    
    Args:
        None

    Return:
        None
    """

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