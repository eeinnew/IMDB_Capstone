from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get("https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31")
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find("div", attrs={"class":"lister list detail sub-list"})
imdb = table.find_all("h3", attrs={"class":"lister-item-header"})

row_length = len(imdb)

temp = [] #initiating a tuple
for i in range(0, len(cont)):
    #Untuk mendapat judul
    judul = cont[i].find('h3',attrs={'class':'lister-item-header'})
    judul = judul.find('a').text
    
    #Untuk mendapat rating
    rating = cont[i].find('div', attrs={'class':'inline-block ratings-imdb-rating'})
    rating = rating.find('strong', attrs={'':''}).text

    #Untuk mendapat Meta
    favorable = cont[i].find('span', attrs={"class": "metascore favorable"})
    mixed = cont[i].find('span', attrs={"class": "metascore mixed"})
     # kondisi ketika keduanya None
    if (favorable == None) and (mixed == None):
     meta = 0
    # kondisi ketika favorable None
    elif (favorable == None):
        meta = mixed.text.strip()
    # kondisi ketika mixed None
    elif (mixed == None):
        meta = favorable.text.strip()

    #Untuk mendapat votes    
    votes = cont[i].find('p', attrs={'class':'sort-num_votes-visible'}).text
    votes = votes.replace("\n","")
    votes = votes.replace("Votes:","")
    votes = votes.replace("| Gross:$858.37M","")
    votes = votes.replace("| Gross:$53.80M","")
    votes = votes.replace("| Gross:$164.87M","")
    votes = votes.replace("| Gross:$121.63M","")
    votes = votes.replace("| Gross:$160.87M","")
    votes = votes.replace("| Gross:$224.54M","")
    votes = votes.replace(",",".")
        
    
    temp.append((judul,rating,meta,votes))
    
temp = temp[::-1]

import pandas as pd
import numpy as np
import seaborn as sb

#change into dataframe
df = pd.DataFrame(temp, columns = ('Judul','imdb_rating','metascore','votes')).replace('N/A',np.NaN)

#insert data wrangling here
df = df.set_index('Judul')
df['votes'] = df['votes'].str.replace(",","")
df['votes'] = df['votes'].astype('float64')
df[['rating','meta']] = df[['rating','meta']].astype('float64')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["imdb_rating"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.sort_values("votes ('0.000)", ascending=False).head(7).plot.barh(figsize = (12,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)