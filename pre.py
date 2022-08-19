from random import random


class Tree:
    """Дерево"""
    def __init__(self, name: str):
        self._age = 0
        self.__height = 0
        self.__name = name

    def grow(self):
        self._age += 1
        self.__height = 2 ** self._age

    def info(self) -> str:
        return f"имя {self.__name} возраст {self._age} высота {self.__height}"

class Season:
    """Сезон"""
    @staticmethod
    def get_season() -> bool:
        if random() > 0.5:
            return True
        return False

class FruitTree(Tree, Season):
    """Фруктовое дерево"""
    def __init__(self, name: str, fruit: str):
        super().__init__(name)
        self.fruit = fruit

    def get_fruit(self) -> str:
        if self._age % 2 == 0 and self.get_season():
            return "no fruits"
        return f"{self._age*2} {self.fruit}"

# tree = Tree('oak')
# tree.grow()
# print(tree.info())
# tree.grow()
# print(tree.info())

appletree = FruitTree('appletree', fruit='apple')
appletree.grow()
print(appletree.info())
print(appletree.get_fruit())
appletree.grow()
print(appletree.info())
print(appletree.get_fruit())
appletree.grow()
print(appletree.info())
print(appletree.get_fruit())
appletree.grow()
print(appletree.info())
print(appletree.get_fruit())