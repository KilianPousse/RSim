##
#  @file element.py
#  @brief File containing the class *Element*
#  @date 2024-10-03
#  @author Rabyte Studio

from map import Map
from math import sqrt
from random import randint

##
#  @class Element
#  @brief Class representing an element on the map
class Element:
    list = []  ##< List of all elements
    
    ##
    #  @brief Initializes an element with a position.
    #  @param coord A tuple (x, y) representing the coordinates of the element.
    #  @throws TypeError if 'coord' is not a tuple or its elements are not integers.
    #  @throws ValueError if 'coord' does not have a length of 2.
    #  @throws ValueError if x or y are out of bounds.
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    ##
    #  @brief Represents the Element as a string.
    #  @return A string representation of the element's coordinates.
    def __repr__(self) -> str:
        return f"pos=({self.x}, {self.y})"
    
    ##
    #  @brief Returns the number of elements.
    #  @return The length of the element list.
    @classmethod
    def __len__(cls):
        return len(cls.list)

    ##
    #  @brief Property getter for x-coordinate.
    #  @return The x-coordinate of the element.
    @property
    def x(self):
        return self._x

    ##
    #  @brief Property setter for x-coordinate.
    #  @param value New x-coordinate.
    #  @throws TypeError if the x-coordinate is not an integer.
    #  @throws ValueError if the x-coordinate is out of bounds.
    @x.setter
    def x(self, value):
        if not isinstance(value, int):
            raise TypeError(f"x must be an integer!")
        if not value in range(Map.size[0]):
            raise ValueError(f"x:{value} must be in [0, {Map.size[0]}[")
        self._x = value

    ##
    #  @brief Property getter for y-coordinate.
    #  @return The y-coordinate of the element.
    @property
    def y(self):
        return self._y

    ##
    #  @brief Property setter for y-coordinate.
    #  @param value New y-coordinate.
    #  @throws TypeError if the y-coordinate is not an integer.
    #  @throws ValueError if the y-coordinate is out of bounds.
    @y.setter
    def y(self, value):
        if not isinstance(value, int):
            raise TypeError(f"y must be an integer!")
        if not value in range(Map.size[1]):
            raise ValueError(f"y:{value} must be in [0, {Map.size[1]}[")
        self._y = value

    ##
    #  @brief Property getter for coordinates.
    #  @return A tuple (x, y) representing the element's coordinates.
    @property
    def coord(self):
        return self._x, self._y

    ##
    #  @brief Property setter for coordinates.
    #  @param value A tuple (x, y) representing the new coordinates.
    #  @throws TypeError if 'value' is not a tuple.
    #  @throws ValueError if 'value' does not have a length of 2.
    def coord(self, value):
        """Set the coordinates of the element with validation."""
        if not isinstance(value, tuple):
            raise TypeError(f"{value} must be a tuple!")
        if len(value) != 2:
            raise ValueError(f"{value} must have a length of 2!")
        
        self.x = value[0]  # Use the setter to validate x
        self.y = value[1]  # Use the setter to validate y

    ##
    #  @brief Creates and adds a new element to the list.
    #  @param coord A tuple (x, y) representing the coordinates of the new element.
    @classmethod
    def new(cls, coord):
        elem = Element(coord)
        cls.list.append(elem)
        return cls.len

    ##
    #  @brief Removes an element from the list.
    #  @param elem The element to remove from the list.
    @classmethod
    def delete(cls, elem):
        cls.list.remove(elem)
        return cls.len

    ##
    #  @brief Returns the number of elements.
    #  @return The length of the element list.
    @classmethod
    def len(cls) -> int:
        return len(cls.list)

    ##
    #  @brief Calculates the Euclidean distance from the element to another element.
    #  @param elem An instance of Element representing the position to which the distance is calculated.
    #  @return The Euclidean distance between the element's position and the given position.
    def distance(self, elem) -> float:
        # Calculate Euclidean distance
        dx = self.x - elem.x
        dy = self.y - elem.y
        return sqrt(dx**2 + dy**2)

    


    

if __name__ == "__main__":
    Map.size = Map.DEFAULT_SIZE
    Element.new((14, 100))
    Element.new((199, 40))
    Element.new((33, 33))
    
    # Print all elements
    print(Element.list)
    
    # Delete the second element
    Element.delete(Element.list[1])
    
    # Print the updated list of elements
    print(Element.list)
