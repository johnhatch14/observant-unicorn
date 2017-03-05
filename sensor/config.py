class Config():

    interface=''

    def loadConfig(self):
        # read config file
        config_file = open('config', 'r')
        self.interface=config_file.readline()
        # remove new line
        self.interface=self.interface[:len(self.interface)-1]

