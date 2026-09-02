class InsufficientStockError(Exception):
    def __init__(self, menu_item_name, available_quantity):
        self.menu_item_name = menu_item_name
        self.available_quantity = available_quantity
        super().__init__(
            f"Apenas {available_quantity} unidades disponíveis para {menu_item_name}."
        )