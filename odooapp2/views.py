from django.http import HttpResponse
import xmlrpclib
from odooapp2.proxy import *

url = "https://demo3.odoo.com"
db = "demo_100_1489265126"
username = "admin"
password = "admin"

#odoo service connection
#info = xmlrpclib.ServerProxy('https://demo.odoo.com/start').start()
#print info

p = ProxiedTransport()
p.set_proxy('proxy.server:3128')

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url), transport = p)
uid = common.authenticate(db, username, password, {})

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url), transport = p)
products = models.execute_kw(db, uid, password,
    'product.template', 'search_read',
    [[]],
    {'fields': ['name', 'list_price'], 'limit': 10})

for product in products:
	print product['id'], product['name'], product['list_price']

def index(request):
	html = "<html><body><h1>Odoo Products</h1>"
	for product in products:
		name = product['name'].encode("utf-8", "strict")
		html += "<div>"+name+": "+str(product['list_price'])+"</div>"
	html += "</body></html>"
	return HttpResponse(html)
