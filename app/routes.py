from flask import Blueprint, render_template, request, jsonify
from .db import get_db

main = Blueprint('main', __name__)


def execute_query(query, params=None):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    data = cursor.fetchall()
    cursor.close()
    return data


# Page Routes
@main.route('/')
def home():
    return render_template('home.html')


@main.route('/add_product_page')
def add_product_page():
    return render_template('add_product.html')


@main.route('/get_inventory_page')
def get_inventory_page():
    return render_template('get_inventory.html')


@main.route('/update_price_page')
def update_price_page():
    return render_template('update_price.html')


@main.route('/delete_item_page')
def delete_item_page():
    return render_template('delete_item.html')


@main.route('/view_queries_page')
def view_queries_page():
    return render_template('view_queries.html')


# Query Endpoints
@main.route('/top_revenue_items', methods=['GET'])
def top_revenue_items():
    data = execute_query(
        "SELECT Iname, TotalRevenue FROM ItemSalesSummary ORDER BY TotalRevenue DESC LIMIT 3;"
    )
    return jsonify(data)


@main.route('/top_selling_items', methods=['GET'])
def top_selling_items():
    data = execute_query(
        "SELECT Iname, TotalQuantitySold FROM ItemSalesSummary WHERE TotalQuantitySold > 50;"
    )
    return jsonify(data)


@main.route('/top_loyal_customer', methods=['GET'])
def top_loyal_customer():
    data = execute_query(
        "SELECT Cname, LoyaltyScore FROM TopLoyalCustomers ORDER BY LoyaltyScore DESC LIMIT 1;"
    )
    return jsonify(data)


@main.route('/loyal_customers_range', methods=['GET'])
def loyal_customers_range():
    data = execute_query(
        "SELECT Cname, LoyaltyScore FROM TopLoyalCustomers WHERE LoyaltyScore BETWEEN 4 AND 5 ORDER BY LoyaltyScore DESC;"
    )
    return jsonify(data)


@main.route('/total_revenue', methods=['GET'])
def total_revenue():
    data = execute_query(
        "SELECT SUM(TotalRevenue) AS TotalStoreRevenue FROM ItemSalesSummary;"
    )
    return jsonify(data)


# CRUD Endpoints
@main.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Upsert vendor
        cursor.execute(
            """
            INSERT INTO vendor (vId, Vname, Street, City, StateAb, ZipCode)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE Vname=VALUES(Vname), Street=VALUES(Street), City=VALUES(City), StateAb=VALUES(StateAb), ZipCode=VALUES(ZipCode);
            """, (
                data['vId'], data['Vname'], data['Street'],
                data['City'], data['StateAb'], data['ZipCode']
            )
        )

        # Insert item
        cursor.execute(
            "INSERT IGNORE INTO item (iId, Iname, Sprice, Category) VALUES (%s, %s, %s, %s);",
            (data['iId'], data['Iname'], data['Sprice'], data['Category'])
        )

        # Insert store_item
        cursor.execute(
            "INSERT INTO store_item (sId, iId, Scount) VALUES (%s, %s, %s) ",
            (data['sId'], data['iId'], data['Scount'])
        )

        conn.commit()
        return jsonify(message='Product added successfully!'), 201
    except Exception as e:
        return jsonify(error=str(e)), 500


@main.route('/get_inventory/<int:store_id>', methods=['GET'])
def get_inventory(store_id):
    data = execute_query(
        """
        SELECT i.Iname, i.Sprice, si.Scount
        FROM item i JOIN store_item si ON i.iId = si.iId
        WHERE si.sId = %s;
        """, (store_id,)
    )
    return jsonify(data)


@main.route('/update_price/<int:item_id>', methods=['PUT'])
def update_price(item_id):
    new_price = request.get_json().get('Sprice')
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE item SET Sprice = %s WHERE iId = %s;",
            (new_price, item_id)
        )
        conn.commit()
        return jsonify(message='Price updated successfully!')
    except Exception as e:
        return jsonify(error=str(e)), 500


@main.route('/delete_item/<int:iId>', methods=['DELETE'])
def delete_item(iId):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT vId FROM vendor_item WHERE iId = %s;", (iId,))
        vendors = cursor.fetchall()
        cursor.execute("DELETE FROM store_item WHERE iId = %s;", (iId,))
        cursor.execute("DELETE FROM vendor_item WHERE iId = %s;", (iId,))
        cursor.execute("DELETE FROM item WHERE iId = %s;", (iId,))
        for (vId,) in vendors:
            cursor.execute("SELECT COUNT(*) FROM vendor_item WHERE vId = %s;", (vId,))
            remaining = cursor.fetchone()[0]
            if remaining == 0:
                cursor.execute("DELETE FROM vendor_store WHERE vId = %s;", (vId,))
                cursor.execute("DELETE FROM vendor WHERE vId = %s;", (vId,))

        conn.commit()
        return jsonify({
            'message': 'Item deleted and orphaned vendor (plus store links) cleaned up.'
        }), 200
        conn.commit()
        return jsonify(message='Item and associated vendor deleted successfully!')
    except Exception as e:
        return jsonify(error=str(e)), 500
