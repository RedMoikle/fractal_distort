"""
Fractal Distort by Michael Stickler

Select an object or group of objects and run this script to create a warpy fractal distortion on the surface.

process:
soft select transforms a random selection of verts along their normals.
Then repeats with smaller radius, but higher selected vert count, and smaller transforms,
creating finer and finer details
TODO: add support for moving along normals
"""

import random

import pymel.core as pm

sel = pm.selected()


def subset(sel, pcnt):
    return random.sample(sel, int(len(sel) * pcnt))


def blob_move(verts, amplitude, sel_scale, soft_scale):
    pm.select(subset(verts, sel_scale))
    pm.softSelect(sse=True, ssd=soft_scale)
    pm.move(amplitude, y=True, os=True, relative=True)


def blob_noise(verts, n, amplitude, sel_scale, soft_scale):
    for i in range(n):
        blob_move(verts, amplitude * random.random(), sel_scale, soft_scale)


def wave_noise(verts, amplitude, sel_scale, soft_scale):
    second_verts = subset(verts, sel_scale)
    before_y = pm.getAttr(pm.polyMoveVertex(second_verts)[0].pivotY)
    blob_move(verts, amplitude, sel_scale, soft_scale)
    after_y = pm.getAttr(pm.polyMoveVertex(second_verts)[0].pivotY)
    offset_y = after_y - before_y
    blob_move(second_verts, -offset_y * random.random() * (0.5 + 0.5), 1, soft_scale)


def fractal_waves(verts, octaves, amplitude, sel_scale, soft_scale):
    for i in range(octaves):
        wave_noise(verts, amplitude, sel_scale, soft_scale)
        sel_scale *= 2
        soft_scale *= 0.8
        amplitude *= 0.5

def do_noise(verts, octaves=4, selections=0.5, amplitude=0.2, frequency=0.5, direction=(0, 1, 0), anchor=0.5,
             amp_pers=0.5, freq_pers=0.5, sel_pers=2):
    normalise = 1 / sum([amp_pers**o for o in range(1, octaves + 1)])
    for i in range(1, octaves + 1):
        o_scale = octaves / i
        selections*=sel_pers
        amplitude*=amp_pers

        blob_noise(verts, selections)


if __name__ == '__main__':
    for _obj in sel:
        do_noise(_obj)
