from typing import Tuple, Dict, List
import pandas as pd

def load_data() -> Tuple[pd.DataFrame]:
    products_dataframe = pd.read_csv('grocery_data/healthy_products.csv')
    return products_dataframe

def setup_dictionaries(products_dataframe: pd.DataFrame) -> Tuple[Dict]:
    """
    """
    product_to_aisle_mapping = {}
    aisle_to_department_mapping = {}
    product_id_to_product_name_mapping = {}

    for index, row in products_dataframe.iterrows():
        product_id_to_product_name_mapping[row['product_id']] = row['product_name']
        product_to_aisle_mapping[row['product_id']] = row['aisle_id']
        aisle_to_department_mapping[row['aisle_id']] = row['department_id']

    return product_to_aisle_mapping, aisle_to_department_mapping, product_id_to_product_name_mapping

def get_similarity_score(order_1: List, order_2: List,
                        products_dataframe: pd.DataFrame,
                        product_to_aisle_mapping: Dict,
                        aisle_to_department_mapping: Dict,
                        product_id_to_product_name_mapping: Dict) -> float:
    """
    Compares two orders to generate a similarity score

    Flow:

    Two orders are compared and the no of exact product matches are counted and scored.
    Then those matching products are removed from both lists, and the unmatched products
    are located are identified. The number of common aisles are counted and scored.
    Then the common aisles are removed from both lists, and aisles belonging to the same department are identified.
    No of common departments are counted and scored.

    The aggregate score will be a combination of product-level match, aisle-level match and department-level match
    """

    get_product_number = lambda order: set(order['product_id'])
    get_aisle_number = lambda products: set(map(lambda product_id: product_to_aisle_mapping[product_id], products))
    get_department_number = lambda aisles: set(map(lambda aisle_id: aisle_to_department_mapping[aisle_id], aisles))
    get_product_names = lambda products: set(map(lambda product_id: product_id_to_product_name_mapping[product_id], products))

    products_1 = get_product_number(order_1)
    products_2 = get_product_number(order_2)
    max_score = max(len(products_1), len(products_2))
    common_products = products_1 & products_2

    product_similarity_score = len(common_products)/max_score

    products_1 = products_1 - common_products
    products_2 = products_2 - common_products

    if len(products_1) == 0 or len(products_2) == 0:
        return 100*product_similarity_score

    aisle_1 = get_aisle_number(products_1)
    aisle_2 = get_aisle_number(products_2)

    common_aisles = aisle_1 & aisle_2
    aisle_similarity_score = len(common_aisles) / max_score
    aisle_1 = aisle_1 - common_aisles
    aisle_2 = aisle_2 - common_aisles

    if len(aisle_1) == 0 or len(aisle_2) == 0:
        return 100*product_similarity_score + 95*aisle_similarity_score

    department_1 = get_department_number(aisle_1)
    department_2 = get_department_number(aisle_2)

    common_departments = department_1 & department_2
    department_similarity_score = len(common_departments) / max_score

    final_score = 100*product_similarity_score + 95*aisle_similarity_score + 90*department_similarity_score

    return final_score
