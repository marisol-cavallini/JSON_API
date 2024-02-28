import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from Product import Products


class RequestHandler(BaseHTTPRequestHandler):
    
    def _set_response(self, status_code=200, content_type='application/json'): #imposta la risposta HTTP
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    
    def do_GET(self):
        if self.path == '/products': #percorso per chiamare metodo che mostra tutti i prodotti
            self.get_products()
        elif self.path.startswith('/products/'): #percorso che chiamare metodo che mostra il prodotto del id richiesto
            parts = self.path.split('/')
            product_id = int(parts[2])
            self.get_product(product_id)
        else:
            self.send_error(404, 'Not Found')
            

    def get_products(self): #ottiene tutti i prodotti 
        records = Products.Find_all()
        products_list = []
        # Itera su ogni record e formatta i dati del prodotto
        for r in records:
            product={
                "type":"products",
                "id":str(r[0]),
                "attributes":{
                    "nome":r[1],
                    "prezzo":r[2],
                    "marca":r[3]
                }
            }
            products_list.append(product) #aggiunge il prodotto alla lista
        #imposta la risposta 
        self._set_response()
        self.end_headers()
        self.wfile.write(json.dumps({'data': products_list}).encode('utf-8'))
    #ottiene un prodotto specifico in base all'ID fornito 
    def get_product(self, product_id):
        product = Products.find(product_id)
        if product is not None: #se lo trova formata i suoi dati
            product_dict = {"data":{
                 "type":"products",
                 "id" : str(product.id),
                "attributes":{
                    'nome':product.nome,
                    'prezzo': product.prezzo,
                    'marca': product.marca
                }
            }}
            self._set_response()
            self.wfile.write(json.dumps(product_dict).encode('utf-8'))
        else:
            self.send_error(404, 'Product Not Found')
    
    def do_POST(self):
        if self.path == '/products':
            #legge lunghezza del contenuto e i dati della richiesta
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.Create(post_data)
        else:
            self.send_error(404, 'Not Found')
    #crea nuovo prodotto con i dati forniti nella richiesta 
    def Create(self, post_data): 
        try:
            data = json.loads(post_data.decode('utf-8'))#decodifica i dati Json dalla richiesta 
            if 'data' not in data or 'attributes' not in data['data']:
                self.send_error(400, 'Bad Request - Incomplete Data')
                return
            attributes = data['data']['attributes']# Estrae gli attributi del prodotto dalla struttura dei dati
            # Verifica se gli attributi richiesti sono presenti
            if 'nome' not in attributes or 'prezzo' not in attributes or 'marca' not in attributes:
                self.send_error(400, 'Bad Request - Incomplete Data')
                return
            # Verifica se il tipo di dato per 'prezzo' è valido (int o float)
            if not isinstance(attributes['prezzo'], (int, float)):
                self.send_error(400, 'Bad Request - Invalid Data Type for "prezzo"')
                return
            # Crea un nuovo prodotto con gli attributi forniti
            new_product = {
                'nome': attributes['nome'],
                'prezzo': attributes['prezzo'],
                'marca': attributes['marca']
            }
            product = Products.create(new_product)#richiama metodo create
            # Formatta la risposta con i dati del nuovo prodotto creato
            response = {
                "data": {
                    "type": "products",
                    "id": str(product['id']),
                "attributes": {
                    'nome': product['nome'],
                    'prezzo': product['prezzo'],
                    'marca': product['marca']
                    }
                }
            }
            self._set_response(status_code=201)
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, 'Bad Request - Invalid JSON')

    
    def do_DELETE(self):
        if self.path.startswith('/products/'):#controlla percorso
            parts = self.path.split('/')
            product_id = int(parts[2])
            product = Products.find(product_id)#cerca prodotto
            if product:
                self.Delete(product)#richiamo metodo
            else:
                self.send_error(404, 'Product Not Found')
        else:
            self.send_error(404, 'Not Found')

    def Delete(self, product):#elimina prodotto
        try:
            product.delete()
            self._set_response(status_code=204) 
        except Exception as e:
            import traceback
            traceback.print_exception(e)#stampa informazioni di traccia e restituisce un errore 500
            self.send_error(500, f'Internal Server Error: {str(e)}') 
    
    def do_PATCH(self):
        if self.path.startswith('/products/'):#controlla il percorso
            parts = self.path.split('/')
            product_id = int(parts[2])
            product = Products.find(product_id)#cerca prodotto
            if product:
                #legge la lunghezza del contenuto e i dati della richiesta
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                self.Update(post_data,product)#chiama metodo per aggiornare
            else:
                self.send_error(404, 'Product Not Found')
        else:
            self.send_error(404, 'Not Found')
            
    def Update(self,post_data,product):
        data = json.loads(post_data.decode('utf-8'))#decodifica i dati 
        # Aggiorna il prodotto con gli attributi forniti nei dati della richiesta
        product.update(data["data"]["attributes"])
        # Formatta la risposta con i dati aggiornati del prodotto
        product_dict = {"data":{
                "type":"products",
                "id" : str(product.id),
            "attributes":{
                'nome':product.nome,
                'prezzo': product.prezzo,
                'marca': product.marca
            }
        }}
        self._set_response()
        self.wfile.write(json.dumps(product_dict).encode('utf-8'))# Scrive la risposta al client nel formato JSON
#avvia il server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8081):
    server_address = ('', port)#imposta l'indirizzo e la porta
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()#inizia ad ascoltare le richieste HTTP

if __name__ == '__main__':
    run()