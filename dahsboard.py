import streamlit as st
import pandas as pd
import numpy as np
import requests

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

    # Get the API key from the user
    api_key = st.text_input("Enter your API key")

    if st.button("Save"):
        # Obtain the access token using the API key
        access_token = get_access_token(api_key)

        if access_token:
            # Save the access token in a Streamlit SessionState
            st.session_state.access_token = access_token


def main_page():
    

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
                st.title(f"Information for {server_options[selected_realm_index]}")          
                st.write(response.json())
                ahs = response.json().get("auctionHouses", [])
                ah_options = [ah["type"] for ah in ahs]
                ah_id = [ah["auctionHouseId"] for ah in ahs]
                
                selected_ah_index = st.sidebar.selectbox("Select Faction", range(len(ah_options)), format_func=lambda i: ah_options[i])
                selected_ah_id = ah_id[selected_ah_index] if ahs else None
                
                url = f"https://pricing-api.tradeskillmaster.com/ah/{selected_ah_id}"
                response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
                st.write(response.json())


def main():
    st.sidebar.title("Navigation")
    pages = ["Settings", "Server", "Region"]
    selected_page = st.sidebar.selectbox("Page", pages)

    if selected_page == "Settings":
        settings_page()
    elif selected_page == "Server":
        main_page()

if __name__ == "__main__":
    main()

   