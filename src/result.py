import sqlite3

from src.utils import logger

# Initialize SQLite database and create table if it doesn't exist
def init_db(db_path: str):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Drop the product_views table if it exists
        cursor.execute('DROP TABLE IF EXISTS product_views')

        # Create a new product_views table
        cursor.execute('''
            CREATE TABLE product_views (
                product_id TEXT PRIMARY KEY,
                completed_views INTEGER
            )
        ''')
        conn.commit()
        logger.info("Database initialized and table created.")
    except Exception as e:
        logger.error(f"Error initializing the database: {e}")
    finally:
        conn.close()

# Update the completed views for a product
def update_completed_views(db_path, product_id, increment=1):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT completed_views FROM product_views WHERE product_id = ?', (product_id,))
        result = cursor.fetchone()

        if result:
            new_count = result[0] + increment
            cursor.execute('UPDATE product_views SET completed_views = ? WHERE product_id = ?', (new_count, product_id))
            logger.debug(f"Updated completed views for {product_id}. New count: {new_count}")
        else:
            cursor.execute('INSERT INTO product_views (product_id, completed_views) VALUES (?, ?)', (product_id, increment))
            logger.debug(f"Inserted new product {product_id} with {increment} completed view(s).")

        conn.commit()
    except Exception as e:
        logger.error(f"Error updating views for {product_id}: {e}")
    finally:
        conn.close()

# Fetch all or specific product view records
def fetch_product_views(db_path, product_id=None):
    try:
        conn = sqlite3.connect(db_path)
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
