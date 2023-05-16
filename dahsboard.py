import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import plost



def get_access_token(api_key):
    # Define the authentication endpoint URL
    auth_url = "https://auth.tradeskillmaster.com/oauth2/token"

    # Create the payload with the API key
    payload = {
    "client_id": "c260f00d-1071-409a-992f-dda2e5498536",
    "grant_type": "api_token",
    "scope": "app:realm-api app:pricing-api",
    "token": api_key
}

    try:
        # Send the POST request to obtain the access token
        response = requests.post(auth_url, json=payload)
        response_data = response.json()

        # Extract the access token from the response
        access_token = response_data.get("access_token")

        if access_token:
            st.success("Access token obtained successfully.")
            return access_token
        else:
            st.error("Failed to obtain access token.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred during authentication: {str(e)}")


def settings_page():
    st.title("Settings")
    st.header("API Key")

    # Get the
    #  API key from the user
    api_key = st.text_input("Enter your API key")

    if st.button("Save"):
        # Obtain the access token using the API key
        access_token = get_access_token(api_key)

        if access_token:
            # Save the access token in a Streamlit SessionState
            st.session_state.access_token = access_token


def server_page():
    if "access_token" not in st.session_state:
        st.warning("Please set the API key in the Settings page.")
    else:
        access_token = st.session_state.access_token

        url = "https://realm-api.tradeskillmaster.com/regions"
        response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            # Region information
            regions = response.json().get("items", [])
            region_options = [region["name"] for region in regions]
            region_ids = [region["regionId"] for region in regions]

        else:
            regions = []
            region_options = []
            region_ids = []
        # Create selectbox in sidebar
        st.sidebar.title("Server params")
        selected_index = st.sidebar.selectbox("Select Region", range(len(region_options)), format_func=lambda i: region_options[i])
        selected_region_id = region_ids[selected_index] if regions else None

        if selected_region_id:
            # Server information from specific region
            url = f"https://realm-api.tradeskillmaster.com/regions/{selected_region_id}"
            response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
            

            realm_url = f"https://realm-api.tradeskillmaster.com/regions/{selected_region_id}/realms"
            response = requests.get(realm_url, headers={"Authorization": f"Bearer {access_token}"})
            
            if response.status_code == 200:
                servers = response.json().get("items", [])
                server_options = [server["name"] for server in servers]
                server_ids = [server["realmId"] for server in servers]
               
            else:
                servers = []
                server_options = []
                server_ids = []
            # Create selectbox in sidebar
            selected_realm_index = st.sidebar.selectbox("Select realm", range(len(server_options)), format_func=lambda i: server_options[i])
            selected_realm_id = server_ids[selected_realm_index] if servers else None
            if selected_realm_id:
                url = f"https://realm-api.tradeskillmaster.com/realms/{selected_realm_id}"
                response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
                st.title(f"{server_options[selected_realm_index]} Server information")          
                ahs = response.json().get("auctionHouses", [])
                ah_options = [ah["type"] for ah in ahs]
                ah_id = [ah["auctionHouseId"] for ah in ahs]
                
                selected_ah_index = st.sidebar.selectbox("Select Faction", range(len(ah_options)), format_func=lambda i: ah_options[i])
                selected_ah_id = ah_id[selected_ah_index] if ahs else None
                
                #url = f"https://pricing-api.tradeskillmaster.com/ah/{selected_ah_id}"
                #response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
                #items = response.json()
                if len(ah_id) == 1:
                    game_version = "Retail"
                else:
                    game_version = "Vanilla"
                if game_version == "Retail":
                    #List of the dragonflight Ores
                    ores = [
                       #Shadowflame Essence 
                       {"id": 204464, "name": "Shadowflame Essence", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Dracothyst
                       {"id": 204463, "name": "Dracothyst", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Shadowed Alloy
                       {"id": 204995, "name": "Shadowed Alloy R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 204996, "name": "Shadowed Alloy R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 204994, "name": "Shadowed Alloy R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Dracothyst Shard, might be unable to auction
                       {"id": 204462, "name": "Dracothyst Shard", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Primal Flux, can be bought from vendors
                       {"id": 190452, "name": "Primal Flux", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Primal Molten Alloy
                       {"id": 189541, "name": "Primal Molten Alloy R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 189542, "name": "Primal Molten Alloy R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 189543, "name": "Primal Molten Alloy R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Obsidian Seared Alloy
                       {"id": 190533, "name": "Obsidian Seared Alloy R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190534, "name": "Obsidian Seared Alloy R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190535, "name": "Obsidian Seared Alloy R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Khaz'gorite Ore
                       {"id": 190312, "name": "Khaz'gorite Ore R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190313, "name": "Khaz'gorite Ore R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190314, "name": "Khaz'gorite Ore R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Draconium Ore
                       {"id": 189143, "name": "Draconium Ore R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 188658, "name": "Draconium Ore R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190311, "name": "Draconium Ore R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Infurious Alloy
                       {"id": 190536, "name": "Infurious Alloy R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190537, "name": "Infurious Alloy R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190538, "name": "Infurious Alloy R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Serevite Ore
                       {"id": 190395, "name": "Serevite Ore R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190396, "name": "Serevite Ore R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190394, "name": "Serevite Ore R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       #Frostfire Alloy
                       {"id": 190530, "name": "Frostfire Alloy R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190531, "name": "Frostfire Alloy R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                       {"id": 190532, "name": "Frostfire Alloy R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None}
                    ]

                    for ore in ores:
                        ore_id = ore["id"]
                        response = requests.get(f"https://pricing-api.tradeskillmaster.com/ah/{selected_ah_id}/item/{ore_id}", headers={"Authorization": f"Bearer {access_token}"})
                        if response.status_code == 200:
                            ore_details = response.json()

                            ore["minBuyout"] = ore_details["minBuyout"]
                            ore["quantity"] = ore_details["quantity"]
                            ore["marketValue"] = ore_details["marketValue"]
                            ore["historical"] = ore_details["historical"]
                            ore["numAuctions"] = ore_details["numAuctions"]
                        else:
                            print(f"Error in gem details request for gem ID {ore_id}")
                    #List of the dragonflight Cloths
                    cloths = [
                        #Axureweave Bolt
                        {"id": 193938, "name": "Azureweave Bolt R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 193939, "name": "Azureweave Bolt R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 193940, "name": "Azureweave Bolt R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Wildercloth
                        {"id": 193922, "name": "Wildercloth", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Tattered Wildercloth
                        {"id": 193050, "name": "Tattered Wildercloth", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Spool of Wilderthread
                        {"id": 192095, "name": "Spool of Wilderthread R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192096, "name": "Spool of Wilderthread R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192097, "name": "Spool of Wilderthread R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Contoured Fowlfeather
                        {"id": 193053, "name": "Contoured Fowlfeather", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Vibrant Wildercloth Bolt
                        {"id": 193929, "name": "Vibrant Wildercloth Bolt R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 193930, "name": "Vibrant Wildercloth Bolt R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 193931, "name": "Vibrant Wildercloth Bolt R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Chronocloth Bolt
                        {"id": 193935, "name": "Chronocloth Bolt R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 193936, "name": "Chronocloth Bolt R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 193937, "name": "Chronocloth Bolt R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Frostbitten Wildercloth
                        {"id": 193924, "name": "Frostbitten Wildercloth", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Wildercloth Bolt
                        {"id": 193926, "name": "Wildercloth Bolt R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 193927, "name": "Wildercloth Bolt R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 193928, "name": "Wildercloth Bolt R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Decayed Wildercloth
                        {"id": 193923, "name": "Decayed Wildercloth", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Singed Wildercloth
                        {"id": 193925, "name": "Singed Wildercloth", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Infurious Wildercloth Bolt
                        {"id": 193932, "name": "Infurious Wildercloth Bolt R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 193933, "name": "Infurious Wildercloth Bolt R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 193934, "name": "Infurious Wildercloth Bolt R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None}  
                    ]

                    for cloth in cloths:
                        cloth_id = cloth["id"]
                        response = requests.get(f"https://pricing-api.tradeskillmaster.com/ah/{selected_ah_id}/item/{cloth_id}", headers={"Authorization": f"Bearer {access_token}"})
                        if response.status_code == 200:
                            cloth_details = response.json()

                            cloth["minBuyout"] = cloth_details["minBuyout"]
                            cloth["quantity"] = cloth_details["quantity"]
                            cloth["marketValue"] = cloth_details["marketValue"]
                            cloth["historical"] = cloth_details["historical"]
                            cloth["numAuctions"] = cloth_details["numAuctions"]
                        else:
                            print(f"Error in gem details request for gem ID {cloth_id}")
                    #List of the dragonflight gems
                    gems = [
                        #Alextraszite
                        {"id": 192852, "name": "Alexstraszite R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192853, "name": "Alexstraszite R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192855, "name": "Alexstraszite R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},                        
                        #Ysmerald
                        {"id": 192859, "name": "Ysemerald R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192860, "name": "Ysemerald R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192861, "name": "Ysemerald R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Nozdorite
                        {"id": 192866, "name": "Nozdorite R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192867, "name": "Nozdorite R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192868, "name": "Nozdorite R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Malygite
                        {"id": 192856, "name": "Malygite R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192857, "name": "Malygite R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192858, "name": "Malygite R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Neltharite
                        {"id": 192862, "name": "Neltharite R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192863, "name": "Neltharite R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192865, "name": "Neltharite R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Mystic Sapphire
                        {"id": 192840, "name": "Mystic Sapphire R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192841, "name": "Mystic Sapphire R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192842, "name": "Mystic Sapphire R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Sundered Onyx
                        {"id": 192846, "name": "Sundered Onyx R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192847, "name": "Sundered Onyx R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192848, "name": "Sundered Onyx R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Vibrant Emerlad
                        {"id": 192843, "name": "Vibrant Emerald R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192844, "name": "Vibrant Emerald R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192845, "name": "Vibrant Emerald R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Eternity Amber
                        {"id": 192849, "name": "Eternity Amber R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192850, "name": "Eternity Amber R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192851, "name": "Eternity Amber R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Illimited Diamond
                        {"id": 192869, "name": "Illimited Diamond R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192870, "name": "Illimited Diamond R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192871, "name": "Illimited Diamond R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        #Queen's Ruby
                        {"id": 192837, "name": "Queen's Ruby R1", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192838, "name": "Queen's Ruby R2", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None},
                        {"id": 192839, "name": "Queen's Ruby R3", "minBuyout": None, "quantity": None, "marketValue": None, "historical": None, "numAuctions": None}
                        ]
                    for gem in gems:
                        gem_id = gem["id"]
                        response = requests.get(f"https://pricing-api.tradeskillmaster.com/ah/{selected_ah_id}/item/{gem_id}", headers={"Authorization": f"Bearer {access_token}"})
                        if response.status_code == 200:
                            gem_details = response.json()

                            gem["minBuyout"] = gem_details["minBuyout"]
                            gem["quantity"] = gem_details["quantity"]
                            gem["marketValue"] = gem_details["marketValue"]
                            gem["historical"] = gem_details["historical"]
                            gem["numAuctions"] = gem_details["numAuctions"]
                        else:
                            print(f"Error in gem details request for gem ID {gem_id}")   




                    # DataFrame for gems        
                    df = pd.DataFrame(gems)
                    pd.options.display.float_format = '{:,.0f}'.format
                    df["id"] = df["id"].astype(int)
                    df.set_index("id", inplace=True)
                   
                    chart_data = df[["name","minBuyout", "marketValue"]].set_index('name')
                    fig,ax = plt.subplots()
                    chart_data.plot(kind='bar', ax=ax)


                    
                    ax.set_xlabel("Gem Name")
                    ax.set_ylabel("Value")
                    ax.set_title("Gem Buyout Prices and Market values")

                    #plt.xticks(rotation=45)
                    st.pyplot(fig)
                   
                if game_version == "Vanilla":
                    st.write("Please select a retail region")    


def main():

    st.set_page_config(layout="wide", initial_sidebar_state='expanded')
    st.sidebar.title('Dashboard `version 0.1`')
    st.sidebar.header("Navigation")
    pages = ["Settings", "Server", "Region"]
    selected_page = st.sidebar.selectbox("Page", pages)

    if selected_page == "Settings":
        settings_page()
    elif selected_page == "Server":
        server_page()

if __name__ == "__main__":
    main()

   