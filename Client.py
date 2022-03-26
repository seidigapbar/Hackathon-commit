import cv2
from PIL import Image, ImageStat
import timeit
# Read the video from specified path

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

def brightness(frame):
    color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_coverted)
    stat = ImageStat.Stat(pil_image)
    return stat.rms[0]

flickering = False

def framesloop():
     brightnessarr = []
     
     for i in range(0, 15):
        ret, frame = cam.read()
        #frame = cv2.resize(frame,(640,480))
        
        if flickering:
            cv2.putText(frame, "Flickering detected!", (0, 48), cv2.FONT_HERSHEY_DUPLEX, 1, (55, 49, 255), 2)
        else:
            cv2.putText(frame, "Status: normal", (0, 48), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("Video", frame)
        b = brightness(frame)
        brightnessarr.append(b)

     return brightnessarr

import asyncio, asyncssh, sys

async def run_client() -> None:
    async with asyncssh.connect('192.168.0.7', username='guest', port=8022, known_hosts=None) as conn:
        async with conn.create_process('bc') as process:
            while True:
                lowf = 0
                highf = 0

                #start = timeit.default_timer()

                brightnessarr = framesloop()

                #end = timeit.default_timer()

                #print("Time took to get array of frames brightness: ", end-start)

                framebefore = -1
                for frame in brightnessarr:   
                    if frame < 100 and framebefore == 1:
                        lowf += 1
                        framebefore = -1
                    elif frame > 120 and framebefore == -1:
                        highf += 1
                        framebefore = 1

                if lowf > 1 and highf > 1:
                    print("flickering")
                    flickering = True
                    process.stdin.write("FLICKERING!" + '\n')
                    print("Message sent!")

                else:
                    print("no flickering")
                    flickering = False

                #cv2.imshow('video',frame)

                cv2.waitKey(1)

try:
    asyncio.get_event_loop().run_until_complete(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
