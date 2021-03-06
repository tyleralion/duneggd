#!/usr/bin/env python
'''
Top level builder of the Fine-Grained Tracker (FGT)
'''

import gegede.builder

class WorldBuilder(gegede.builder.Builder):
    '''
    Build a big box world volume.
    N.B. -- Global convention: index 0,1,2 = x,y,z
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, worldDim=['100m','100m','100m'], worldMat='Rock', **kwds):
        self.dimensions = worldDim
        self.material   = worldMat
        self.detEncBldr = self.get_builder("DetEnclosure")


    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        self.define_materials(geom)

        worldBox = geom.shapes.Box( self.name,                 dx=0.5*self.dimensions[0], 
                                    dy=0.5*self.dimensions[1], dz=0.5*self.dimensions[2])
        world_lv = geom.structure.Volume('vol'+self.name, material=self.material, shape=worldBox)
        self.add_volume(world_lv)

        # Position volDetEnclosure in the World Volume.
        # THIS SETS THE ORIGIN wherever we need it in the detector
        detEncDim = self.detEncBldr.dimensions
        detEncPos = ['0cm', '0cm', 0.5*detEncDim[2] ]
        detEnc_lv = self.detEncBldr.get_volume("volDetEnclosure")
        detEnc_in_world = geom.structure.Position('DetEnc_in_World', detEncPos[0], detEncPos[1], detEncPos[2])
        pD_in_W = geom.structure.Placement('placeDetEnc_in_World',
                                           volume = detEnc_lv,
                                           pos = detEnc_in_world)
        world_lv.placements.append(pD_in_W.name)


        return


    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def define_materials(self, g):
        h  = g.matter.Element("hydrogen",   "H",  1,  "1.0791*g/mole" )
        c  = g.matter.Element("carbon",     "C",  6,  "12.0107*g/mole")
        n  = g.matter.Element("nitrogen",   "N",  7,  "14.0671*g/mole")
        o  = g.matter.Element("oxygen",     "O",  8,  "15.999*g/mole" )
        na = g.matter.Element("sodium",     "Na", 11, "22.99*g/mole"  )
        mg = g.matter.Element("magnesium",  "Mg", 12, "24.305*g/mole" )
        al = g.matter.Element("aluminum",   "Al", 13, "26.9815*g/mole")
        si = g.matter.Element("silicon",    "Si", 14, "28.0855*g/mole")
        p  = g.matter.Element("phosphorus", "P",  15, "30.973*g/mole" )
        s  = g.matter.Element("sulfur",     "S",  16, "32.065*g/mole" )
        ar = g.matter.Element("argon",      "Ar", 18, "39.948*g/mole" )
        ca = g.matter.Element("calcium",    "Ca", 20, "40.078*g/mole" )
        ti = g.matter.Element("titanium",   "Ti", 22, "47.867*g/mole" )
        fe = g.matter.Element("iron",       "Fe", 26, "55.8450*g/mole")

        # Molecules for Rock and fibrous_glass Mixtures 
        SiO2  = g.matter.Molecule("SiO2",  density="2.2*g/cc",   elements=(("silicon",1),("oxygen",2)))
        FeO   = g.matter.Molecule("FeO",   density="5.745*g/cc", elements=(("iron",1),("oxygen",1)))
        Al2O3 = g.matter.Molecule("Al2O3", density="3.97*g/cc",  elements=(("aluminum",2),("oxygen",3)))
        MgO   = g.matter.Molecule("MgO",   density="3.58*g/cc",  elements=(("magnesium",1),("oxygen",1)))
        CO2   = g.matter.Molecule("CO2",   density="1.562*g/cc", elements=(("carbon",1),("oxygen",2)))
        CaO   = g.matter.Molecule("CaO",   density="3.35*g/cc",  elements=(("calcium",1),("oxygen",1)))
        Na2O  = g.matter.Molecule("Na2O",  density="2.27*g/cc",  elements=(("sodium",2),("oxygen",1)))
        P2O5  = g.matter.Molecule("P2O5",  density="1.562*g/cc", elements=(("phosphorus",2),("oxygen",5)))        
        TiO2  = g.matter.Molecule("TiO2",  density="4.23*g/cc",  elements=(("titanium",1),("oxygen",2)))
        Fe2O3 = g.matter.Molecule("Fe2O3", density="5.24*g/cc",  elements=(("iron",2),("oxygen",3)))

        rock  = g.matter.Mixture( "Rock", density = "2.82*g/cc", 
                                 components = (
                                     ("SiO2",   0.5267),
                                     ("FeO",    0.1174),
                                     ("Al2O3",  0.1025),
                                     ("oxygen", 0.0771),
                                     ("MgO",    0.0473),
                                     ("CO2",    0.0422),
                                     ("CaO",    0.0382),
                                     ("carbon", 0.0240),
                                     ("sulfur", 0.0186),
                                     ("Na2O",   0.0053),
                                     ("P2O5",   0.0007),
                                 ))


        air   = g.matter.Mixture( "Air", density = "1.290*mg/cc", 
                                 components = (
                                     ("nitrogen", 0.781154), 
                                     ("oxygen",   0.209476),
                                     ("argon",    0.00934)
                                 ))


        fib_glass = g.matter.Mixture( "fibrous_glass", density = "0.1*g/cc", 
                                      components = (
                                          ("SiO2",   0.600),
                                          ("CaO",    0.224),
                                          ("Al2O3",  0.118),
                                          ("MgO",    0.034),
                                          ("TiO2",   0.013),
                                          ("Na2O",   0.010),
                                          ("Fe2O3",  0.001)
                                      ))

        # Materials for the radiators 
        # WARNING! densities not right!
        Fabric = g.matter.Molecule("Fabric", density="0.1*g/cc",   elements=(("carbon",3), ("hydrogen",6)))
        C3H6   = g.matter.Molecule("C3H6",   density="0.1*g/cc",   elements=(("carbon",16),("hydrogen",18),("oxygen",1)))

        # Materials for the targets
        H2O      = g.matter.Molecule("Water",       density="1.0*kg/l",   elements=(("oxygen",1),("hydrogen",2)))
        ArTarget = g.matter.Molecule("ArgonTarget", density="0.233*g/cc", elements=(("argon",1),))
        Aluminum = g.matter.Molecule("Aluminum",    density="2.70*g/cc",  elements=(("aluminum",1),))

    

