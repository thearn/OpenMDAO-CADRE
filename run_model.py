
import sys
import numpy as np

from openmdao.lib.drivers.api import CONMINdriver
from openmdao.main.api import Assembly, set_as_top, Component
from openmdao.lib.datatypes.api import Array, Float
from pyopt_driver import pyopt_driver

from CADRE.CADRE_assembly import CADRE

class Dummy(Component):
    
    x = Array(iotype='in')
    y = Float(iotype='out')
    
    def execute(self):
        self.y = self.x[0, -1]
        
    def linearize(self):
        pass
    
    def provideJ(self):
        J = np.zeros((1, np.prod(self.x.shape)))
        J[0, -1] = 1.0
        
        return ('x',), ('y',), J

solar_raw1 = np.genfromtxt('CADRE/data/Solar/Area10.txt')
solar_raw2 = np.loadtxt("CADRE/data/Solar/Area_all.txt")
comm_rawGdata = np.genfromtxt('CADRE/data/Comm/Gain.txt')
comm_raw = (10**(comm_rawGdata/10.0)).reshape((361,361), order='F')
power_raw = np.genfromtxt('CADRE/data/Power/curve.dat')


n = 20
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

#model.add('driver', CONMINdriver())
#model.driver.iprint = 2
model.add("driver", pyopt_driver.pyOptDriver())
model.driver.optimizer = "SNOPT"
model.driver.options = {'Major optimality tolerance' : 1e-8}

# add parameters to driver
#for k in xrange(12):
    #for j in xrange(2):
        #param = ''.join(["cadre.CP_Isetpt[", str(k), ", ",
                         #str(j), "]"])
        #model.driver.add_parameter(param, low=0, high=0.4)
for k in xrange(2):
    param = ''.join(["cadre.CP_gamma[",str(k),"]"])
    model.driver.add_parameter(param, low=0, high=np.pi/2.)
#for k in xrange(2):
    #param = ''.join(["cadre.CP_P_comm[",str(k),"]"])
    #model.driver.add_parameter(param, low=0.1, high=25.)

# add battery constraints
#constr = ''.join(["cadre.ConCh <= 0"])
#model.driver.add_constraint(constr)

#constr = ''.join(["cadre.ConDs <= 0"])
#model.driver.add_constraint(constr)

#constr = ''.join(["cadre.ConS0 <= 0"])
#model.driver.add_constraint(constr)

#constr = ''.join(["cadre.ConS1 <= 0"])
#model.driver.add_constraint(constr)

constr = ''.join(["cadre.SOC[0][0] = cadre.SOC[0][-1]"])
#constr = ''.join(["cadre.SOC[0][0] <10000"])
model.driver.add_constraint(constr)

#param = ''.join(["cadre.iSOC[0]"])
#model.driver.add_parameter(param, low=0.2, high=1.)


#finangles = "cadre.finAngle"
#antangles = "cadre.antAngle"
#model.driver.add_parameter(finangles, low=0, high=np.pi/2.)
#model.driver.add_parameter(antangles, low=0, high=np.pi)
#model.driver.conmin_diff = False

#add objective
obj = "-cadre.Data[0][-1]"
model.driver.workflow.add(['cadre'])
#model.add('dumb', Dummy())
#model.connect('cadre.Data', 'dumb.x')
#model.driver.workflow.add(['cadre', 'dumb'])
#obj = "-dumb.y"

model.driver.add_objective(obj)

model.run()
print 'answer', model.cadre.Data[0, -1]#, model.dumb.y



#inputs =  ['Comm_BitRate.P_comm', 'Comm_BitRate.gain', 'Comm_BitRate.GSdist', 'Comm_BitRate.CommLOS']
#inputs = [('BsplineParameters.CP_Isetpt')]
#inputs = ['BsplineParameters.CP_Isetpt', 'BsplineParameters.CP_gamma', 'BsplineParameters.CP_P_comm']
#inputs = ['cadre.CP_Isetpt']
#inputs2 = ['cadre.CP_gamma']
inputs2 = ['cadre.CP_gamma']
#outputs =  ['Comm_DataDownloaded.Data']
outputs2 =  ['cadre.SOC[0][0]', 'cadre.SOC[0][-1]']
#outputs2 = ['cadre.Data']
#outputs2 = ['dumb.y']
#outputs2 = None


model.driver.clear_constraints()
model.driver.workflow.config_changed()
model.cadre.driver.workflow.config_changed()
J = model.driver.workflow.calc_gradient(inputs=None, outputs=None,
                                        mode='adjoint')
print J.shape
print J#[0, :]
print '\n'

model.driver.clear_constraints()
model.driver.workflow.config_changed()
model.cadre.driver.workflow.config_changed()
J = model.driver.workflow.calc_gradient(inputs=None, outputs=None,
                                        mode='forward')
print J.shape
print J#[0, :]
print '\n'

model.driver.clear_constraints()
model.driver.workflow.config_changed()
model.cadre.driver.workflow.config_changed()
J = model.driver.workflow.calc_gradient(inputs=None, outputs=None,
                                        mode='adjoint')
print J.shape
print J#[0, :]
print '\n'


model.driver.workflow.config_changed()
model.cadre.driver.workflow.config_changed()
J = model.driver.workflow.calc_gradient(inputs=inputs2, outputs=outputs2,
                                        fd=True)

print J.shape
print J#[0, :]
print '\n'

model.driver.workflow.config_changed()
J = model.driver.workflow.calc_gradient(inputs=inputs2, outputs=outputs2,
                                        fd=True)
print J.shape
print J#[0, :]
print '-------\n'

#model.cadre.driver.workflow.config_changed()
#J = model.cadre.driver.workflow.calc_gradient(inputs=inputs, outputs=outputs,
                                              #mode='adjoint')
#print J.shape
#print J[-1, :]
#print '\n'
#model.cadre.driver.workflow.config_changed()
#J = model.cadre.driver.workflow.calc_gradient(inputs=inputs, outputs=outputs,
                                              #fd=True)
#print J.shape
#print J[-1, :]

