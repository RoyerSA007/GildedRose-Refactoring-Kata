import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    
    # --- 1. ÍTEMS NORMALES ---
    def test_normal_item_degrades_quality_by_one(self):
        items = [Item("Producto Equis", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 19)

    def test_normal_item_degrades_sell_in_by_one(self):
        items = [Item("Producto Equis", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].sell_in, 9)

    def test_normal_item_quality_never_negative(self):
        items = [Item("Producto Equis", 10, 0)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 0)

    # --- 2. ÍTEMS NORMALES (CADUCADOS) ---
    def test_normal_item_degrades_double_after_sell_in(self):
        items = [Item("Producto Equis", 0, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 18)

    # --- 3. AGED BRIE (EL QUESO) ---
    def test_aged_brie_increases_quality(self):
        items = [Item("Aged Brie", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 21)

    def test_aged_brie_quality_max_50(self):
        items = [Item("Aged Brie", 10, 50)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 50)

    # --- 4. SULFURAS (EL LEGENDARIO) ---
    def test_sulfuras_never_changes_quality(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 10, 80)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 80)

    def test_sulfuras_never_changes_sell_in(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 10, 80)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].sell_in, 10)

    # --- 5. BACKSTAGE PASSES (LOS TICKETS) ---
    def test_backstage_passes_increase_normally(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 21)

    def test_backstage_passes_increase_by_2_when_10_days_left(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 22)

    def test_backstage_passes_increase_by_3_when_5_days_left(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 23)

    def test_backstage_passes_drop_to_zero_after_concert(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 0)

    
    # --- 6. CONJURED ITEMS (LOS INVOCADOS) ---
    def test_conjured_item_degrades_double_speed(self):
        # Baja 2 en lugar de 1
        items = [Item("Conjured Mana Cake", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 18)

    def test_conjured_item_degrades_double_speed_after_sell_in(self):
        # Baja 4 en lugar de 2 (el doble de un ítem normal caducado)
        items = [Item("Conjured Mana Cake", 0, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 16)

    def test_conjured_item_quality_never_negative(self):
        items = [Item("Conjured Mana Cake", 10, 1)]
        GildedRose(items).update_quality()
        self.assertEqual(items[0].quality, 0)

if __name__ == "__main__":
    unittest.main()