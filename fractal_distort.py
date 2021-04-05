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


def fractal_waves(verts, octaves, amplitude, sel_scale, soft_scale, sel_pers=3, soft_pers=0.7, amp_pers=0.7):
    for i in range(octaves):
        wave_noise(verts, amplitude, sel_scale, soft_scale)
        sel_scale *= sel_pers
        soft_scale *= soft_pers
        amplitude *= amp_pers



if __name__ == '__main__':
    for _obj in sel:
        do_noise(_obj)
