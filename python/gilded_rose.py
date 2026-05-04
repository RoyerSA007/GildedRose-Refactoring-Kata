# -*- coding: utf-8 -*-

# 1. Constantes
AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
CONJURED = "Conjured Mana Cake"


class ItemUpdater:
    """Clase base (Estrategia). Por defecto para ítems normales."""
    
    def __init__(self, item):
        self.item = item
        # Factor de degradación: Normal = 1, Conjured = 2
        self.degradation_factor = 1

    def update(self):
        self.update_quality()
        self.update_sell_in()
        if self.item.sell_in < 0:
            self.handle_expired()

    def update_quality(self):
        self._decrease_quality(self.degradation_factor)

    def update_sell_in(self):
        self.item.sell_in -= 1

    def handle_expired(self):
        self._decrease_quality(self.degradation_factor)

    def _increase_quality(self, amount=1):
        if self.item.quality < 50:
            self.item.quality = min(50, self.item.quality + amount)

    def _decrease_quality(self, amount):
        self.item.quality = max(0, self.item.quality - amount)


class AgedBrieUpdater(ItemUpdater):
    def update_quality(self):
        self._increase_quality()

    def handle_expired(self):
        self._increase_quality()


class SulfurasUpdater(ItemUpdater):
    def update(self):
        pass


class BackstagePassUpdater(ItemUpdater):
    def update_quality(self):
        self._increase_quality()
        if self.item.sell_in < 11:
            self._increase_quality()
        if self.item.sell_in < 6:
            self._increase_quality()

    def handle_expired(self):
        self.item.quality = 0


class ConjuredItemUpdater(ItemUpdater):
    """Refactorizado: Solo cambia el factor, usa la lógica base."""
    def __init__(self, item):
        super().__init__(item)
        self.degradation_factor = 2


class NormalItemUpdater(ItemUpdater):
    pass


class UpdaterFactory:
    _registry = {
        AGED_BRIE: AgedBrieUpdater,
        SULFURAS: SulfurasUpdater,
        BACKSTAGE_PASSES: BackstagePassUpdater,
        CONJURED: ConjuredItemUpdater
    }

    @classmethod
    def for_item(cls, item):
        updater_class = cls._registry.get(item.name, NormalItemUpdater)
        return updater_class(item)


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            UpdaterFactory.for_item(item).update()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)