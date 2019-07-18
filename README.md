# RayCastingEngine
Python-implemented raycasting engine

As an intro to computer graphics, I decided to implement a ray casting engine  
after watching [a video](https://www.youtube.com/watch?v=eOCQfxRQ2pY&t=601s) and finding myself interested. My friend [Nik](https://github.com/NikolasUntoten) helped  
as usual with an ear and fresh perspectives. I chose to use Python for this  
project since the [pygame](https://www.pygame.org/news) library so I didn't have to implement anything  
related to keyboard listeners or graphics panels.  
![alt text](https://github.com/PieterBenjamin/RayCastingEngine/blob/master/imgs/RayCastingSampleTopDown)

Because this was intended as a short project to understand the basics of rendering,  
I did not take great care to avoid all the possible errors. My method of calculating
intersections can be slow and inaccurate, and leads to a fisheye effect. These could  
be avoided, but I decided instead to keep this project short and make approximations.  
You can see the effect of this in the second screenshot (around the edges). However,  
considering the aim of the project, I am quite happy with how it turned out.

![alt text](https://github.com/PieterBenjamin/RayCastingEngine/blob/master/imgs/First%20person%20raycasting%20sample.png)
