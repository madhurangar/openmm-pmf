# coding: utf-8
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit as u

class ForceReporter(object):
    def __init__(self, file, reportInterval):
        self._out = open(file, 'w')
        self._out.write("\"Time (ps)\"  Index fx fy fz \n")
        self._reportInterval = reportInterval

    def __del__(self):
        self._out.close()

    def describeNextReport(self, simulation):
        steps = self._reportInterval - simulation.currentStep%self._reportInterval
        return (steps, False, False, True, False)

    def report(self, simulation, state):
        forces = state.getForces().value_in_unit(u.kilojoules/u.mole/u.nanometer)
        for atom, f in zip(simulation.topology.atoms(), forces):
          if atom.index in [0]:
            self._out.write('%s %g %g %g %g\n' % (state.getTime()/u.picosecond, atom.index, f[0], f[1], f[2]))
