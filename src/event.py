import pygame as pg

class Event:
    def __init__(self,game):
        self.reset_event()
        self.game = game
        self.Count = 4
        
    def reset_event(self):
        self.description = ""
        self.number = 0
        self.reference = ""
        self.choice = {}
        self.LastEvent = pg.time.get_ticks()
        
    def event_exit(self):
        self.reset_event()
        
    def consequence(self,amount,stuff):
        if stuff == "Fame":
            pass
        else:
            pass
        
    def load_event(self):
        if self.reference == "":
            self.reference = str(self.number)
        match self.reference: 
            case 'event_exit':
                self.event_exit()
                
            case '1':
                self.description = "Attention, Pilot. Sensor array indicates the detection of a faint signal amidst our trajectory through space. Initiating scan protocol to determine the nature and origin of the signal. Stand by for further analysis."
                self.choice = {"Continue":'1_1'}
            
            case '1_1':
                self.description = "Pilot, analysis of the signal source reveals an unexpected discovery. The probe has been identified as Voyager 2, a relic from the Solar System. Its presence in this remote sector of space is perplexing, as it exceeds known parameters of its intended trajectory. Recommend proceeding with caution and preparing for further investigation. \n \n Scrap it for parts.\n \n Contact nearest science base."
                self.choice = {"Scrap it":'1_1_1',"Share coordinates":'1_1_2'}
            
            case '1_1_1':
                self.description = "Acknowledged, Pilot. Initiating salvage procedure for Voyager 2 probe. Preparing to deploy retrieval drones to safely gather electronic components for analysis and potential utilization. Salvage operation commencing.\n \n[Gained 1 electronic part.]"
                self.consequence(1,"Electronic parts")
                self.choice = {"Leave":'event_exit'}
        
            case '1_1_2':
                self.description = "Understood, Pilot. Transmitting coordinates of Voyager 2's location to the nearest science base for further study. Data transfer initiated. This significant discovery has the potential to garner widespread attention and acclaim for your contribution to scientific knowledge. Transmission complete. \n \n[Gained 10 fames.]"
                self.consequence(10, "Fame")
                self.choice = {"Leave":'event_exit'}
            
            case '2':
                self.description = "Attention, Pilot. Sensors have detected the presence of an undetected black hole in close proximity to our trajectory. Initiating emergency protocol for black hole encounter. Scans underway to assess potential damage to the ship's systems. Please standby for further analysis."
                self.choice = {"Proceed" : '2_1'}
                
            case '2_1':
                self.description = "Pilot, preliminary scans indicate no immediate damage to the ship's hull or systems as a result of the black hole encounter. However, gravitational fluctuations may have caused minor deviations in our course. Recommend recalibrating navigation systems to compensate for gravitational distortions."
                self.choice = {"Proceed ?" :'2_1_1'}
                
            case '2_1_1':
                self.description = "Further analysis reveals that the ship's proximity to the black hole has resulted in time dilation effects. Time may have passed differently for observers outside the gravitational influence of the black hole. Adjusting ship's clocks to account for temporal discrepancies."
                self.choice = {"Wait what ?":'2_1_1_1'}
                
            case '2_1_1_1':
                self.description = "Pilot, all systems have been stabilized following the black hole encounter. However, it's worth noting that due to time dilation effects, approximately one year has passed relative to observers outside the gravitational influence of the black hole. Continuing on our journey with heightened vigilance for potential gravitational anomalies."
                self.consequence(1,"Time")
                self.choice = {"Leave":"event_exit"}
                
            case '3':
                self.description = "Pilot, sensors have detected an unidentified object directly in our path. Attempting to maneuver to avoid collision... Collision imminent! Impact confirmed. Damage to the hull has occurred. Initiating emergency repairs."
                self.consequence(-1,"Hull")
                self.choice = {"Activate sensors":"3_1"}
            
            case '3_1':
                self.description = "Analysis of the object reveals it to be an asteroid composed of valuable minerals. Despite the damage sustained, the asteroid presents an opportunity for resource extraction. Recommend dispatching mining drones to collect the valuable minerals while repairs to the hull are underway."
                self.choice = {"Send drones":'3_1_1',"Ignore the asteroid":"3_1_2"}
                
            case '3_1_1':
                self.description = "Pilot, good news. The breach in the hull has been successfully sealed, and repairs have been completed to a sufficient level to ensure safe navigation to the next station. Additionally, the mining drones have efficiently collected the valuable minerals from the asteroid. All systems are now operational, and we are ready to resume our journey. \n \n[Gained 3 iron ore. Gained 1 uranium ore.]"
                self.consequence(3,"Iron")
                self.consequence(1,"Uranium")
                self.choice = {"Leave":"event_exit"}
                
            case '3_1_2':
                self.description = "Understood.The breach in the hull has been successfully sealed, and repairs have been completed to a sufficient level to ensure safe navigation to the next station. All systems are now operational, and we are ready to resume our journey."
                self.choice = {"Leave":"event_exit"}
              
            case '4':
                self.description = "Attention, Pilot. An automated distress signal has been intercepted from a nearby derelict spacecraft. Analysis indicates that it has been drifting in space for an extended period. Shall we investigate the source of the distress signal?"
                self.choice = {"Proceed":"4_1","Ignore it":"4_exit"}
                
            case '4_1':
                self.description = "Understood, Pilot. Initiating approach to the derelict spacecraft to investigate the source of the distress signal. Preparing to establish communication and assess the situation. Stand by for further updates."
                self.choice = {"Continue":"4_2"}
            
            case '4_2':
                self.description = "Pilot, as we draw nearer to the derelict spacecraft, visual scans unveil substantial hull damage and indications of internal depressurization. External communication efforts continue to yield no response. Caution is advised as we proceed with docking maneuvers for a closer inspection."
                self.choice = {"Dock to ship":"4_3","Leave":'4_exit'}
                
            case '4_3':
                self.description = "Acknowledged, Pilot. Initiating docking sequence with the derelict spacecraft. Approaching designated docking port. Docking clamps engaged... Docking complete. Atmospheric seals activated. Ready to proceed with boarding procedures. Shall I open the airlock hatch for entry?"
                self.choice = {"Explore the ship":"4_3_1","Salvage the ship":"4_3_2","Leave":'4_exit'}
            
            case '4_3_1':
                self.description = "Acknowledged, Pilot. Initiating exploration protocol of the derelict spacecraft. Opening the airlock hatch for entry. Proceeding cautiously into the interior of the vessel. Monitoring environmental conditions and scanning for any signs of life or potential hazards. Ready to provide updates as exploration progresses."
                self.choice = {"Suit up":"4_3_1_1"}
                
            case '4_3_1_1':
                self.description = "Pilot, further investigation reveals that the derelict spacecraft is a colony ship housing cryopods. Remarkably, one of the cryopods remains operational, containing a young woman in stasis. Her pod appears to be functioning properly, preserving her in suspended animation. Shall we prioritize efforts to revive her ?"
                self.choice = {"Revive her":"4_3_1_1_1","Leave her":"4_3_1_1_2"}
                
            case '4_3_1_1_1':
                self.description = "Acknowledged, Pilot. Initiating the process to bring the young woman out of stasis. Engaging the cryopod's revival sequence... Revival process complete. The young woman has been successfully awakened from stasis. Monitoring her vital signs and cognitive functions as she adjusts to consciousness."
                self.choice = {"Bring her back":"4_3_1_1_1_1"}
                
            case '4_3_1_1_1_1':
                self.description = "Acknowledged, Pilot. Initiating retrieval of the young woman from the cryopod. Extending the retrieval platform to safely transfer her to the ship's interior. Retrieval in progress... Transfer complete. The young woman has been successfully brought aboard the ship. Monitoring her condition and providing necessary medical attention as she acclimates to her surroundings."
                self.choice = {"Talk to her":"4_3_1_1_1_2"}
                
            case '4_3_1_1_1_2':
                self.description = "The young woman expresses profound gratitude for her rescue, conveying her disbelief at being saved after the harrowing experience aboard the lost colony ship. She recounts the ordeal caused by a navigation system malfunction leading to the ship drifting off. As a last hope, the crew locked themselves in cryostasis to survive. Eager to repay the kindness shown to her, she expresses a willingness to assist in any way possible."
                self.choice = {"Accept help":"4_3_1_1_1_2_1", "Refuse politely":"4_3_1_1_2_2"}
                
            case '4_3_1_1_1_2_1':
                self.description = "You warmly welcome the young woman to join the crew, recognizing her resilience and potential contributions to the ship's endeavors. With her acceptance, she becomes a valued member of the crew, ready to embark on new adventures and forge bonds with her newfound companions. \n\n[Gained 1 crewmate.]"
                self.consequence(1,"Crewmate_f")
                self.choice = {"Leave":"event_exit"}
                
            case '4_3_1_1_1_2_2':
                self.description = "You expresse gratitude for her offer but explain that the ship's crew can manage without additional assistance. However, you assure her that you will ensure her safety and well-being by dropping her off at the next star station, where she can receive proper care and support."
                self.choice = {"Leave":"event_exit"}
            
            case '4_3_1_1_2':
                self.description = "Acknowledged, Pilot. Acknowledging the inherent danger of awakening the young woman from cryosleep without proper medical supervision. It poses potential risks to her well-being. Proposing the prioritization of gathering valuable medical supplies from the colony ship instead. \n\n [Gained 3 medical supplies.]"
                self.consequence(3,"Medical supplies")
                self.choice = {"Leave":"event_exit"}
                
            case '4_3_2':
                self.description = "Understood, Pilot. Initiating deployment of mining drones for salvage operation on the derelict spacecraft. Drones dispatched to gather any salvageable materials and resources from the vessel's wreckage. Monitoring drone activity and resource collection progress."
                self.choice = {"Report results":"4_3_2_1"}
           
            case '4_3_2_1':
                self.description = "Salvage operation complete. Analysis indicates that the mining drones have successfully retrieved valuable materials and resources from the derelict spacecraft. \n \n [Gained 10 steels. Gained 1 electronic part.]"
                self.consequence(10,"Steel")
                self.consequence(1,"Electronic parts")
                self.choice = {"Leave":"event_exit"}