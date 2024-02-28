from Db_Manager import DbManager
import mysql.connector
import json
class Products:
    
    def __init__(self,id,nome,prezzo,marca):
        self.id=id
        self.nome=nome
        self.prezzo=prezzo
        self.marca=marca
        
    @staticmethod
    def connector():
        try:
            #db_manager = db_manager("198.168.2.200", 3306, "cavallini_marisol", "Cepheid.battlegrounds.hilaritys.", "cavallini_marisol_ecommerce")#modifica con dati del databse di dbeaver 
            db_manager = DbManager("127.0.0.1", 3306, "mari", "ecom123!", "Ecommerce_products")
            conn = db_manager.connect()
            return conn
        except mysql.connector.Error as e:
            print("Errore durante la connessione al database:", str(e))
    
    @staticmethod
    def create(params):
        conn=Products.connector()
        cursor = conn.cursor()#consente di eseguire query SQL e interagire con il database
        cursor.execute('INSERT INTO products (nome, prezzo, marca) VALUES (%s, %s, %s)',
                       (params['nome'], params['prezzo'], params['marca']))
        product_id=cursor.lastrowid
        conn.commit()#Conferma le modifiche apportate al database
        params['id'] =product_id
        conn.close()
        return params
    
    @staticmethod
    def Find_all():
        conn = Products.connector()
        cursor = conn.cursor()#consente di eseguire query SQL e interagire con il database
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()#recupera tutte le righe 
        conn.close()
        return rows

    def update(self,updated_product):
        conn = Products.connector()
        cursor = conn.cursor()#consente di eseguire query SQL e interagire con il database
        cursor.execute('UPDATE products SET nome=%s, prezzo=%s, marca=%s WHERE id=%s',
                       (updated_product['nome'],updated_product['prezzo'],updated_product['marca'],self.id))
        conn.commit()#conferma le modifiche apportate al database
        conn.close()
        return updated_product

    @staticmethod
    def find(id):
        conn = Products.connector()
        cursor = conn.cursor()#consente di eseguire query SQL e interagire con il database
        cursor.execute('SELECT * FROM products WHERE id = %s', (id,))
        row = cursor.fetchone()#recupera una singola riga
        conn.close()
        if row is not None:
            return Products(id=row[0],nome=row[1],prezzo=row[2],marca=row[3])
        else:
            return None
    
    def delete(self):
        conn = Products.connector()
        cursor = conn.cursor()#consente di eseguire query SQL e interagire con il database
        cursor.execute('DELETE FROM products WHERE id=%s', (self.id,))
        conn.commit()#conferma le modifiche apportate al database
        conn.close()
        
                 
    def get_id(self):
        return self.id
    
    def set_nome(self,nome):
        self._nome=nome
    
    def get_nome(self):
        return self._nome
    
    def set_prezzo(self,prezzo):
        self._prezzo=prezzo
    
    def get_prezzo(self):
        return self._prezzo
    
    def set_marca(self,marca):
        self._marca=marca
    
    def get_marca(self):
        return self._marca

        