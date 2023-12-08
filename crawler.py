#crawling the website for all defis

import requests
from bs4 import BeautifulSoup

def crawl_nuitdelinfo(start_page, end_page):
    base_url = "https://www.nuitdelinfo.com/inscription/defis/liste?page="

    for page_number in range(start_page, end_page + 1):
        url = base_url + str(page_number)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            challenges = soup.select('.defiList .defi')
            for challenge in challenges:
                title_element = challenge.select_one('.title a')
                title = title_element.text.strip()
                thumbnail = challenge.select_one('.lot img')['src']
                link = title_element['href']
                
                # Extract the content after </a> directly within the title div
                desc = ""  # title_element.find(string=True, recursive=False).strip() if title_element else ""

                # Prepare data for the POST request
                data = {
                    'title': title,
                    'description': desc,
                    'thumbnail': thumbnail, 
                    'link': link
                }

                
                submit_url = 'http://127.0.0.1:5000/submit_problem'  # Update with your app's URL
                response = requests.post(submit_url, data=data)

                print(f"POST Response Status Code: {response.status_code}")

                print("\n---\n")
        else:
            print(f"Failed to fetch page {page_number}")

if __name__ == "__main__":
    start_page = 1
    end_page = 10
    crawl_nuitdelinfo(start_page, end_page)
