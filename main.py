# -*- coding: utf-8 -*-
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import logging

#
#User Modules
#
import makeURL
import html_to_info
import dataBases


class MainHandler(webapp.RequestHandler):
	def get(self):
		template_values = {
		}

		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

class getContacts(webapp.RequestHandler):
	def get(self):
		template_values = {
		}

		path = os.path.join(os.path.dirname(__file__), 'contacts.html')
		
		self.response.out.write(template.render(path, template_values))		
		
		

class conversions(webapp.RequestHandler):
	def get(self):
		try:
			dataBases.get_currency()
		except :
			pass
		
		
class getHTML(webapp.RequestHandler):
	def post(self):
		html = self.request.get("html").encode('utf-8')
		url = str(self.request.get("url").encode('utf-8'))
		
		moeda = str(self.request.get("moeda").encode('utf-8'))
		
		info = html_to_info.rui_costa(url,html,moeda)
		self.response.out.write(info)

		
class getHTML_Exceptions(webapp.RequestHandler):
	def post(self):
		url = str(self.request.get("url").encode('utf-8'))
		
		moeda = str(self.request.get("moeda").encode('utf-8'))
		
		
		toReturn = html_to_info.pablo_aimar(url,moeda)
		
		self.response.out.write(toReturn)
		
		
import dataBases
class returnPages(webapp.RequestHandler):
	def post(self):
		allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,-' ()"
		good_card = True
		
		card = (self.request.get("card").encode('utf-8')).strip()
		
		#sanatize input
		for c in card:
			if c not in allowed_chars:
				self.response.out.write("Caracter Invalido na pesquisa")
				good_card = False
				break
		
		if good_card:
			# obtain ip address
			ip = self.request.remote_addr
		
			# E-MAIL ?
			#USER_EMAIL
		
			dataBases.add_info_cards(card,ip)
		
			toReturn = ""

			#To make the necessary links
			link0 = makeURL.card_cardsmagic_link(card)
			link1 = makeURL.card_magictuga_link(card)
			link2 = makeURL.card_viamagic_link(card)
			link3 = makeURL.card_letscollect_link(card)
		
		
			toReturn = link1 + "###" + link3 + "###" + link2 + "###" + link0 
		
			self.response.out.write(toReturn)
		

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
										 ('/contacts',getContacts),
										 ('/returnPages',returnPages),
										 ('/getHTML',getHTML),
										 ('/getHTML_Exceptions',getHTML_Exceptions),
										 ('/conversions',conversions)],
										 debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
