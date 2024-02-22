import re
import urllib.parse
import requests
import json

def generate_diffbot_api_url(url, token):
    # Encode the URL
    encoded_url = urllib.parse.quote_plus(url)
    
    # Construct the Diffbot API URL
    diffbot_api_url = f"https://api.diffbot.com/v3/list?url={encoded_url}&token={token}"
    
    return diffbot_api_url

def get_json_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

# Example URL
url = "https://www.glassdoor.co.in/Job/pune-india-data-scientist-jobs-SRCH_IL.0,10_IC2856202_KO11,25.htm?fromAge=500"

# Example token
token = "xxxxxxxxxxxxxxxxx"

# Generate the Diffbot API URL
api_url = generate_diffbot_api_url(url, token)

json_data = get_json_data(api_url)
if json_data:
    # print("JSON data:")
    # print(json.dumps(json_data, indent=4))
    items = json_data['objects'][0]['items']
    
    # Print items
    for item in items:
        # print(json.dumps(item, indent=4))
        date = item.get('date', 'N/A')
        summary = item.get('summary', 'N/A')
        job_title_link = item.get('JobCard_jobTitle__rbjTE', 'N/A')
        job_listing_age = item.get('JobCard_listingAge__KuaxZ', 'N/A')
        location = item.get('JobCard_location__N_iYE', 'N/A')
        job_link = item.get('link', 'N/A')
        title = item.get('title', 'N/A')
        employer_profile = item.get('EmployerProfile_employerWithLogo__vpfvz', 'N/A')
        job_description = item.get('JobCard_jobDescriptionSnippet__HUIod', 'N/A')
        salary_estimate_type = item.get('JobCard_salaryEstimateType__bIY_C', 'N/A')
        
        # Print extracted data
        print("Date:", date)
        print("Summary:", summary)
        print("Job Title Link:", job_title_link)
        print("Job Listing Age:", job_listing_age)
        print("Location:", location)
        print("Job Link:", job_link)
        print("Title:", title)
        print("Employer Profile:", employer_profile)
        print("Job Description:", job_description)
        print("Salary Estimate Type:", salary_estimate_type)
        print("\n")
