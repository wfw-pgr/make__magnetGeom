import numpy as np
import os, sys
import gmsh

# ========================================================= #
# ===  make__magnet                                     === #
# ========================================================= #

def make__magnet( dimtags={} ):

    # ------------------------------------------------- #
    # --- [1] load constants                        --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnsFile = "dat/unified_parts.conf"
    const   = lcn.load__constants( inpFile=cnsFile )

    # ------------------------------------------------- #
    # --- [2] make variables list                   --- #
    # ------------------------------------------------- #
    keys    = [ "geometry.r_pole", \
                "geometry.z_gap" , \
                "geometry.z_pole", \
                "geometry.w_coil", \
                "geometry.w_iair1", \
                "geometry.w_iair2", \
                "geometry.h_coil", \
                "geometry.h_iair1", \
                "geometry.h_iair2", \
                "geometry.w_yoke", \
                "geometry.h_yoke", \
                "geometry.w_cut", \
                "geometry.h_cut", \
                "geometry.w_oair", \
                "geometry.h_oair", \
    ]
    outFile = "dat/variables.conf"
    import nkUtilities.write__variableDefinition as wvd
    ret     = wvd.write__variableDefinition( table=const, keys=keys, outFile=outFile )
    
    # ------------------------------------------------- #
    # --- [3] define geometries                     --- #
    # ------------------------------------------------- #
    inpFile = "dat/magnet_divide.conf"
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
    
    gmsh.model.occ.synchronize()
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()

    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    mesh_from_config = True                #   from nkGMshRoutines/test/mesh.conf, phys.conf
    if ( mesh_from_config ):
        meshFile = "dat/magnet_mesh.conf"
        physFile = "dat/magnet_phys.conf"
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( meshFile=meshFile, physFile=physFile, dimtags=dimtags )
    else:
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( uniform=0.1, dimtags=dimtags )

    # ------------------------------------------------- #
    # --- [4] post process                          --- #
    # ------------------------------------------------- #
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.write( "msh/model.msh" )
    gmsh.finalize()
