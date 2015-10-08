# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import re

#USER LIBS
import httpUtils
import dataBases

#DEBUG
import logging


############################################################	
##################COMMON FUNTIONS to HTML###################
############################################################
#Creates page links based in names
def create_link(name):
    INIT = "<a keyName=\"" + name + "\" onmouseover=\"ChangeBigCard(this)\" href=\"http://gatherer.wizards.com/Pages/Search/Default.aspx?name=+"
    END = "\" target=\"_blank\">"+ name + "</a>"
    
    name_pieces = name.split(" ")
    
    correct_name = ""
    
    for piece in name_pieces:
        correct_name += "["+ piece.strip() +"]"
    
    correct_name.replace("%EF%BF%BD","'")
    
    return INIT + correct_name.replace("][","]+[") + END
    

	
#Cardsmagic
#Letscollect
#Viamagic
#Magictuga
#Creates page links for the stores
def create_store_link(store):
	if store == "Cardsmagic":
		return "<a href=\"http://www.cardsmagic.net\" target=\"\&quot;_blank\&quot;\"><b>Cardsmagic</a>"
	elif store == "Viamagic":
		return "<a href=\"http://www.viamagic.net\" target=\"\&quot;_blank\&quot;\"><b>Viamagic</a>"
	elif store == "Letscollect":
		return "<a href=\"http://letscollect.com.br\" target=\"\&quot;_blank\&quot;\"><b>Letscollect</a>"
	elif store == "Magictuga":
		return "<a href=\"http://www.magictuga.com\" target=\"\&quot;_blank\&quot;\"><b>Magictuga</a>"
		
	#Exceptions
	elif  store == "Cardsmagic - Site Unavailable":
		return "<a href=\"http://www.cardsmagic.net\" target=\"\&quot;_blank\&quot;\"><b>Cardsmagic - Site Unavailable</a>"
#creates info to use in html table	
def info_to_table(cards,existing = "",desired = ""):
	
	#what is to be returned
	html = ""

	for card in cards:
		#Foil Filter
		if "Foil" in card.edicao:
			pass
		else:
			#To make prices uniform
			price = card.preco.replace(',','.')
			
			html += create_store_link(card.loja) + ";;;" + create_link(card.nome) + ";;;" + card.edicao + ";;;" + card.tipo + ";;;" + card.stock + ";;;" + price_with_currency(price,existing,desired)
			html += "###"
		
		if card.nome == "N/A":
			break
		
	return html

#creates the correct price	
def price_with_currency(price,existing,desired):
	
	if existing == desired:
		if existing == "":
			return price
		if existing == "Euro":
			return str(price) + " &euro;"
		if existing == "Real":
			return "R$ " + str(price)
	price = float(price)	
	if existing == "Euro" and desired == "Real":
		Real = dataBases.get_info_conversoes("real")
		
		toReturn = price*Real
		toReturn += 0.05
		toReturn = "%.2f" % toReturn
		
		return "R$ " + str(toReturn)
		
		
	if existing == "Real" and desired == "Euro":
		Real = dataBases.get_info_conversoes("real")
		
		toReturn = price/Real
		toReturn += 0.05
		toReturn = "%.2f" % toReturn
		
		return str(toReturn) + " &euro;"
	return price

	
############################################################
#########Class que representa uma carta de magic############
############################################################
class cartaMagic(object):
    def __init__(self, nome, edicao, tipo, preco,stock,loja):
        self.nome = nome
        self.edicao = edicao
        self.tipo = tipo
        self.preco = preco
        self.stock = stock
        self.loja = loja
        

############################################################	
#######################COMMON FUNTIONS######################
############################################################
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)	

	

############################################################	
################HTML FETCHER BY YAHOO#######################
############################################################		
	
	
############################################################	
########################MAGICTUGA###########################
############################################################
allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,-' ()¥`"
def sanatize_output_magictuga(str):
	
	try:
		sanatized_output = ""
		control_var = 2
		for i in range(len(str)):
	
			if control_var == 2:
				if str[i] in allowed_chars:
					sanatized_output += str[i]
				elif str[i-1].isalpha():
					sanatized_output += "'"
					control_var = 0
				else:
					sanatized_output += "-"
					control_var = 0
			else:
				control_var += 1
		return sanatized_output
	except:	
		return str
		

