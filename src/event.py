class Event:
    def __init__(self,game):
        self.reset_event()
        self.game = game
        
    def reset_event(self):
        self.description = ""
        self.number = 0
        self.choice = {}
        
    def event_exit(self):
        self.reset_event()
        self.number = 0
        
    def consequence(self,amount,stuff):
        if stuff == "Fame":
            pass
        else:
            pass
        
    def load_event(self):
        self.reference = str(self.number)
        match self.reference:
            case 'event_exit':
                self.event_exit()
                
            case '1':
                self.description = "Attention, Pilot. Sensor array indicates the detection of a faint signal amidst our trajectory through space. Initiating scan protocol to determine the nature and origin of the signal. Stand by for further analysis."
                self.choice = {"continue":'1_1'}
            
            case '1_1':
                self.description = "Pilot, analysis of the signal source reveals an unexpected discovery. The probe has been identified as Voyager 2, a relic from the Solar System. Its presence in this remote sector of space is perplexing, as it exceeds known parameters of its intended trajectory. Recommend proceeding with caution and preparing for further investigation."
                self.choice = {"Scrap it":'1_1_1',"Share coordinates":'1_1_2'}
            
            case '1_1_1':
                self.description = "Acknowledged, Pilot. Initiating salvage procedure for Voyager 2 probe. Preparing to deploy retrieval drones to safely gather electronic components for analysis and potential utilization. Salvage operation commencing."
                self.consequence(1,"Electronic parts")
                self.choice = {"Leave":'event_exit'}
        
            case '1_1_2':
                self.description = "Understood, Pilot. Transmitting coordinates of Voyager 2's location to the nearest science base for further study. Data transfer initiated. This significant discovery has the potential to garner widespread attention and acclaim for your contribution to scientific knowledge. Transmission complete."
                self.consequence(10, "Fame")
                self.choice = {"Leave":'event_exit'}
        
EventCount = 1  
