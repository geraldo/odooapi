from django.http import HttpResponse
import xmlrpclib

url = "https://demo3.odoo.com"
db = "demo_100_1489044950"
username = "admin"
password = "admin"

#odoo service connection
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
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