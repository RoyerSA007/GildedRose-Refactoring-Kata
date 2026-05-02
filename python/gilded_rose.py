# -*- coding: utf-8 -*-

class GildedRose(object):
    # --- Constantes para evitar "Magic Strings" ---
    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            self._update_item_status(item)

    def _update_item_status(self, item):
        """Orquesta la actualización de un ítem según su nombre."""
        if item.name == self.SULFURAS:
            return  # Sulfuras no cambia nunca

        if item.name == self.AGED_BRIE:
            self._update_aged_brie(item)
        elif item.name == self.BACKSTAGE_PASSES:
            self._update_backstage_pass(item)
        else:
            self._update_normal_item(item)

        # Reducción del tiempo de venta para todos excepto Sulfuras
        item.sell_in -= 1

        # Lógica post-vencimiento
        if item.sell_in < 0:
            self._handle_expired_item(item)

    # --- Métodos Privados de Lógica Específica ---

    def _update_aged_brie(self, item):
        if item.quality < 50:
            item.quality += 1

    def _update_backstage_pass(self, item):
        if item.quality < 50:
            item.quality += 1
            if item.sell_in < 11 and item.quality < 50:
                item.quality += 1
            if item.sell_in < 6 and item.quality < 50:
                item.quality += 1

    def _update_normal_item(self, item):
        if item.quality > 0:
            item.quality -= 1

    def _handle_expired_item(self, item):
        """Define qué pasa cuando sell_in < 0."""
        if item.name == self.AGED_BRIE:
            if item.quality < 50:
                item.quality += 1
        elif item.name == self.BACKSTAGE_PASSES:
            item.quality = 0
        else:
            if item.quality > 0:
                item.quality -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)