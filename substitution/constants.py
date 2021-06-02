"""
Constants that can be changed for mroe or less data
retrieved from the OFF API
"""
# Number of categories to be extracted from API, Default is 3
NBR_CAT = 3

# Number of product per category to be extracted from API, Default is 20
NBR_PROD = 10

# Number of results per page in the results page
NBR_RESULTS_PER_PAGE = 8

# ERROR: user not logged_in
NOT_LOGGED_IN = "Vous devez vous identifier pour pouvoir effectuer cette action"

# ERROR: no match for searched product in the DB
NO_PROD_FOUND = """Désolé, aucun produit de notre base de données ne correspond 
à vorte recherche\nessayez par exemple 'Nutella', ou 'produit à l'abricot'"""
