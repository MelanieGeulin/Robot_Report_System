href = a_elements["href"]
            href = url36_auth + href
            
            response_temp = session.get(href,auth=auth36, verify=False)

            if response.status_code == 200:
                soup_temp = bs(response_temp.text,"html.parser")

                ul_element = soup_temp.find('ul')
                li_elements = ul_element.find_all('li')

                if li_elements[1].text != "Mission Instance ID: None":
                    num_real_mission = num_real_mission+1