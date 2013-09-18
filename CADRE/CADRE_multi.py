from openmdao.main.api import Assembly
from openmdao.main.datatypes.api import Float, Array, Int
import numpy as np
from CADRE_assembly import CADRE
from pyopt_driver import pyopt_driver
from openmdao.lib.drivers.api import CONMINdriver

class CADRE_Optimization(Assembly):

    def __init__(self, n=1500, m=300):
        super(CADRE_Optimization, self).__init__()

        npts = 2
        #add SNOPT driver
        self.add("driver", pyopt_driver.pyOptDriver())
        self.driver.optimizer = "SNOPT"
        self.driver.options = {'Major optimality tolerance' : 1e-8,
                                'Iterations limit' : 2000000}

        #self.add("driver", CONMINdriver())

        # Raw data to load
        solar_raw1 = np.genfromtxt('CADRE/data/Solar/Area10.txt')
        solar_raw2 = np.loadtxt("CADRE/data/Solar/Area_all.txt")
        comm_rawGdata = np.genfromtxt('CADRE/data/Comm/Gain.txt')
        comm_raw = (10**(comm_rawGdata/10.0)).reshape((361,361),order='F')
        power_raw = np.genfromtxt('CADRE/data/Power/curve.dat')

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

        for i in xrange(npts):
            aname = ''.join(["pt", str(i)])
            self.add(aname, CADRE(n, m, solar_raw1, solar_raw2,
                                  comm_raw, power_raw))
            self.get(aname).set("LD", LDs[i])
            self.get(aname).set("r_e2b_I0", r_e2b_I0s[i])

            
            # add parameters to driver
            for k in xrange(12):
                print "adding parameter: CP_Isetpt",k
                for j in xrange(m):
                    param = ''.join(["pt", str(i), ".CP_Isetpt[(", str(k), ", ",
                                     str(j), ")]"])
                    self.driver.add_parameter(param, low=0, high=0.4)
            for k in xrange(m):
                print "adding parameter: CP_gamma",k
                param = ''.join(["pt",str(i),".CP_gamma[",str(k),"]"])
                self.driver.add_parameter(param, low=0, high=np.pi/2.)
            for k in xrange(m):
                print "adding parameter: CP_comm",k
                param = ''.join(["pt",str(i),".CP_P_comm[",str(k),"]"])
                self.driver.add_parameter(param, low=0.0, high=25.)

            param = ''.join(["pt",str(i),".iSOC[0]"])
            self.driver.add_parameter(param, low=0.2, high=1.)

            # add battery constraints
            constr = ''.join(["pt",str(i),".ConCh <= 0"])
            self.driver.add_constraint(constr)

            constr = ''.join(["pt",str(i),".ConDs <= 0"])
            self.driver.add_constraint(constr)

            constr = ''.join(["pt",str(i),".ConS0 <= 0"])
            self.driver.add_constraint(constr)

            constr = ''.join(["pt",str(i),".ConS1 <= 0"])
            self.driver.add_constraint(constr)

            constr = ''.join(["pt",str(i),".SOC[0] = pt",
                              str(i),".SOC[-1]"])
            #self.driver.add_constraint(constr)
            
        
        #add rest of parameters to driver
        for i in xrange(7):
            print "adding constraint: Cellinstd",i
            for k in xrange(12):
                param = [''.join(["pt",str(j),".cellInstd[(",str(i),
                ",",str(k),")]"]) for j in xrange(npts)]
                self.driver.add_parameter(param, low=0, high=1)
        
        finangles = ["pt"+str(i)+".finAngle" for i in xrange(npts)]
        antangles = ["pt"+str(i)+".antAngle" for i in xrange(npts)]
        self.driver.add_parameter(finangles, low=0, high=np.pi/2.)
        self.driver.add_parameter(antangles, low=0, high=np.pi)

        #add objective
        obj = ''.join([''.join(["-pt",str(i),".Data[0, -1]"]) for i in xrange(npts)])
        self.driver.add_objective(obj)

if __name__ == "__main__":
    import time
    a = CADRE_Optimization(50)
    a.driver.iprint = 2
    print a.pt0.Data[0,-1]
    t = time.time()
    a.run()
    print a.pt0.Data[0,-1], time.time() - t

    # Data downloaded for each design pt (pkl file):
    #[5066.3720823070635, 5384.7361694638694, 4209.5489047612755, 6067.161589929754, 4760.663169148871, 5403.4000465009376]
    #Total:
    #30891.8819621


