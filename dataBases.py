from google.appengine.ext import db

#Keeps history of searched cards
class Cards(db.Model):
	card = db.StringProperty()
	ip = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	

def add_info_cards(card,ip):
	cards = Cards()
	cards.card = card
	cards.ip = ip
	cards.put()	
	  
#Keeps the REAL and DOLLAR currency	  
class Conversoes(db.Model):
	euro_to_real = db.FloatProperty()
	euro_to_dollar = db.FloatProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	
	
def add_info_conversoes(real,dollar):
	conversoes = Conversoes()
	conversoes.euro_to_real = real
	conversoes.euro_to_dollar = dollar
	conversoes.put()


def get_info_conversoes(info):
	try:
		conversoes = db.GqlQuery("SELECT * "
							"FROM Conversoes ")
						
		if info == "real":
			return conversoes[0].euro_to_real
		if info == "dollar":
			return conversoes[0].euro_to_dollar
	except:
		return "not available"
	
	
import httpUtils
from BeautifulSoup import BeautifulSoup
import logging
import html_to_info
def get_currency():
	url_real = "http://www.google.com/finance/converter?a=1&from=EUR&to=BRL"
	url_dollar = "http://www.google.com/finance/converter?a=1&from=EUR&to=USD"
	
	##################################################
	##################REAL##########################
	##################################################
	real_html = httpUtils.fetchURL(url_real)
	
	soup_real = BeautifulSoup(real_html)
	
	t = str(soup_real.body.find(id="currency_converter_result"))

	notags = html_to_info.remove_html_tags(t)
	
	start = notags.find("1 EUR = ")
	end = notags.find("BRL")
	
	str_real = notags[start+7:end]
	
	real = float(str_real.strip())
	
	##################################################
	##################DOLLAR##########################
	##################################################
	
	dollar_html = httpUtils.fetchURL(url_dollar)
	
	soup_dollar = BeautifulSoup(dollar_html)
	
	t = str(soup_dollar.body.find(id="currency_converter_result"))

	notags = html_to_info.remove_html_tags(t)
	
	start = notags.find("1 EUR = ")
	end = notags.find("USD")
	
	str_dollar = notags[start+7:end]
	
	dollar = float(str_dollar.strip())
	
	conversoes = db.GqlQuery("SELECT * "
                            "FROM Conversoes ")
	
	for conversao in conversoes:
		conversao.delete()
	
	#TO ADD TO DATABASE
	add_info_conversoes(real,dollar)
	
	