class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        p_id = str(product_id)
        if p_id not in self.cart:
            self.cart[p_id] = {'quantity': 0}
        self.cart[p_id]['quantity'] += quantity
        self.save()

    def remove(self, product_id):
        p_id = str(product_id)
        if p_id in self.cart:
            del self.cart[p_id]
            self.save()

    def update_quantity(self, product_id, quantity):
        """
        Изменяет количество товара.
        Если quantity <= 0 — удаляет товар.
        """
        p_id = str(product_id)
        if p_id in self.cart:
            if quantity > 0:
                self.cart[p_id]['quantity'] = quantity
            else:
                del self.cart[p_id]
            self.save()

    def save(self):
        print("Сохраняем корзину:", self.cart)
        self.session['cart'] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_items(self):
        """Возвращает общее количество всех товаров в корзине (для бейджа)"""
        return sum(item['quantity'] for item in self.cart.values())

    def __len__(self):
        """Чтобы можно было использовать len(cart)"""
        return self.get_total_items()

    def __iter__(self):
        """Для удобного перебора товаров в шаблоне"""
        for p_id, data in self.cart.items():
            yield {
                'product_id': p_id,
                'quantity': data['quantity'],
                # Если позже добавишь продукт в сессию — здесь можно будет его подгружать
            }