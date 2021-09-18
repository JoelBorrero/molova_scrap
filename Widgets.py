import time


class LoadingBar:
    def __init__(self, total, scale=.5, sleep=False):
        '''Take care of the console width'''
        self.value = 0
        self.total = total
        self.scale = scale
        self.sleep = sleep
    
    def update(self):
        self.value += 1
        percentage = int(self.value / self.total * 100)
        print(f'\r|{"▓"*int(percentage*self.scale)}{"·"*int((100-percentage)*self.scale)}|{percentage}% {self.value}/{self.total}', end='\n' if percentage == 100 else '\r')
        if self.sleep:
            time.sleep(.00001)
