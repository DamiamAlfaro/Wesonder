from bs4 import BeautifulSoup
import requests
import pandas as pd


url = "https://en.wikipedia.org/wiki/List_of_municipalities_in_California"

souping = requests.get(url)
soup = BeautifulSoup(souping.content, 'html.parser')
text = soup.get_text() # Pure text without html attributes, useful for strings

table = soup.find_all('table')
result = table[1]

tablerows = result.find_all('tr')

municipalities = []
for muni in range(len(tablerows)):
  municipalityRaw = [tablerows[muni].find_all('th'),tablerows[muni].find_all('td')]
  municipalityAtt = []
  for i in municipalityRaw[0]:
    x = i.text[:-1]
    if x[-1].isalpha() == False:
      municipalityAtt.append(x[:-1])
    else:
      municipalityAtt.append(x)
  for rest in municipalityRaw[1]:
    if "\xa0" in rest.text:
      newString = rest.text.replace('\xa0', ' ')
      municipalityAtt.append(newString[:-1])
    else:
      municipalityAtt.append(rest.text[:-1])
  municipalities.append(municipalityAtt)

allMunicipalities = municipalities[2:]

maintableHeaders = ['MunicipalityName','HumanSettlementType','MunicipalityCounty','2020Population',
                    '2010Population','PopulationChange',
                    'SquareMiles','SquareKilometers','PopulationDensity','DateIncorporated']

df = pd.DataFrame(data=allMunicipalities,columns=maintableHeaders)


#resultFile = "CaliforniaMunicipalities.csv"

#df.to_csv(resultFile,index=False)

read = pd.read_csv("CaliforniaMunicipalities.csv",index_col=5)
print(read)
  