def get_magictuga_card(list):

	nome = sanatize_output_magictuga(list[0].strip())
	edicao = list[1].strip()
	tipo = sanatize_output_magictuga(list[3].strip())
	stock = list[7].strip()
	preco = list[8].strip()
    
	index = preco.find('.')
	preco = preco[:index+3]
	
	return cartaMagic(nome,edicao,tipo,preco,stock,"Magictuga")

def magictugaHTMLtoInfo(html):

    soup = BeautifulSoup(html)
    
    
    All_tables = soup.findAll("table")
    
    table = None
    
    for t in All_tables:
        temp = str(t)
        if "<a href=\"carta_ver.asp?id=" in temp:
            table = t
    
    #NO INFO
    if table == None:
        return "No Info"
    
    midway_info = [] # store all of the records in this list
    for row in table.findAll('tr'):
        col = row.findAll('td')
        for elem in col:
            midway_info.append((remove_html_tags(str(elem.contents)).replace("\n","")).strip())
    
    
	
	
	other_midway_info = midway_info
	midway_info =  []
	
	for info in other_midway_info:
		
		midway_info.append(info)
		
	
    
    cards = []
    midway_card = []
    for i in range(len(midway_info)):
	
        #FOR TRANSAFORMATION CARDS
        if "-----Transform-----" in midway_info[i]:
            start = midway_info[i].find("\">")
            transform_name = midway_info[i]
            transform_name = transform_name[start+2:]
            
            midway_info[i] = ","+transform_name
		
		
        if i < 10:
            pass
        else:
            try :
                card_cat = ""
                info = midway_info[i].split(",")
                if len(info) >3:
                    card_cat = info[1] + "," + info[2]
                    midway_card.append(card_cat)
                else:
                    midway_card.append(midway_info[i].split(",")[1])
            except :
                midway_card.append(" ")
            

            
        if i%10 == 9 and i > 9:            
            cards.append(get_magictuga_card(midway_card))
            midway_card = []

        
    return cards
        
############################################################	
########################VIAMAGIC############################
############################################################
#just cleans the preco and stock properties of cards
def clean_info(info):
	accepted_chars = "0123456789."
	
	clean_info = ""
	
	for i in info:
		if i in accepted_chars:
			clean_info = clean_info+i
			
	return clean_info		
  
def viamagicHTMLtoInfo(html):
	
	soup = BeautifulSoup(html)
    
	card_info = soup.body.findAll("td", {"width" : "173" , "valign" : "top"})
    
    
	table = BeautifulSoup(str(card_info))
    
	
	midway_info = [] # store all of the records in this list
	for row in table.findAll('tr'):
		col = row.findAll('td')
		for elem in col:
			midway_info.append((remove_html_tags(str(elem.contents)).replace("\n","")).strip())	
	
	
	if midway_info == []:
		return "No Info"
	
	#cards to return
	cards = []
	
	two_is_a_card = 0
	name = ""
	edition = ""
	preco = ""
	stock = ""
	for piece in midway_info:
		if ")" and "(" in piece:
			two_is_a_card += 1
		
			#edicao
			start_edition = piece.find('(')
			end_edition = piece.find(')')
			
			edition = piece[start_edition+1:end_edition]
			
			#Nome
			start_name = piece.find(" ")
			end_name = piece.find("/")
			
			if end_name == -1:
				end_name = piece.find("(")
			
			name = piece[start_name+1:end_name]
			

		if "Stock" in piece:
			two_is_a_card += 1
		
			#preco
			dot_location = piece.find('.')
			preco = piece[dot_location-3:dot_location+3]
			
			#stock
			blank = piece.replace(" ","")
			location = (blank.split("Stock"))[1]
			closer_location = (location.split('¬'))[1]
			where_to_cut = closer_location.find('¬')
			stock = closer_location[where_to_cut+1:]
			
		if two_is_a_card == 2:
			cards.append(cartaMagic(name,edition,"N/A",clean_info(preco),clean_info(stock),"Viamagic"))
			
			two_is_a_card = 0
			name = ""
			edition = ""
			preco = ""
			stock = ""

			
	return cards

	
