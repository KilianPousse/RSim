## 
#  @file save.py
#  @brief File containing the class *Save*.
#  @date 2024-10-04
#  @author Rabyte Studio
import struct
from entity import Entity
from food import Food
from map import Map
from time import time, sleep 
from shutil import copy
import path


## 
#  @class Save
#  @brief Class for saving and loading simulation states to and from binary files.
class Save:

    _dir = path.PATH_SAVES   ##< Directory for save files
    _backup = path.PATH_BACKUPS   
    _name = 'save_'         ##< Base name for save files

    NBYTES_TIME = 8     ##< Number of bytes for time in the binary representation
    NBYTES_COORD = 2    ##< Number of bytes for coordinates in the binary representation

    TIME_MAX = 2 ** (NBYTES_TIME * 8)  ##< Maximum time value

    TIME_IN_AGE = 40

    ## 
    #  @brief Initializes the Save object.
    #  @param numSave An integer representing the save file number (default is 0).
    def __init__(self, numSave=0) -> None:
        self.number = numSave   ##< Save file number
        self.last = 0           ##< Last loading timestamp
        self.time = 0   
        self.path = Save._dir / (Save._name + str(self.number))     

        # Create the save directory if it doesn't exist
        Save._dir.mkdir(parents=True, exist_ok=True) 
        # Create the backup directory if it doesn't exist
        Save._backup.mkdir(parents=True, exist_ok=True)   

        self.starting = int(time())  

    ## 
    #  @brief Returns a string representation of the Save object.
    #  @return A string containing save file path, last loading time, current time, and entities/food lists.
    def __repr__(self) -> str:
        return (f"Save_{str(self.number)}: path='{self.path}'\n"+
                f"last_loading={self.last}, time={self.time}, age={self.age}\n"+
                f"\nEntities:{Entity.list}\n"+
                f"\nFoods:{Food.list}\n"
                )

    ## 
    #  @brief Gets the current simulation time.
    #  @return The current time as an integer.
    @property
    def time(self):
        return self._time

    ##
    #  @brief Sets the current simulation time.
    #  @param value An integer representing the time to set.
    #  @throws TypeError if the value is not an integer.
    #  @throws ValueError if the value is out of range.
    @time.setter
    def time(self, value):
        if not isinstance(value, int):
            raise TypeError("time must be an integer!")
        if value not in range(Save.TIME_MAX):
            self._time = -1
            self._energy = 0
            self._age = 0  
        else:
            self._time = value
            self._age = self.time // self.TIME_IN_AGE  # Calculate age based on time.

    ## 
    #  @brief Gets the current age based on simulation time.
    #  @return The calculated age as an integer.
    @property
    def age(self):
        return self._age 

    ## 
    #  @brief Saves the current simulation state to a binary file.
    #  @throws IOError if file operations fail.
    #  @throws ValueError if a value exceeds its byte limits.
    def save(self):
        try:
            stop = int(time())
            timestamp = str(stop)
            backup_path = Save._backup / (Save._name + f"{self.number}.bak")
            copy(str(self.path), backup_path) 
        except:
            stop = int(time())

        try:
            # Open the file for writing in binary mode
            with open(self.path, 'wb') as file:        
                self._write_int(file, Save.NBYTES_TIME, stop, 'file.last_loading')
                self._write_int(file, Save.NBYTES_TIME, self.time + ( stop - self.starting ), 'file.sim_time')
                self._write_int(file, Save.NBYTES_COORD, Map.size[0], 'map.size_x')
                self._write_int(file, Save.NBYTES_COORD, Map.size[1], 'map.size_y')

                self._write_food(file)
                self._write_entity(file)
                
        except IOError as e:
            raise IOError(f"File error: {e}")
        except ValueError as e:
            raise ValueError(f"Value error: {e}")
        except Exception as e:
            raise Exception(f"Failed to save: {e}")

    ## 
    #  @brief Writes an integer value to a binary file.
    #  @param file The file object to write to.
    #  @param size Number of bytes for the integer.
    #  @param value The integer value to write.
    #  @param name Optional parameter for the value's name (used for error messages).
    #  @throws ValueError if value does not fit in the specified byte size.
    def _write_int(self, file, size, value, name="value"):
        # Ensure the value fits in the specified byte size
        if not (0 <= value < 2 ** (size * 8)):
            raise ValueError(f"{name} must fit in {size} bytes!")

        # Pack the integer into bytes using struct
        file.write(value.to_bytes(size, byteorder='big'))

    ## 
    #  @brief Writes the current food list to a binary file.
    #  @param file The file object to write to.
    def _write_food(self, file):
        for food in Food.list:
            self._write_int(file, Food.NBYTES_PTS, food.pts, 'food.pts')
            self._write_int(file, Save.NBYTES_COORD, food.x, 'food.x')
            self._write_int(file, Save.NBYTES_COORD, food.y, 'food.y')
        self._write_int(file, Food.NBYTES_PTS, 0x00, 'food.end')

    ## 
    #  @brief Writes the current entity list to a binary file.
    #  @param file The file object to write to.
    def _write_entity(self, file):
        for entity in Entity.list:
            self._write_int(file, Entity.NBYTES_ID, entity.id, 'entity.id')
            self._write_int(file, Save.NBYTES_COORD, entity.x, 'entity.x')
            self._write_int(file, Save.NBYTES_COORD, entity.y, 'entity.y')
            self._write_int(file, Entity.NBYTES_ENERGY, entity.energy, 'entity.energy')
            self._write_int(file, Entity.NBYTES_TIME, entity.time, 'entity.time')
        self._write_int(file, Entity.NBYTES_ID, 0x00, 'entity.end')

    ## 
    #  @brief Loads the simulation state from a binary file.
    #  @throws IOError if file operations fail.
    #  @throws ValueError if the data in the file is invalid.
    def load(self):
        try:
            # Open the file for reading in binary mode
            with open(self.path, 'rb') as file:
                self.last = self._read_int(file, Save.NBYTES_TIME, 'file.last_loading')
                self.time = self._read_int(file, Save.NBYTES_TIME, 'file.sim_time')
                Map.size = (self._read_int(file, Save.NBYTES_COORD, 'map.size_x'),
                            self._read_int(file, Save.NBYTES_COORD, 'map.size_y'))

                self._read_food(file)
                self._read_entity(file)
                
        except IOError as e:
            raise IOError(f"File error: {e}")
        except ValueError as e:
            raise ValueError(f"Value error: {e}")
        except Exception as e:
            raise Exception(f"Failed to load: {e}")

    ## 
    #  @brief Reads an integer value from a binary file.
    #  @param file The file object to read from.
    #  @param size Number of bytes for the integer.
    #  @param name Optional parameter for the value's name (used for error messages).
    #  @return The integer value read from the file.
    #  @throws ValueError if the value cannot be read correctly.
    def _read_int(self, file, size, name="value"):
        data = file.read(size)
        if len(data) != size:
            raise ValueError(f"Could not read {name} from file.")
        return int.from_bytes(data, byteorder='big')

    ## 
    #  @brief Reads food data from a binary file and populates the Food list.
    #  @param file The file object to read from.
    def _read_food(self, file):
        Food.list.clear()  # Clear existing food list
        while True:
            pts = self._read_int(file, Food.NBYTES_PTS, 'food.pts')
            if pts == 0:  # End of food data
                break
            x = self._read_int(file, Save.NBYTES_COORD, 'food.x')
            y = self._read_int(file, Save.NBYTES_COORD, 'food.y')
            Food.new((x, y), pts)  # Create new food item
            


    ## 
    #  @brief Reads entity data from a binary file and populates the Entity list.
    #  @param file The file object to read from.
    def _read_entity(self, file):
        Entity.list.clear()  # Clear existing entity list
        while True:
            entity_id = self._read_int(file, Entity.NBYTES_ID, 'entity.id')
            if entity_id == 0:  # End of entity data
                break
            x = self._read_int(file, Save.NBYTES_COORD, 'entity.x')
            y = self._read_int(file, Save.NBYTES_COORD, 'entity.y')
            energy = self._read_int(file, Entity.NBYTES_ENERGY, 'entity.energy')
            time = self._read_int(file, Entity.NBYTES_TIME, 'entity.time')
            Entity.new((x, y), energy, time)  # Create new entity

if __name__ == "__main__":  
    Map.size = Map.DEFAULT_SIZE
    save = Save(numSave=1)
    save.load()
    print(save)
    sleep(4)
    save.save()
    
