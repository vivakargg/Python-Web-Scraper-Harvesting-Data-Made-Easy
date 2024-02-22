from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent

class IndeedScraper:
    def __init__(self, url, email, password):
        self.url = url
        self.email = email
        self.password = password
        self.long_sleep_time = 10  # Adjust as needed

        # Create a new Firefox browser instance with headless mode
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def email_login(self) -> None:
        input_mail = WebDriverWait(self.driver, self.long_sleep_time).until(
            EC.presence_of_element_located((By.ID, "modalUserEmail"))
        )
        input_mail.send_keys(self.email)
        input_mail.send_keys(Keys.RETURN)

        input_password = WebDriverWait(self.driver, self.long_sleep_time).until(
            EC.presence_of_element_located((By.ID, "modalUserPassword"))
        )
        input_password.send_keys(self.password)
        input_password.send_keys(Keys.RETURN)

    def scrape(self):
        try:
            # Open the webpage
            self.driver.get(self.url)

            # Function to click on "Show more jobs" button
            def click_show_more():
                try:
                    show_more_button = self.driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/div/button")
                    show_more_button.click()
                    time.sleep(5)  # Wait for the page to load additional content
                    return True
                except NoSuchElementException:
                    print("No 'Show more' button found.")
                    return False

            # Test the click function
            click_show_more()

            # Gmail login
            self.email_login()

            # Wait for the login process to complete
            time.sleep(5)

            # Fetch and scrape job details
            self.scrape_job_details()

        except Exception as e:
            print("An error occurred:", e)

        finally:
            # Quit the WebDriver
            self.driver.quit()

    def scrape_job_details(self):
        prev_job_data = None
        while True:
            try:
                # Fetch the HTML content of the webpage
                html_content = self.driver.page_source

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                if not soup.find(class_="jobCard JobCard_jobCardContent__0_4vj"):
                    print("No job cards found. Exiting...")
                    self.driver.quit()
                    break

                job_cards = soup.find_all(class_="jobCard JobCard_jobCardContent__0_4vj")

                # Initialize lists to store job details
                job_titles = []
                job_locations = []
                job_descriptions = []
                job_links = []

                # Iterate through each job card to extract job details
                for job_card in job_cards:
                    # Extract job title
                    job_title_elem = job_card.find(class_="JobCard_jobTitle__rbjTE")
                    job_title = job_title_elem.text.strip() if job_title_elem else "N/A"
                    job_titles.append(job_title)

                    # Extract job location
                    job_location_elem = job_card.find(class_="JobCard_location__N_iYE")
                    job_location = job_location_elem.text.strip() if job_location_elem else "N/A"
                    job_locations.append(job_location)

                    # Extract job description
                    job_description_elem = job_card.find(class_="JobCard_jobDescriptionSnippet__HUIod")
                    job_description = job_description_elem.text.strip() if job_description_elem else "N/A"
                    job_descriptions.append(job_description)

                    job_link_elem = job_card.find("a", class_="JobCard_jobTitle__rbjTE")
                    job_link = job_link_elem["href"] if job_link_elem else "N/A"
                    job_links.append(job_link)

                # Check if there is new data scraped
                current_job_data = (job_titles, job_locations, job_descriptions, job_links)
                if prev_job_data == current_job_data:
                    print("No new data scraped. Exiting...")
                    self.driver.quit()
                    break

                prev_job_data = current_job_data

                # Print or use the collected job details
                for title, location, description , link in zip(job_titles, job_locations, job_descriptions , job_links):
                    print("Title:", title)
                    print("Location:", location)
                    print("Description:", description)
                    print("Link:", link)
                    print()

                # Print the count of jobs scraped
                print("Number of jobs scraped:", len(job_titles))

                # Find the "Show more jobs" button
                if not self.click_show_more():
                    break  # Break the loop if there's no more "Show more jobs" button

            except Exception as e:
                print("An error occurred:", e)
                break

    def click_show_more(self):
        try:
            show_more_button = self.driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/div/button")
            show_more_button.click()
            time.sleep(5)  # Wait for the page to load additional content
            return True
        except NoSuchElementException:
            print("No 'Show more' button found.")
            return False

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Create an instance of IndeedScraper and start scraping
scraper = IndeedScraper("https://www.glassdoor.co.in/Job/pune-india-data-scientist-jobs-SRCH_IL.0,10_IC2856202_KO11,25.htm",
                        "vinnethvicy@gmail.com",
                        "7205674702")
scraper.scrape()
