from app import create_app, db
from app.models import (User, Artist, Product, ProductImage,
                        Order, OrderItem, Review, WishlistItem, DiscountCode)

app = create_app()


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
        'DiscountCode': DiscountCode
    }


if __name__ == '__main__':
    app.run(debug=True)
