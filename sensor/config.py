class Config():

    interface=''
    database_name=''
    database_host=''
    database_user=''
    databass_pass=''

    def loadConfig(self):
        # read config file
        try:
            with open('config', 'r') as config_file:
                self.interface=config_file.readline()
                # remove new line
                self.interface=remove_new_line(self.interface)
                self.database_name=remove_new_line(config_file.readline())
                self.database_host=remove_new_line(config_file.readline())
                self.database_user=remove_new_line(config_file.readline())
                self.databass_pass=remove_new_line(config_file.readline())
        except FileNotFoundError as error:
            print("Please create '" + error.filename + "' file")
            quit()

def remove_new_line(string):
    return string[0:len(string)-1]
