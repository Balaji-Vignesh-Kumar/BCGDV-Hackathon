from flask import Blueprint, render_template, request, app
from random import random
from matching_algorithm.match_grocery_list import load_data, get_similarity_score, setup_dictionaries


mod = Blueprint('page_routes', __name__)

@mod.route('/')
def home():
    return render_template("index.html")

@mod.route('/shop/', methods=["POST"])
def shop():
    no_of_elements = 5
    products = load_data()
    product_to_aisle_mapping, aisle_to_department_mapping, product_id_to_product_name_mapping = setup_dictionaries(products)
    prices = [round(random()*20, 2) for num in range(no_of_elements)]
    total_price = round(sum(prices), 2)
    order_1 = products.sample(no_of_elements)
    outstanding_orders = [products.sample(no_of_elements) for num in range(20)]
    max_score = 0
    for order_2 in outstanding_orders:
        score = get_similarity_score(order_1,
                                     order_2,
                                     products,
                                     product_to_aisle_mapping,
                                     aisle_to_department_mapping,
                                     product_id_to_product_name_mapping)
        if score > max_score:
            max_score = score
            best_match = order_2
    return render_template("shopping-cart.html", products= order_1, prices = prices, total_price=total_price, score=max_score)

@mod.route('/checkout', methods=["GET"])
def checkout():
    score = request.args.get("score")
    return render_template("quickview.html", score=score)

@mod.route('/final/', methods=["GET", "POST"])
def final():
    return render_template("grid.html")
