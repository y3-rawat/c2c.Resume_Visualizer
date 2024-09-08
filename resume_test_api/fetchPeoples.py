import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import re
import json

def twitter(company,position):

    query =f'site:twitter.com "{position}" "{company}" in bio -inurl:status'

    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': 'YOUR_COOKIE_HERE'
    }
    response = requests.get(url, headers=headers)   

    # Define the regex pattern to find Twitter URLs
    pattern = r'https://twitter.com[^\s"\'<>]+'

    # Find all matches in the content
    matches = re.findall(pattern, response.text)
    filtered_matches = [match for match in matches if '&' not in match and ';' not in match and '\\' not in match]
    fm = set(filtered_matches)

    # List to hold the JSON objects
    json_objects = []

    # Process each link
    for link in fm:
        # Extract the last word from the link
        name = link.split('/')[-1]
        
        # Create a dictionary for the JSON object
        json_object = {
            "name": name,
            "position": position,
            "link": link
        }
        
        # Add to the list of JSON objects
        json_objects.append(json_object)


    # Print or save the JSON string
    
    return json_objects

def linkedin(company, position):
    query = f'site:linkedin.com/in/ AND "{company}" AND "{position}"'
    encoded_query = quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    hrefs = [link.get('href') for link in soup.find_all('a') if link.get('href')]
    linkedin_links = [href for href in hrefs if 'linkedin.com/' in href and '&' not in href]        
    
    if linkedin_links:
        
        # Process all profiles
        profile_data_list = []
        for link in linkedin_links:  # Corrected variable name
            profile_data = {
                "name": link.split('/')[-1],  # Access the link
                "position": position,
                "link": link  # Access the link
            }
            profile_data_list.append(profile_data)
        
        return profile_data_list  # Return the list of profile data

    else:
        print("No LinkedIn profiles found.")
        return []  # Return an empty list if no profiles found




def instagram(company,position):


    query =f'site:instagram.com "{company}" "{position}" -reel -p/'

    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': 'YOUR_COOKIE_HERE'
    }
    response = requests.get(url, headers=headers)   

    # Define the regex pattern to find Twitter URLs
    pattern = r'https://www.instagram.com/[^\s"\'<>]+'

    # Find all matches in the content
    matches = re.findall(pattern, response.text)
    unique_instagram_links = list(set(matches))
    filtered_matches = [match for match in unique_instagram_links if '&' not in match and ';' not in match and '\\' not in match and 'reels' not in match]
    # List to hold the JSON objects
    json_objects = []
    # Process each link
    for link in filtered_matches:
        # Extract the last word from the link
        name = link.split('/')[-2]
        
        # Create a dictionary for the JSON object
        json_object = {
            "name": name,
            "position": position,
            "links": link
        }
        
        # Add to the list of JSON objects
        json_objects.append(json_object)

    
    return json_objects


