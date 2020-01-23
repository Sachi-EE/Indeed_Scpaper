import requests
from bs4 import BeautifulSoup
import pandas as pd 
import time
import urllib3

#List the job types and location  
jobs = ['software engineer']
location = 'los angeles'


# A function to return the urls of the items that'll be serached
def create_url(jobs,location):
  #url for the indeed search page
  url_1 = 'https://www.indeed.com/jobs?q='
  url_2 = '&l='
  url_lst = []
  
  #Writing a for loop to automate url search
  for job in jobs: #Iterating through each job on the list
    url_lst.append(url_1 + job.replace(' ', '+') + url_2 + location.replace(' ', '+')) 

  return url_lst

def scrape(url_lst):

  home_url = 'https://www.indeed.com' #needs to be added to the retrieved link of the scraped page

  for url in url_lst: #Looping through all the urls on the list
    page = requests.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.content, 'lxml')
    rows = soup.find('td', {'id' :  'resultsCol'}).find_all(class_='row')
    links = soup.find('td', {'id' :  'resultsCol'}).find_all(class_='title')
    links_2 = soup.find('td',{'id' : 'resultsCol'}).find_all(class_= 'sjcl')


    job_titles = []
    company_names = []
    job_salaries = []
    job_links = []

    for link in links:
      job_link = link.find('a')['href']
      job_links.append(home_url + job_link)

      job_title = link.find('a')['title']
      job_titles.append(job_title)



    for link_2 in links_2:
      company_name = link_2.find('span', class_= 'company').text.strip()
      company_names.append(company_name)

    for row in rows:
      #job_salary = row.find(name='div', attrs = {'class': 'salarySnippet holisticSalary'})
      try:
        job_salary = row.find('span',{'class': 'salaryText'}).text.strip()
        job_salaries.append(job_salary)
      except:
        job_salaries.append('Nothing_found')
      
    
     #Insert the data into a dictionary 
    data = {
            'Job Title': job_titles,
            'Company Name': company_names,
            'Salary':job_salaries,
            'Link':job_links
           }
      #Use pandas to visualize the data     
    data_pandas = pd.DataFrame(data)
    print(data_pandas)
  
 #Call the scrape function with the create_url as the input function that has jobs & location as input parameters   
scrape(create_url(jobs, location))





