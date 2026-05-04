# -*- coding: utf-8 -*-

# 1. Extracción de Constantes (Globales para fácil acceso en toda la lógica)
AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"


class ItemUpdater:
    """Clase base (Estrategia) para la actualización de ítems."""
    def __init__(self, item):
        self.item = item

    def update(self):
        """Método de orquestación (Template Method simplificado)"""
        self.update_quality()
        self.update_sell_in()
        if self.item.sell_in < 0:
            self.handle_expired()

    def update_quality(self):
        """Lógica por defecto para ítems normales"""
        if self.item.quality > 0:
            self.item.quality -= 1

    def update_sell_in(self):
        self.item.sell_in -= 1

    def handle_expired(self):
        if self.item.quality > 0:
            self.item.quality -= 1

    def _increase_quality(self):
        """Método utilitario privado para subclases"""
        if self.item.quality < 50:
            self.item.quality += 1


class AgedBrieUpdater(ItemUpdater):
    def update_quality(self):
        self._increase_quality()

    def handle_expired(self):
        self._increase_quality()


class SulfurasUpdater(ItemUpdater):
    def update(self):
        # Cláusula de guarda definitiva: No hace nada
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


class NormalItemUpdater(ItemUpdater):
    """Mantiene el comportamiento base de ItemUpdater"""
    pass


class UpdaterFactory:
    """Fabrica la estrategia adecuada con un registro centralizado."""
    
    # Registro que mapea nombres de ítems a sus clases actualizadoras
    _registry = {
        AGED_BRIE: AgedBrieUpdater,
        SULFURAS: SulfurasUpdater,
        BACKSTAGE_PASSES: BackstagePassUpdater
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
            # Delegación total: GildedRose ya no conoce las reglas del negocio
            UpdaterFactory.for_item(item).update()


class Item:
    """Restricción: No modificada."""
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)