# Hackathon-commit
### Prototype of Lepsy
Lepsy's prototype represents a Raspberry PI equipped camera. 

For now, the Raspberry PI connects to a PC via ssh and sends signal in case it registers seizure causing video input.
After that, the PC forwards the information to a mobile phone via push notifications.

### Implementation
Most important libraries are **opencv** for analyzing the video input, and **asyncssh** for the communication. 

The server listens on the port 8022 for any incoming connection. Security is to be added via certificates verification. 
### What's next?
The project should implement a real mobile application. The mobile application should connect to Lepsy via Bluetooth connection. Smart watches are the next, as they should measure the heart rate right after a seizure causing video input has been captured. In case user does not respond to the notification within 2 minutes, it should call an ambulance to the user's location.
