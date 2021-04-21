There is a specific manage.py command to drop the 3 following tables from database:
 - Product 
 - Favorites 
 - Categories

**USE WITH CAUTION, DATA CAN BE LOST USING THIS**
if you want to erase the three above table, please use:

    python manage.py resetdb

To import a new batch of products in the database you can use the following command:

    python manage.py fetch_api_data