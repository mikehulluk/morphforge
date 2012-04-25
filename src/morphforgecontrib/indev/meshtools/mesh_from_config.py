
xTest = """


COLOR_ALIASES {

    RB: (255,210,50);
    dlc: (255,0,0);
    dla: (255,170,140);
    tIN: (230,50,120);
    cIN: (0,170,220);
    aIN: (70,70,180);
    dIN: (150,80,30) ;
    MN: (0,150,60);

    UnknownRgn: (30,250,250);
}


COLOR_DEFAULTS {
    RegionColor 1 : (128,0,0);
    RegionColor 2,3,4 : (0,128,0);
}

COLOR_DEFAULTS {
    RegionColor 1 : (128,128,0);
    RegionColor 6,7: RB;
}

MAKEPLY "aIN 471.ply" {
    RegionColor 1 : aIN;
    RegionColor 9,10,13,14: IGNORE;
    }


MAKEPLY "aIN 471.ply" {
    RegionColor 5,15,16 : UnknownRgn;
    RegionColor 2 : aIN;
    RegionColor 1 : aIN;
    RegionColor 9,10,13,14: IGNORE;
    Include "aIN 471 nrn + ns 100325.transl.invX.scaled.straightened.swc" {TRIM:100} ;

    }

#MAKEPLY "aIN 471.ply" {
#    RegionColor * : aIN;
#    RegionColor 9,10,13,14: IGNORE;
#    Include "aIN 471 nrn + ns 100325.transl.invX.scaled.straightened.swc" {TRIM:50, OFFSET:(0,0,0) };
#    Include "aIN 471 nrn + ns 100325.transl.invX.scaled.straightened.swc" {TRIM:50, OFFSET:(0,0,20) };
#    Include "aIN 471 nrn + ns 100325.transl.invX.scaled.straightened.swc" {TRIM:50, OFFSET:(0,0,40) };
#
#    }
#



"""

from mesh_config_parser import parse_mesh_config
from mesh_config_parser import parse_zip_file
parse_zip_file( zip_in ="/home/michael/Desktop/ply/src.zip",
                zip_out = "/home/michael/Desktop/ply/fromPly.zip")




