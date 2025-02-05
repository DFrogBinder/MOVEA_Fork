from simnibs import sim_struct, run_simnibs

tdcs_lead_field = sim_struct.TDCSLEADFIELD()

# subject folder [m2m_earnie]
tdcs_lead_field.subpath = '/home/boyan/sandbox/simnibs4_exmaples/m2m_MNI152'

# output directory
tdcs_lead_field.pathfem = '/home/boyan/sandbox/MOVEA_Fork/Output/leadfield_generatione'

# faster solver, but uses ~12GB RAM
tdcs_lead_field.solver_options = 'pardiso'

run_simnibs(tdcs_lead_field)
