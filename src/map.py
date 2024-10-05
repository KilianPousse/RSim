from random import randint

##
#  @file map.py
#  @brief File containing the class *Map*
#  @date 2024-10-03
#  @author Rabyte Studio

##
#  @class Map
#  @brief Class representing a map of simulation
class Map:
    MAX_SIZE = 500  ##< Maximum allowed size for the map.
    DEFAULT_SIZE = (200, 150)  ##< Default size of the map.
    _size = DEFAULT_SIZE  ##< Internal storage for the size.

    ##
    #  @brief Property getter for the size of the map.
    #  @return A tuple representing the current size of the map.
    @property
    def size(self):
        """Getter for the size."""
        return self._size

    ##
    #  @brief Property setter for the size of the map.
    #  @param value A tuple of two integers representing the new size.
    #  @throws ValueError if the size is not a tuple of two integers.
    #  @throws TypeError if either dimension is not an integer.
    #  @throws ValueError if any dimension is out of bounds.
    @size.setter
    def size(self, value):
        """Setter for the size with validation."""
        # Check that the size is a tuple of two integers
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError("Size must be a tuple of two integers.")
        
        if not all(isinstance(dim, int) for dim in value):
            raise TypeError("Both dimensions of size must be integers.")
        
        # Check that each dimension is within the specified limits
        if not value[0] in range(self.MAX_SIZE) or not value[1] in range(self.MAX_SIZE):
            raise ValueError(f"Size dimensions must be between 0 and {self.MAX_SIZE} inclusive.")
        
        self._size = value
    
    @classmethod
    def rmdCoord(cls, datas=[]):

        if (Map.size[0] * Map.size[1]) > len(datas):

            while True:
                x = randint(0, Map.size[0] - 1)  # Adjust range to avoid index out of bounds
                y = randint(0, Map.size[1] - 1)
                coord = (x, y)
                
                # Vérifie si les coordonnées générées sont déjà présentes dans les objets de `datas`
                if not any(getattr(obj, 'x', None) == x and getattr(obj, 'y', None) == y for obj in datas):
                    return coord
        return None


    



if __name__ == "__main__":
    Map.size = Map.DEFAULT_SIZE
    