## 
#  @file cmd.py
#  @brief File containing the class *Cmd*.
#  @date 2024-10-05
#  @author Rabyte Studio

from entity import Entity
from food import Food
import threading
import os
import platform


## 
#  @class Cmd
#  @brief Class for handling terminal commands and interaction in the simulation.
class Cmd:

    lock = threading.Lock()  ##< Lock for synchronizing access to terminal input

    @classmethod
    def startCmd(cls):
        """Starts the command input thread."""
        cls.input = threading.Thread(target=cls._handle_input)
        cls.input.start()  # Start the input thread

    
    @classmethod
    def stopCmd(cls):
        """Waits for the command input thread to finish."""
        cls.input.join()  # Wait for the input thread to finish

    ## 
    #  @brief Handles terminal input for commands.
    #  @details This method continuously reads input from the terminal in a separate thread.
    #  @note The input thread will stop when _running is set to False.
    @classmethod
    def _handle_input(cls):
        while True:
            with cls.lock:
                if not cls._running:
                    break
            command = input("> ")
            if cls._running:
                try:
                    cls.processCmd(command)
                except Exception as err:
                    print(f"#ERROR: {err}")

    ## 
    #  @brief Processes commands entered in the terminal.
    #  @param command The command string entered by the user.
    #  @details This method interprets the command and executes the corresponding action.
    @classmethod
    def processCmd(cls, command):
        parts = command.split()
        if len(parts) == 0:
            return

        cmd = parts[0]
        if cmd == "save":
            cls._save()
        elif cmd == "exit":
            cls._running = False
        elif cmd == "help":
            cls._help()
        elif cmd == "clear":
            cls._clear()
        elif cmd == "spawn":
            cls._spawn(parts[1:])
        else:
            print("Unknown command. Type 'help' for a list of commands.")

    ## 
    #  @brief Saves the current state of the simulation.
    #  @details This method attempts to save the current simulation state and handles any errors.
    @classmethod
    def _save(cls):
        try:
            cls.save_duration = 60
            cls.save.save()
            print(f"Saving simulation with ID {cls.save.number}...")
        except Exception as e:
            print(f"Error saving simulation: {e}")

    ## 
    #  @brief Clears the terminal screen and resets the input prompt.
    #  @details This method determines the appropriate clear command based on the operating system.
    @classmethod
    def _clear(cls):
        command = "cls" if platform.system() == "Windows" else "clear"
        os.system(command)

    ## 
    #  @brief Spawns entities or food in the simulation.
    #  @param args The arguments for the spawn command.
    #  @details This method interprets the spawn command and creates the specified element type.
    @classmethod
    def _spawn(cls, args):
        if len(args) < 1:
            print("Usage: spawn <elem_type> [x] [y] [...]")
            return

        elem_type = args[0]
        
        # Initialization of coordinates
        x, y = None, None
        try:
            if len(args) > 1:
                x = int(args[1])
            if len(args) > 2:
                y = int(args[2])
        except ValueError:
            print("Coordinates must be integers.")
            return

        # Create entities based on the type
        if elem_type == 'entity':
            if x is not None and y is not None:
                Entity.new((x, y), Entity.ENERGY_DEF)
                print(f"Spawning entity at ({x}, {y})")
            else:
                Entity.generate()
                print("Spawning entity at a random location.")
        elif elem_type == 'food':
            if x is not None and y is not None:
                Food.new((x, y))
                print(f"Spawning food at ({x}, {y})")
            else:
                Food.generate()
                print("Spawning food at a random location.")
        else:
            print("Unknown element type. Use 'entity' or 'food'.")

    ## 
    #  @brief Displays the help message with available commands.
    #  @details This method prints out a list of all commands that the user can enter.
    @classmethod
    def _help(cls):
        print("Available commands:")
        print(" - save: Saves the current state of the simulation.")
        print(" - spawn <elem_type> [x] [y] [...]: Make an element spawn in the simulation.")
        print(" - exit: Exits the simulation.")
        print(" - clear: Clears the terminal screen.")
        print(" - help: Displays this help message.")

