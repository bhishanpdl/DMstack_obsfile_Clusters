#!python
# -*- coding: utf-8 -*-#
"""
Reading fitsfile table

@author: Bhishan Poudel

@date: Mar 24, 2018


"""
# Imports
import os

def yaml_create():
    output = os.getcwd() + '/output'
    sim_yaml = """
{
"cluster": "SIM_cluster",
"ra": 0.1,
"dec": 0.1,
"redshift": 0.3,
"filter": ["u", "g", "r", "i", "i2", "z"],
"butler": "%s",
"keys": {'src':["id", "coord*", "ext_shapeHSM_HsmSourceMoments_x", "ext_shapeHSM_HsmSourceMoments_y", "ext_shapeHSM_HsmShapeRegauss_e1", "ext_shapeHSM_HsmShapeRegauss_e2"]},
"sim": {"flag" : True, "zfile":"sim.txt"},
"mass":{ "zconfig" : "zphot_ref",
         "mprior":'lin'}
}"""% output

    with open('sim.yaml','w') as fo:
        fo.write(sim_yaml.lstrip())

def main():
    """Run main function."""
    yaml_create()



if __name__ == "__main__":
    main()
