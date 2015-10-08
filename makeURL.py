# -*- coding: utf-8 -*-
import urllib


#
#MAGICTUGA
#
def card_magictuga_link(card):
	suf = "http://www.magictuga.com/index.asp?ant=rap&estado=palavra&val="
	pref = "&procurar=Procurar"

	card = urllib.quote(card)

	card_temp1 = card.replace("%27", "%92")
	
	url = suf + card_temp1 + pref
	
	return url

#
#VIAMAGIC
#
def card_viamagic_link(card):
	suf = "http://viamagic.net/advanced_search_result.php?categories_id=&search_in_description=1&keywords="
	pref = "&x=0&y=0"
	
	card = urllib.quote(card)
	
	url = suf + card + pref
	
	return url
	
	
#
#LETSCOLLECT
#	
def card_letscollect_link(card):
	suf = "http://letscollect.com.br/ecom.aspx/Buscar/"
	
	card = urllib.quote(card)
	
	url = suf + card
	
	return url


#
#CardsMagic
#
def card_cardsmagic_link(card):
	suf = "http://cardsmagic.net/search.php?orderby=position&orderway=desc&search_query="
	pref = "&submit_search=Search"
	
	url = suf + urllib.quote(card) + pref
	
	url = url.replace(" ","%20")
	
	return url
	
	