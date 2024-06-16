#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created with ChatGPT-4o
# Date =<today>

import math
import OCC.Core.BRepPrimAPI as BRepPrimAPI
import OCC.Core.gp as gp
import OCC.Core.BRepAlgoAPI as BRepAlgoAPI
import OCC.Display.SimpleGui as SimpleGui
import OCC.Core.BRepBuilderAPI as BRepBuilderAPI
import OCC.Core.BRepOffsetAPI as BRepOffsetAPI
import OCC.Core.STEPControl as STEPControl

class HijabStand:
    def __init__(self, base_radius, base_height, stem_radius, stem_height, sphere_radius):
        self.base_radius = base_radius
        self.base_height = base_height
        self.stem_radius = stem_radius
        self.stem_height = stem_height
        self.sphere_radius = sphere_radius
        self.shapes = []
        self.create_stand()

    def create_base(self):
        """Create the base of the stand."""
        base = BRepPrimAPI.BRepPrimAPI_MakeCylinder(self.base_radius, self.base_height).Shape()
        self.shapes.append(base)

    def create_stem(self):
        """Create the stem of the stand."""
        stem = BRepPrimAPI.BRepPrimAPI_MakeCylinder(self.stem_radius, self.stem_height).Shape()
        # Translate the stem to be on top of the base
        transform = gp.gp_Trsf()
        transform.SetTranslation(gp.gp_Vec(0, 0, self.base_height))
        stem = BRepBuilderAPI.BRepBuilderAPI_Transform(stem, transform).Shape()
        self.shapes.append(stem)

    def create_sphere(self):
        """Create the spherical top of the stand."""
        sphere = BRepPrimAPI.BRepPrimAPI_MakeSphere(self.sphere_radius).Shape()
        # Translate the sphere to be on top of the stem
        transform = gp.gp_Trsf()
        transform.SetTranslation(gp.gp_Vec(0, 0, self.base_height + self.stem_height))
        sphere = BRepBuilderAPI.BRepBuilderAPI_Transform(sphere, transform).Shape()
        self.shapes.append(sphere)

    def create_stand(self):
        """Create the entire stand."""
        self.create_base()
        self.create_stem()
        self.create_sphere()

    def display(self):
        """Display the hijab stand."""
        display, start_display, add_menu, add_function_to_menu = SimpleGui.init_display()
        for shape in self.shapes:
            display.DisplayShape(shape, update=True)
        start_display()

    def export_step(self, filename):
        """Export the stand to a STEP file."""
        step_writer = STEPControl.STEPControl_Writer()
        for shape in self.shapes:
            step_writer.Transfer(shape, STEPControl.STEPControl_AsIs)
        step_writer.Write(filename)

# Parameters for the hijab stand
base_radius = 50  # mm
base_height = 10  # mm
stem_radius = 10  # mm
stem_height = 200  # mm
sphere_radius = 100  # mm

# Create the hijab stand
stand = HijabStand(base_radius, base_height, stem_radius, stem_height, sphere_radius)
stand.display()
stand.export_step("hijab_stand.step")
