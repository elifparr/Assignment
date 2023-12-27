import sqlite3 as sql
from flask import Flask,redirect, render_template, request, url_for




app = Flask(__name__,static_url_path='/static')

def initDB():
    conn = sql.connect('database.db')
    print("Opened database successfully")   
    
    conn.execute('ALTER TABLE products ADD COLUMN image_path TEXT')
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, Gender Text,Brand TEXT,Category Text, description TEXT, price INTEGER, image_path TEXT)')
    print("Table created successfully")
    

    
    conn.commit()
    conn.close()

def get_products():
    conn = sql.connect('database.db')
    cursor = conn.execute("SELECT id,Gender,Brand,Category,description, price, image_path FROM products")
    products = cursor.fetchall()
    conn.close()
    return products


def get_product_by_id(product_id):
    conn = sql.connect('database.db')
    cursor = conn.execute("SELECT id, Gender, Brand, Category, description, price, image_path FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if product:
        # Convert the result to a dictionary for easier access in the template
        product_dict = {
            'id': product[0],
            'Gender': product[1],
            'Brand': product[2],
            'Category': product[3],
            'description': product[4],
            'price': product[5],
            'image_path': product[6],
        }
        return product_dict
    else:
        # Return None if the product is not found
        return None



@app.route('/home')
def home_page():
    products = get_products()
    return render_template('home.html', products=products)

@app.route('/initialize')
def initialize():
    # Call the initDB function to initialize the database and insert the first element
    initDB()
    return redirect(url_for('home_page'))

@app.route('/detail/<int:id>', methods = ['GET'])
def detail(id):
    if request.method == 'GET':
        try:

         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT FROM products WHERE Id = ?",(id) )
            
            con.commit()
            con.close() 
        finally:
            product = get_product_by_id(id)
            

            
            return render_template('detail.html', product=product)

@app.route('/woman')
def woman_page():
    products = get_products()
    return render_template('woman.html', products=products)  

@app.route('/man')
def man_page():
    products = get_products()
    return render_template('man.html', products=products)  

@app.route('/children')
def children_page():
    products = get_products()
    return render_template('children.html', products=products)  

@app.route('/starbutik')
def starbutik_page():
    products = get_products()
    return render_template('starbutik.html', products=products)  

@app.route('/manclub')
def manclub_page():
    products = get_products()
    return render_template('manclub.html', products=products) 
 
@app.route('/littlethings')
def littlethings_page():
    products = get_products()
    return render_template('littlethings.html', products=products) 

@app.route('/search', methods=['GET'])
def search_results():
    query = request.args.get('q', '')

    conn = sql.connect('database.db')
    cursor = conn.cursor()

    
    cursor.execute("""
        SELECT * FROM products
        WHERE Brand LIKE ? OR Category LIKE ? OR description LIKE ? OR Gender LIKE ? OR price LIKE ?
    """, ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))

    results = cursor.fetchall()

    conn.close()

    return render_template('search.html', results=results)



if __name__ == "__main__":
    app.run(debug=Trueport=5001)