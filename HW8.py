import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute(
        "SELECT r.name,c.category,b.building, r.rating FROM restaurants r, categories c, buildings b WHERE r.category_id = c.id AND r.building_id = b.id"
    )
    info_list = []
    for i in cur.fetchall():
        dict = {}
        dict['name'] = i[0]
        dict['category'] = i[1]
        dict['building'] = i[2]
        dict['rating'] = i[3]
        info_list.append(dict)
    return info_list

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute(
        "SELECT c.category,COUNT(*) FROM restaurants r, categories c WHERE r.category_id = c.id GROUP BY c.category"
    )
    dict = {}
    for i in cur.fetchall():
        dict[i[0]] = dict.get(i, 0) + i[1]

    categories = list(dict.keys())
    val = list(dict.values())
 
    plt.barh(categories, val)
    
    plt.ylabel("Restaurant Categories")
    plt.xlabel("No. of Restaurants")
    plt.title("Types of Restaurants in South University")
    plt.tight_layout()
    plt.show()
    return dict

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT category, rating
        FROM restaurants 
        JOIN categories 
        ON restaurants.category_id = categories.id 
        GROUP BY category_id
        ORDER BY rating ASC
        """
    )
    data = cur.fetchall()
    new = {}
    for i in data:
        new[i[0]] = new.get(i, 0) + i[1]

    categories = list(new.keys())
    val = list(new.values())

    plt.barh(categories, val)
    
    plt.ylabel("Categories")
    plt.xlabel("Ratings")
    plt.title("Average Restaurant Ratings by Category")
    plt.tight_layout()
    plt.show()
    return data[-1]

#Try calling your functions here
def main():
    first = get_restaurant_data('South_U_Restaurants.db')
    second = barchart_restaurant_categories('South_U_Restaurants.db')
    third = highest_rated_category('South_U_Restaurants.db')

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
