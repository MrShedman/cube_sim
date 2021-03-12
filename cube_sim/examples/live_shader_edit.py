#!/usr/bin/env python

from cube_sim.application import Application
from cube_sim.led_cube import LEDCube, Face
from cube_sim.resource import getResource
from cube_sim.shader import Shader
from cube_sim.mesh_view import MeshView
from cube_sim.camera import Camera
from cube_sim.vbo import VBO

import OpenGL.GL as GL
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LiveShaderEdit(Application, FileSystemEventHandler):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)

        self.vpos = np.repeat(self.led_cube.sphere_positions[::6], 6, axis=0)
        GL.glBindVertexArray(self.led_cube.mesh.vao)
        self.vbo = VBO(GL.GL_ARRAY_BUFFER, GL.GL_DYNAMIC_DRAW)
        self.vbo.data(self.vpos.nbytes, self.vpos)
        self.vbo.set_slot(3, 3)

        self.noise_scale = 1.0
        self.noise_speed = 1.0
        self.life = 0.0
        self.notify = False

        self.filenames = ['noise.vert', 'perlin_noise.frag']
        self.noise_shader = Shader(self.filenames[0], self.filenames[1])
        self.callbacks = [self.notifyChange, self.notifyChange]
        self.startObserver()

    def update(self, dt):
        self.life += dt * self.noise_speed
        self.reloadShader()

    def render(self):
        self.noise_shader.bind()
        self.noise_shader.setUniform1f("time", self.life)
        self.noise_shader.setUniform1f("scale", self.noise_scale)
        MeshView(self.led_cube, self.noise_shader, self.camera).render(True, False)
        MeshView(self.led_cube, self.shader, self.camera).render(False, self.wireframe)

    def notifyChange(self, filename):
        self.notify = True

    def reloadShader(self):
        if self.notify:
            self.notify = False
            new_shader = Shader(self.filenames[0], self.filenames[1])
            if new_shader.isLinked():
                self.noise_shader = new_shader

    def on_modified(self, event):
        super().on_modified(event)
        if not event.is_directory:
            for i, file in enumerate(self.filenames):
                if event.src_path.endswith(file):
                    if self.callbacks[i] is not None:
                        self.callbacks[i](event.src_path)

    def startObserver(self):
        self.observer = Observer()
        self.observer.schedule(self, getResource(""), recursive=False)
        self.observer.start()

    def stopObserver(self):
        self.observer.stop()
        self.observer.join()

if __name__ == "__main__":
    app = LiveShaderEdit()
    app.run()
    app.stopObserver()
    del app