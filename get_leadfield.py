import simnibs
from simnibs import sim_struct

tdcs_lf = sim_struct.TDCSLEADFIELD()
tdcs_lf.fnamehead = '/home/boyan/sandbox/simnibs4_exmaples/m2m_MNI152/MNI152.msh' #[your path to msh]
tdcs_lf.subpath = '/home/boyan/sandbox/simnibs4_exmaples/m2m_MNI152' #[your path to m2m folder]
tdcs_lf.pathfem = '/home/boyan/sandbox/MOVEA_Fork/Output' #[output path]
tdcs_lf.interpolation = None
tdcs_lf.map_to_surf = False
tdcs_lf.tissues = [1,2]
simnibs.run_simnibs(tdcs_lf)
