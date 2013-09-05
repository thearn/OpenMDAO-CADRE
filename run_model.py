
import numpy as np

from openmdao.lib.drivers.api import CONMINdriver
from openmdao.main.api import Assembly, set_as_top

from CADRE.CADRE_assembly import CADRE

solar_raw1 = np.genfromtxt('CADRE/data/Solar/Area10.txt')
solar_raw2 = np.loadtxt("CADRE/data/Solar/Area_all.txt")
comm_rawGdata = np.genfromtxt('CADRE/data/Comm/Gain.txt')
comm_raw = (10**(comm_rawGdata/10.0)).reshape((361,361), order='F')
power_raw = np.genfromtxt('CADRE/data/Power/curve.dat')


n = 100
m = 20

# Initialize analysis points
LDs = [5233.5, 5294.5, 5356.5, 5417.5, 5478.5, 5537.5]

r_e2b_I0s = [np.array([ 4505.29362, -3402.16069, -3943.74582,
                        4.1923899 , -1.56280012,  6.14347427]),
np.array([-1005.46693 ,  -597.205348, -6772.86532, -0.61047858,
          -7.54623146,  0.75907455 ]),
np.array([ 4401.10539,  2275.95053, -4784.13188, -5.26605537,
           -1.08194926, -5.37013745]),
np.array([-4969.91222,  4624.84149,  1135.9414,  0.1874654 ,
          -1.62801666,  7.4302362 ]),
np.array([ -235.021232,  2195.72976 ,  6499.79919, -2.55956031,
           -6.82743519,  2.21628099 ]),
np.array([ -690.314375, -1081.78239 , -6762.90367,  7.44316722,
           1.19745345, -0.96035904 ])]

model = set_as_top(Assembly())
model.add('cadre', CADRE(n, m, solar_raw1, solar_raw2, comm_raw, power_raw))

model.cadre.set("LD", LDs[0])
model.cadre.set("r_e2b_I0", r_e2b_I0s[0])
model.cadre.set("CP_P_comm", np.random.random((m,))+0.5)

model.add('driver', CONMINdriver())
model.driver.iprint = 2


# add parameters to driver
#for k in xrange(12):
    #for j in xrange(m):
    #    param = ''.join(["cadre.CP_Isetpt[(", str(k), ", ",
    #                     str(j), ")]"])
    #    model.driver.add_parameter(param, low=0, high=0.4)
for k in xrange(m):
    param = ''.join(["cadre.CP_gamma[",str(k),"]"])
    model.driver.add_parameter(param, low=0, high=np.pi/2.)
for k in xrange(m):
    param = ''.join(["cadre.CP_P_comm[",str(k),"]"])
    model.driver.add_parameter(param, low=0.1, high=25.)

param = ''.join(["cadre.iSOC[0]"])
model.driver.add_parameter(param, low=0.2, high=1.)


finangles = "cadre.finAngle"
antangles = "cadre.antAngle"
model.driver.add_parameter(finangles, low=0, high=np.pi/2.)
model.driver.add_parameter(antangles, low=0, high=np.pi)

#add objective
obj = "cadre.Data_Final"
model.driver.add_objective(obj)

model.run()


#for item in sorted(model.driver.workflow.get_interior_edges()):
#    print item
#inputs = ['Comm_AntRotation.antAngle']#, 'Solar_ExposedArea.finAngle'
#inputs =  ['BsplineParameters.CP_P_comm']
#outputs =  ['Comm_DataDownloaded.Data']
#model.cadre.driver.workflow.check_gradient(inputs=inputs, outputs=outputs)
