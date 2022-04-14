import numpy as np
import os, sys
import gmsh

# ========================================================= #
# ===  make__magnet                                     === #
# ========================================================= #

def make__magnet( dimtags={} ):

    inpFile = "dat/magnet.conf"
    
    import nkGmshRoutines.geometrize__fromTable as gft
    parts   = {}
    parts   = gft.geometrize__fromTable( dimtags=parts, inpFile=inpFile )
    dimtags = { **dimtags, **parts }

    return( dimtags )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    # ------------------------------------------------- #
    # --- [1] initialization of the gmsh            --- #
    # ------------------------------------------------- #
    gmsh.initialize()
    gmsh.option.setNumber( "General.Terminal", 1 )
    gmsh.option.setNumber( "Mesh.Algorithm"  , 5 )
    gmsh.option.setNumber( "Mesh.Algorithm3D", 4 )
    gmsh.option.setNumber( "Mesh.SubdivisionAlgorithm", 0 )
    gmsh.model.add( "model" )
    
    # ------------------------------------------------- #
    # --- [2] Modeling                              --- #
    # ------------------------------------------------- #

    dimtags = make__magnet()
    print( dimtags )
    
    gmsh.model.occ.synchronize()
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()


    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #

    uniform_mesh = False
    
    if ( uniform_mesh ):
        gmsh.option.setNumber( "Mesh.CharacteristicLengthMin", 0.050 )
        gmsh.option.setNumber( "Mesh.CharacteristicLengthMax", 0.050 )
    else:
        meshFile = "dat/mesh.conf"
        physFile = "dat/phys.conf"
        import nkGmshRoutines.assign__meshsize as ams
        meshes   = ams.assign__meshsize( dimtags=dimtags, meshFile=meshFile, physFile=physFile )
    
    # ------------------------------------------------- #
    # --- [4] post process                          --- #
    # ------------------------------------------------- #
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.write( "msh/model.msh" )
    gmsh.finalize()
    

