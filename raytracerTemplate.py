"""
/*******************************************************************************
 *
 *            #, #,         CCCCCC  VV    VV MM      MM RRRRRRR
 *           %  %(  #%%#   CC    CC VV    VV MMM    MMM RR    RR
 *           %    %## #    CC        V    V  MM M  M MM RR    RR
 *            ,%      %    CC        VV  VV  MM  MM  MM RRRRRR
 *            (%      %,   CC    CC   VVVV   MM      MM RR   RR
 *              #%    %*    CCCCCC     VV    MM      MM RR    RR
 *             .%    %/
 *                (%.      Computer Vision & Mixed Reality Group
 *
 ******************************************************************************/
/**          @copyright:   Hochschule RheinMain,
 *                         University of Applied Sciences
 *              @author:   Prof. Dr. Ulrich Schwanecke, Fabian Stahl
 *             @version:   2.0
 *                @date:   01.04.2023
 ******************************************************************************/
/**         raytracerTemplate.py
 *
 *          Simple Python template to generate ray traced images and display
 *          results in a 2D scene using OpenGL.
 ****
"""
from rendering import Scene, RenderWindow
import numpy as np
import rt3


class RayTracer:

    def __init__(self, width, height):
        self.width  = width
        self.height = height
        # Setup the raytracer accordingly
        self.scene = [
            rt3.Sphere(rt3.vec3(.4, .6, 0.7), 0.3, rt3.vec3(1, 0, 0)),
            rt3.Sphere(rt3.vec3(0, 1.2, 0.7),0.3, rt3.vec3(0, 0, 1)),
            rt3.Sphere(rt3.vec3(-.4, .6, 0.7), 0.3, rt3.vec3(0, 1, 0)),
            rt3.Triangle(rt3.vec3(0.4, 0.6, 0.7), rt3.vec3(0, 1.2, 0.7), rt3.vec3(-0.4, 0.6, 0.7), rt3.vec3(1, 1, 0)),
            rt3.CheckeredSphere(rt3.vec3(0,-99999.5, 0), 99999, rt3.vec3(.9, .9, .9), 0.25)
        ]
        # Calculate scene center
        self.scene_center = rt3.vec3(0, 0, 0)
        i = 0
        for sphere in self.scene:
            self.scene_center += sphere.c
            print(i, ' ', [i for i in sphere.c.components()])
            i+= 1
            if i == 3:
                break
        self.scene_center = rt3.vec3(self.scene_center.components()[0]/3,self.scene_center.components()[1]/3,self.scene_center.components()[2]/3)

        
        # Rotation angle (in radians)
        self.alpha = np.pi / 10
        

    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
        
        # Adjust screen coordinates
        r = float(self.width) / self.height
        self.S = (-1, 1 / r + .5, 1, -1 / r + .5)
        
        # Regenerate points
        x = np.tile(np.linspace(self.S[0], self.S[2], self.width), self.height)
        y = np.repeat(np.linspace(self.S[1], self.S[3], self.height), self.width)
        Q = rt3.vec3(x, y, 0)
        self.color = rt3.raytrace(rt3.E, (Q - rt3.E).norm(), self.scene)
    
    def rotate_pos(self):
        # TODO: Modify scene accordingly
        #fuer Z-AchsenRotation
        #R = np.array([[np.cos(-self.alpha), -np.sin(-self.alpha), 0],
        #              [np.sin(-self.alpha), np.cos(-self.alpha), 0],
        #              [0, 0, 1]])
        R = np.array([[np.cos(self.alpha), 0, np.sin(self.alpha)],
                     [0, 1, 0],
                     [-np.sin(self.alpha), 0, np.cos(self.alpha)]])
        for object in self.scene:
            if isinstance(object, rt3.Triangle):
                v0 = rt3.vec3(*((R.dot((object.v0 - self.scene_center).components())) + self.scene_center.components()))
                v1 = rt3.vec3(*((R.dot((object.v1 - self.scene_center).components())) + self.scene_center.components()))
                v2 = rt3.vec3(*((R.dot((object.v2 - self.scene_center).components())) + self.scene_center.components()))
                object.v0 = v0
                object.v1 = v1
                object.v2 = v2
                
            elif isinstance(object, rt3.Sphere):
                position = object.c
                new_position = rt3.vec3(*((R.dot((position - self.scene_center).components())) + self.scene_center.components()))
                object.c = new_position
    
    def rotate_neg(self):
        # TODO: Modify scene accordingly
        # fuer Z-AchsenRotation
        #R = np.array([[np.cos(self.alpha), -np.sin(self.alpha), 0],
        #          [np.sin(self.alpha), np.cos(self.alpha), 0],
        #          [0, 0, 1]])
        R = np.array([[np.cos(-self.alpha), 0, np.sin(-self.alpha)],
                    [0, 1, 0],
                    [-np.sin(-self.alpha), 0, np.cos(-self.alpha)]])
        
        for object in self.scene:
            if isinstance(object, rt3.Triangle):
                v0 = rt3.vec3(*((R.dot((object.v0 - self.scene_center).components())) + self.scene_center.components()))
                v1 = rt3.vec3(*((R.dot((object.v1 - self.scene_center).components())) + self.scene_center.components()))
                v2 = rt3.vec3(*((R.dot((object.v2 - self.scene_center).components())) + self.scene_center.components()))
                object.v0 = v0
                object.v1 = v1
                object.v2 = v2

            elif isinstance(object, rt3.Sphere):
                position = object.c
                new_position = rt3.vec3(*((R.dot((position - self.scene_center).components())) + self.scene_center.components()))
                object.c = new_position
            
        
        

    def render(self):
        # Ray trace each pixel and generate an image
        r = float(self.width) / self.height
        # Screen coordinates: x0, y0, x1, y1.
        self.S = (-1, 1 / r + .5, 1, -1 / r + .5)
        x = np.tile(np.linspace(self.S[0], self.S[2], self.width), self.height)
        y = np.repeat(np.linspace(self.S[1], self.S[3], self.height), self.width)
        Q = rt3.vec3(x, y, 0)
        self.color = rt3.raytrace(rt3.E, (Q - rt3.E).norm(), self.scene)

        rgb = [rt3.Image.fromarray((255 * np.clip(c, 0, 1).reshape((self.height, self.width))).astype(np.uint8), "L") for c in self.color.components()]
        return rt3.Image.merge("RGB", rgb)


# main function
if __name__ == '__main__':

    # set size of render viewport
    width, height = 640, 480

    # instantiate a ray tracer
    ray_tracer = RayTracer(width, height)

    # instantiate a scene
    scene = Scene(width, height, ray_tracer, "Raytracing Template")

    # pass the scene to a render window
    rw = RenderWindow(scene)

    # ... and start main loop
    rw.run()
