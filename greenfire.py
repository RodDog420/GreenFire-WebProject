import os
from app import create_app, db
from app.models import (User, Artist, Product, ProductImage,
                        Order, OrderItem, Review, WishlistItem, DiscountCode)
from config import Config, DevConfig

_config_map = {
    'development': DevConfig,
    'production':  Config,
}
app = create_app(_config_map.get(os.environ.get('FLASK_CONFIG', 'production'), Config))


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Artist': Artist,
        'Product': Product,
        'ProductImage': ProductImage,
        'Order': Order,
        'OrderItem': OrderItem,
        'Review': Review,
        'WishlistItem': WishlistItem,
        'DiscountCode': DiscountCode,
    }


if __name__ == '__main__':
    app.run(debug=False)