############################################################	
########################letscollect#########################
############################################################
def clean_price(price):
	div = price.find(" ")
	
	return price[div:].strip()



def getInfo_letscollect(html):

	soup = BeautifulSoup(html)
	
	table = soup.body.findAll(id = 'ctl00_content_ctl00_content_ajpListagemPanel')	
	
	info_splitted = str(table).split(">\n<")
	
	name = ""
	edition = ""
	type = ""
	price = ""
	stock = ""
	
	card_reference_val = 0
	
	cards = []
	
	for t in info_splitted:
	
		if card_reference_val == 5:
		
			cards.append(cartaMagic(name,edition,type,clean_price(price),stock,"Letscollect"))
		
			name = ""
			edition = ""
			type = ""
			price = ""
			stock = ""
	
			card_reference_val = 0
			
		if "td colspan=\"4\"><a href=\"/ecom.aspx/Produto/" in t:
			start = t.find("<span class=\"cad-tit\">")
			mid_name = t[start+len("<span class=\"cad-tit\">"):]
			end = mid_name.find("<")
			name = mid_name[:end]
			
			if name.endswith(" - "):
				name = name.replace(" - ","")
				
			name = name.strip()
			
			card_reference_val += 1
		
		if "S√©rie"	in t:
			start = t.find("<span class=\"cad-lbl2\">")
			mid_edition = t[start+len("<span class=\"cad-lbl2\">"):]
			end = mid_edition.find("</span>")
			edition = mid_edition[:end]
			
			edition = edition.strip()
			
			#####################################################
			
			start = mid_edition.find("<span class=\"cad-lbl2\">")
			mid_type = mid_edition[start+len("<span class=\"cad-lbl2\">"):]
			end = mid_type.find("</span>")
			type = mid_type[:end]
			
			type = type.strip()
			
			card_reference_val += 2
			
		if "Pre√ßo:" in t:
			start = t.find("</span> <span>")
			mid_price = t[start+len("</span> <span>"):]
			end = mid_price.find("</span>")
			price = mid_price[:end]
			
			price = price.strip()
			
			card_reference_val += 1
			
		if ">Qtde. em Estoque:" in t:
			start = t.find("<strong class=\"qtde\">")
			mid_stock = t[start+len("<strong class=\"qtde\">"):]
			end = mid_stock.find("</strong>")
			stock = mid_stock[:end]
			
			stock = stock.strip()
			
			card_reference_val += 1
			
	if len(cards) == 0:
		return "No info"
		
	return cards
			
		
############################################################	
################HTML FETCHER BY GOOGLE######################
############################################################	


