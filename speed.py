import numpy as np
import pickle

from openmdao.main.api import Assembly, set_as_top

from CADRE.attitude import Attitude_Angular, Attitude_AngularRates, \
     Attitude_Attitude, Attitude_Roll, Attitude_RotationMtx, \
     Attitude_RotationMtxRates, Attitude_Sideslip, Attitude_Torque
from CADRE.battery import BatteryConstraints, BatteryPower, BatterySOC
from CADRE.parameters import BsplineParameters
from CADRE.comm import Comm_AntRotation, Comm_AntRotationMtx, Comm_BitRate, \
     Comm_DataDownloaded, Comm_Distance, Comm_EarthsSpin, Comm_EarthsSpinMtx, \
     Comm_GainPattern, Comm_GSposEarth, Comm_GSposECI, Comm_LOS, Comm_VectorAnt, \
     Comm_VectorBody, Comm_VectorECI, Comm_VectorSpherical
#from MultiPtParameters import MultiPtParameters ??
from CADRE.orbit import Orbit_Initial, Orbit_Dynamics
from CADRE.reactionwheel import ReactionWheel_Motor, ReactionWheel_Power, \
     ReactionWheel_Torque, ReactionWheel_Dynamics
from CADRE.solar import Solar_ExposedArea
from CADRE.sun import Sun_LOS, Sun_PositionBody, Sun_PositionECI,\
     Sun_PositionSpherical
from CADRE.thermal_temperature import ThermalTemperature
from CADRE.power import Power_CellVoltage, Power_SolarPower, Power_Total


NTIME = 1500

cadre = set_as_top(Assembly())

#cadre.add('comp', Attitude_Roll(NTIME))
#inputs = ['comp.Gamma']
#outputs = ['comp.O_BR']
#shape = cadre.comp.Gamma.shape
#cadre.comp.Gamma = np.random.random(shape)

#cadre.add('comp', ReactionWheel_Dynamics(NTIME))
#shape = cadre.comp.w_B.shape
#cadre.comp.w_B = np.random.random(shape)*1e-4
#shape = cadre.comp.T_RW.shape
#cadre.comp.T_RW = np.random.random(shape)*1e-9
#shape = cadre.comp.w_RW0.shape
##cadre.comp.w_RW0 = np.random.random(shape)
#inputs = ['comp.T_RW']
#outputs = ['comp.w_RW']

#cadre.add('comp', ThermalTemperature(NTIME))
#shape = cadre.comp.exposedArea.shape
#cadre.comp.exposedArea = np.random.random(shape)
#shape = cadre.comp.cellInstd.shape
#cadre.comp.cellInstd = np.random.random(shape)
#shape = cadre.comp.LOS.shape
#cadre.comp.LOS = np.random.random(shape)
#shape = cadre.comp.P_comm.shape
#cadre.comp.P_comm = np.random.random(shape)
#inputs = ['comp.exposedArea', 'comp.cellInstd',
          #'comp.LOS', 'comp.P_comm']
#outputs = ['comp.temperature']

#cadre.add('comp', Solar_ExposedArea(NTIME))
#cadre.comp.finAngle = .15
#shape = cadre.comp.azimuth.shape
#cadre.comp.azimuth = np.random.random(shape)
#shape = cadre.comp.elevation.shape
#cadre.comp.elevation = np.random.random(shape)
#inputs = ['comp.finAngle', 'comp.azimuth', 'comp.elevation']
#outputs = ['comp.exposedArea']

#cadre.add('comp', Power_CellVoltage(NTIME))
#shape = cadre.comp.LOS.shape
#cadre.comp.LOS = np.ones(shape)
#shape = cadre.comp.temperature.shape
#cadre.comp.temperature = np.random.random(shape)*40 + 240
#shape = cadre.comp.exposedArea.shape
#cadre.comp.exposedArea = np.random.random(shape)*1e-4
#shape = cadre.comp.Isetpt.shape
#cadre.comp.Isetpt = np.random.random(shape)*1e-2
#inputs = ['comp.LOS', 'comp.temperature', 'comp.exposedArea', 'comp.Isetpt']
#outputs = ['comp.V_sol']

#cadre.add('comp', Comm_GSposECI(NTIME))
#shape = cadre.comp.O_IE.shape
#cadre.comp.O_IE = np.ones(shape)
#shape = cadre.comp.r_e2g_E.shape
#cadre.comp.r_e2g_E = np.ones(shape)
#inputs = ['comp.O_IE', 'comp.r_e2g_E']
#outputs = ['comp.r_e2g_I']
#state0 = []

cadre.add('comp', Comm_VectorBody(NTIME))
shape = cadre.comp.r_b2g_I.shape
cadre.comp.r_b2g_I = np.ones(shape)
shape = cadre.comp.O_BI.shape
cadre.comp.O_BI = np.ones(shape)
inputs = ['r_b2g_I', 'O_BI']
outputs = ['r_b2g_B']
state0 = []

# --------------------------------------------------

cadre.driver.workflow.add('comp')
cadre.comp.h = .01
from time import time
tzero = time()
cadre.comp.execute()
for i in range(25):
    #cadre.comp.execute()
    cadre.comp.linearize()
    #cadre.driver.workflow.calc_gradient(inputs=inputs, outputs=outputs)
    #cadre.driver.workflow.calc_gradient(inputs=inputs, outputs=outputs, mode='adjoint')
    #cadre.driver.workflow.calc_gradient(inputs=inputs, outputs=outputs, fd=True)
print "Execution time", time()-tzero
