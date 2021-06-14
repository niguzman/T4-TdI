import requests
import xml.etree.ElementTree as ET
import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd


def call_everyone(countries, words):
	dfs = []
	for country in countries:
		url_country = 'https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_'+ country +'.xml'
		r = requests.get(url_country)
		root = ET.fromstring(r.content)

		data = []
		cols = [[]]
		for j in range(len(root.getchildren())):
			child = root.getchildren()[j]
			test = [subchild.tag for subchild in child.getchildren()]
			nro = test.index('GHO')
			if len(cols[0]) != len(test):
				cols[0] = test
			for w in words:
				if w in root[j][nro].text:
					data.append([subchild.text for subchild in child.getchildren()])
					break

		
		df = pd.DataFrame(data)  # Create DataFrame
		df.columns = cols[0]  # Update column names
		df['Numeric'] = df['Numeric'].astype(float)
		df['High'] = df['High'].astype(float)
		df['Low'] = df['Low'].astype(float)
		dfs.append(df.T)
	
	result = pd.concat(dfs, axis=1)
	

	# ACCES GOOGLE SHEET
	gc = gspread.service_account(filename='tarea4-tdi-189603454e11.json')
	sh = gc.open_by_key('16tEMwiHYJXCYPAYbkJ-zCX1DC7GFPfoYhTtXnq1tA2o')
	worksheet = sh.get_worksheet(0)

	# APPEND DATA TO SHEET
	set_with_dataframe(worksheet, result.T)

countries = ["CHL", "ARG", "AUS", "BRA", "CAN", "COL"]
# countries = ["CHL", "ARG"]


words = ["Number of deaths", "Number of infant deaths", "Number of under-five deaths", "Mortality rate for 5-14 year-olds", "Adult mortality rate", "Estimates of number of homicides", "Crude suicide rates",
        "Mortality rate attributed to unintentional poisoning", "Number of deaths attributed to non-communicable diseases", "Estimated road traffic death rate", "Estimated number of road traffic deaths",
        "Mean BMI", "Prevalence of obesity among adults", "Prevalence of obesity among children and adolescents", "Prevalence of overweight among adults", "Prevalence of overweight among children and adolescents",
        "Prevalence of underweight among adults", "Prevalence of thinness among children and adolescents", "Alcohol, recorded per capita", "Estimate of daily cigarette smoking prevalence", "Estimate of daily tobacco smoking prevalence",
        "Estimate of current cigarette smoking prevalence", "Estimate of current tobacco smoking prevalence", "Mean systolic blood pressure (crude estimate)", "Mean fasting blood glucose (mmol/l) (crude estimate)",
        "Mean Total Cholesterol (crude estimate)"]

call_everyone(countries, words)