############################################################	
########################CARDSMAGIC##########################
############################################################	
def cardsmagicHTMLtoInfo(html):

	soup = BeautifulSoup(html)
	
	card_table = soup.body.find(id="product_list")
	
	
	if card_table == None:
		return "No info"
	
	divs = card_table.findAll('div')
	
	toReturn = []
	
	name = ""
	stock = ""
	price = ""
	edition = ""
	
	center_block = False
	right_block = False
	
	for div in divs:
		if center_block and right_block:
			center_block = False
			right_block = False
			toReturn.append(cartaMagic(name,edition,"N/A",price,stock,"Cardsmagic"))
	
	
		line = str(div)
		#NAME AND EDITION
		if "<div class=\"center_block\">" in line:
			
			center_block = True
		
			start = line.find("title=\"")
			name_line = line[start+7:]
			end = name_line.find("\"><")
			
			#cutted
			name_line = name_line[:end]
			
			name_edition = name_line.split("(")
			
			#NAME AND EDITION
			name = (name_edition[0]).strip().replace("&rsquo;","'")
			edition = (name_edition[1].replace(")","")).strip()
			
		#PRICE AND STOCK
		elif "<div class=\"right_block\">" in line:
		
			right_block = True
		
			start = line.find("<span class=\"price\" style=\"display: inline;\">")
			price_line = line[start+ len("<span class=\"price\" style=\"display: inline;\">"):]
			end = price_line.find("</span")
			
			#cutted
			price = ((price_line[:end].strip()).split(" ")[0]).replace(",",".")
			
			stock_line = price_line[end+6:]
			
			#To remove Add to cart feature
			
			start = stock_line.find("</span>")
			end = stock_line.find("items in stock")
			if end == -1:
				end = stock_line.find("item in stock")
			
			stock = stock_line[start+7:end].strip()
			
			#To add add to cart feature
			
			#stock = stock_line[start+7:end].strip()
			
			#start = stock_line.find("</span>")
			
			#end = stock_line.find("</a><br />")
			
			#end += len("</a>")
			
			#stock = stock_line[start+7:end].strip()
			
			#stock = stock.replace("items in stock","")
			#stock = stock.replace("item in stock","")
			#stock = stock.replace("</div>","")
			#stock = stock.replace("title=\"Add to cart\"","title=\"Add to cart\" target=\"_blank\"")
			
			#position = stock.find("token=") + len("token=")
			
			#start_line = stock[:position]
			#end_line = stock[stock.find(" rel=\"ajax_id_product"):]
			
			#token = "f9491f5fc5adfe03cacedc2aab0fae4b\""
			
			#stock = start_line + token + end_line
		
			#logging.info("-----------------------------------------")
			#logging.info(stock)
			#logging.info("-----------------------------------------")
	
	return toReturn	
	
#Distributor for YAHOO	
def rui_costa(url,html,moeda):

	cards = None
	
	if "magictuga" in url:
		info = magictugaHTMLtoInfo(html)
		if info == "No Info":
			error_cards = [] 
			error_cards.append(cartaMagic("N/A","N/A","N/A","N/A","N/A","Magictuga"))
			cards = info_to_table(error_cards)
		else:
			cards = info_to_table(info,"Euro",moeda)
        
	elif "viamagic" in url:
		info = viamagicHTMLtoInfo(html)
		if info == "No Info":
			error_cards = [] 
			error_cards.append(cartaMagic("N/A","N/A","N/A","N/A","N/A","Viamagic"))
			cards = info_to_table(error_cards)
		else:
			cards = info_to_table(info,"Euro",moeda)

	if "cardsmagic" in url:
		info = cardsmagicHTMLtoInfo(html)
		if info == "No info":
			error_cards = []
			error_cards.append(cartaMagic("N/A","N/A","N/A","N/A","N/A","Cardsmagic"))
			cards = info_to_table(error_cards)
		else:
			cards = info_to_table(info,"Euro",moeda)
	
	if "letscollect" in url:
		info = getInfo_letscollect(html)
		if info == "No info":
			error_cards = []
			error_cards.append(cartaMagic("N/A","N/A","N/A","N/A","N/A","Letscollect"))
			cards = info_to_table(error_cards)
		else:
			cards = info_to_table(info,"Real",moeda)
 
	return cards
 
#Distributor for GOOGLE
def pablo_aimar(url,moeda):

	cards = None
	
	html = httpUtils.synch_fetchURL(url)
	
	if html == 502:
		html = httpUtils.fetchURL(url)
		#Must break if unavailable
		if html == 502:
			if "cardsmagic" in url:
				error_cards = []
				error_cards.append(cartaMagic("N/A","N/A","N/A","N/A","N/A","Cardsmagic - Site Unavailable"))
				return info_to_table(error_cards)

	
	if "cardsmagic" in url:
		info = cardsmagicHTMLtoInfo(html)
		if info == "No info":
			error_cards = []
			error_cards.append(cartaMagic("N/A","N/A","N/A","N/A","N/A","Cardsmagic"))
			cards = info_to_table(error_cards)
		else:
			cards = info_to_table(info,"Euro",moeda)

	return cards
                    