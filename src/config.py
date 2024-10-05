## 
#  @file config.py
#  @brief File containing the class *Config*.
#  @date 2024-10-05
#  @author Rabyte Studio

import configparser
import path
import os

DEFAULT_WINDOW_NAME = 'RSim - Simulation'
DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 600


class _Config_Visual:
    ## 
    #  @brief Initializes the _Config_Visual class from a config parser object.
    #
    #  This constructor retrieves visual configuration parameters such as 
    #  window name, width, and height from the provided config object. 
    #
    #  @param config A configparser.ConfigParser object containing the configuration.
    def __init__(self, config):
        try:
            self.window_name = config.get('VISUAL', 'window_name', fallback=DEFAULT_WINDOW_NAME)
            self.window_width = config.getint('VISUAL', 'window_width', fallback=DEFAULT_WINDOW_WIDTH)
            self.window_height = config.getint('VISUAL', 'window_height', fallback=DEFAULT_WINDOW_HEIGHT)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise f"Error reading config: {e}"
        
    ## 
    #  @brief Returns a string representation of the visual configuration.
    #
    #  @return A formatted string describing the visual configuration settings.
    def __repr__(self) -> str:
        return (
            f"  Visual:\n"
            f"     - window_name: '{self.window_name}'\n"
            f"     - window_width: {self.window_width}pxl\n"
            f"     - window_height: {self.window_height}pxl\n"
            )


## 
#  @class Config
class Config:
    ## 
    #  @brief A class for managing the configuration settings of the application.
    #
    #  This class provides methods to initialize configuration from a file, 
    #  create default configurations, and access visual settings.
    visual = None

    ## 
    #  @brief Initializes the configuration from a specified file.
    #
    #  This class method checks if the specified config file exists. If not, 
    #  it creates a default config file. It then reads the configuration and 
    #  initializes the visual settings.
    #
    #  @param config_file The path to the configuration file (default: path.PATH_CONFIG).
    @classmethod
    def init(self, config_file=path.PATH_CONFIG):
        # Check if the config file exists
        if not os.path.exists(config_file):
            print(f"{config_file} not found. Creating default config.")
            self.default(config_file)

        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Read the configuration file
        config.read(config_file)

        Config.visual = _Config_Visual(config)
        return None

    ## 
    #  @brief Creates and writes a default configuration file.
    #
    #  This method initializes default visual settings and writes them to the 
    #  specified config file.
    #
    #  @param config_file The path to the configuration file (default: path.PATH_CONFIG).
    def default(self, config_file=path.PATH_CONFIG):
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        config['VISUAL'] = {
            'window_name': DEFAULT_WINDOW_NAME,
            'window_width': DEFAULT_WINDOW_WIDTH,
            'window_height': DEFAULT_WINDOW_HEIGHT
        }

        # Write the default configuration to a file
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        print(f"Default config created at {config_file}")

    ## 
    #  @brief Returns a string representation of the Config class.
    #
    #  @return A formatted string describing the current configuration settings.
    def __repr__(self) -> str:
        return (
            f"Config:\n{self.visual}"
        )

# Example usage
if __name__ == "__main__":
    c = Config()
    print(c)
