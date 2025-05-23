from sqlite3 import connect

from src.utils import logger

# Updated database initialization
def init_db(db_path: str, product_id_list: list):
    try:
        conn = connect(db_path)
        cursor = conn.cursor()

        # Drop the product_views table if it exists
        cursor.execute('DROP TABLE IF EXISTS product_views')

        # Create a new product_views table with both completed and failed views
        cursor.execute('''
            CREATE TABLE product_views (
                product_id TEXT PRIMARY KEY,
                completed_views INTEGER,
                failed_views INTEGER
            )
        ''')
        conn.commit()
        logger.info("Database initialized and table created.")

        # Insert product IDs from the list into the table with completed_views and failed_views initialized to 0
        for product_id in product_id_list:
            cursor.execute('INSERT INTO product_views (product_id, completed_views, failed_views) VALUES (?, ?, ?)', (product_id, 0, 0))
            logger.debug(f"Inserted product {product_id} with 0 completed.")

        # Commit the changes to the database
        conn.commit()
        logger.info("All product IDs inserted successfully.")

    except Exception as e:
        logger.error(f"Error initializing the database and inserting products: {e}")
    finally:
        conn.close()


# Update the completed or failed views for a product
def update_completed_views(db_path, product_id, increment=1, failed=False):
    try:
        conn = connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT completed_views, failed_views FROM product_views WHERE product_id = ?', (product_id,))
        result = cursor.fetchone()

        if result:
            completed_views, failed_views = result
            if failed:
                new_failed_count = failed_views + increment
                cursor.execute('UPDATE product_views SET failed_views = ? WHERE product_id = ?', (new_failed_count, product_id))
                logger.debug(f"Updated failed views for {product_id}. New count: {new_failed_count}")
            else:
                new_completed_count = completed_views + increment
                cursor.execute('UPDATE product_views SET completed_views = ? WHERE product_id = ?', (new_completed_count, product_id))
                logger.debug(f"Updated completed views for {product_id}. New count: {new_completed_count}")
        else:
            if failed:
                cursor.execute('INSERT INTO product_views (product_id, completed_views, failed_views) VALUES (?, ?, ?)', (product_id, 0, increment))
                logger.debug(f"Inserted new product {product_id} with {increment} failed view(s).")
            else:
                cursor.execute('INSERT INTO product_views (product_id, completed_views, failed_views) VALUES (?, ?, ?)', (product_id, increment, 0))
                logger.debug(f"Inserted new product {product_id} with {increment} completed view(s).")

        conn.commit()
    except Exception as e:
        logger.error(f"Error updating views for {product_id}: {e}")
    finally:
        conn.close()

# Fetch all or specific product view records
def fetch_product_views(db_path, product_id=None) -> list:
    try:
        conn = connect(db_path)
        cursor = conn.cursor()

        if product_id:
            cursor.execute('SELECT * FROM product_views WHERE product_id = ?', (product_id,))
            result = cursor.fetchone()
            if result:
                logger.info(f"Fetched views for product {product_id}: {result[1]} views.")
            else:
                logger.info(f"No record found for product {product_id}.")
        else:
            cursor.execute('SELECT * FROM product_views')
            result = cursor.fetchall()
            logger.info("Fetched all product view records.")
        
        return result
    except Exception as e:
        logger.error(f"Error fetching product views: {e}")
        return None
    finally:
        conn.close()

def reset_failed_views(db_path, product_id=None):
    """
    Resets the failed view count to 0 in the database for all products or a specific product.

    Args:
        db_path (str): The path to the SQLite database file.
        product_id (str): (Optional) The product ID to reset failed views for. If None, reset for all products.
    """
    try:
        conn = connect(db_path)
        cursor = conn.cursor()

        if product_id:
            # Reset the failed views count for a specific product
            cursor.execute('UPDATE product_views SET failed_views = 0 WHERE product_id = ?', (product_id,))
            logger.info(f"Reset failed views for product {product_id}.")
        else:
            # Reset the failed views count for all products
            cursor.execute('UPDATE product_views SET failed_views = 0')
            logger.info(f"Reset failed views for all products.")
        
        # Commit the changes
        conn.commit()
    except Exception as e:
        logger.error(f"Error resetting failed views: {e}")
    finally:
        conn.close()
