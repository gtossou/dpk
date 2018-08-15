import requests 
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import pandas as pd


class ScrapeSite(object):

	links=[]
	ouptut_filename = "output.xlsx"

	def __init__(self,base_url,base_level, next_page_attr):
		self.base_url = base_url
		self.base_level = base_level
		self.next_page_attr = next_page_attr
		
	def getLinks(self):
		page = requests.get(self.base_level)
		soup = bs(page.text, 'html.parser')
		content = soup.find(class_="pager-next").find('a', href=True)
		self.links.append(self.base_level)

		while (content):
			try:
				next_page=urljoin(self.base_url,content.get("href"))
				self.links.append(next_page)
				page = requests.get(next_page)
				soup = bs(page.text, 'html.parser')
				if (soup.find(class_="pager-next")):
					content = soup.find(class_="pager-next").find('a', href=True)
				else:
					content = None
			except(TypeError, KeyError) as e:
				print("Erreur")

		return self.links

	def saveData(self, links_list):
		columns = set()
		pages_data = []
		self.links = links_list

		for link in self.links:
			page = requests.get(link)
			soup = bs(page.text, 'html.parser')
			table = soup.find('table', attrs={'class':self.next_page_attr})
			header = table.find("thead").find_all('th')
			header = [ele.text.strip() for ele in header]
			columns.update(header)
			table_rows = table.find("tbody")
			rows = table_rows.find_all('tr')
			for row in rows:
				cols = row.find_all('td')
				cols = [ele.text.strip() for ele in cols]
				pages_data.append([ele for ele in cols if ele])
		#print(header)
		dataframe =  pd.DataFrame(data=pages_data, columns = columns)
		writer = pd.ExcelWriter(self.ouptut_filename)
		dataframe.to_excel(writer,'Sheet1')
		writer.save()




projet = ScrapeSite("http://www.ceetrus.com/","http://www.ceetrus.com/fr/implantations-sites-commerciaux","views-table cols-6")
liens = projet.getLinks()
projet.saveData(liens)