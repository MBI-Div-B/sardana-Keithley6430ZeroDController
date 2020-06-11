import visa

from sardana import State
from sardana.pool.controller import ZeroDController
from sardana.pool.controller import Type, Description, DefaultValue

class Keithley6430ZeroDController(ZeroDController):
    """This class represents a dummy Sardana 0D controller."""
    
    ctrl_properties = {'resource': {Type: str, Description: 'GPIB resource', DefaultValue: 'GPIB0::3::INSTR'}}
    
    MaxDevice = 2

    def __init__(self, inst, props, *args, **kwargs):
        ZeroDController.__init__(self, inst, props, *args, **kwargs)

        self.rm = visa.ResourceManager('@py')
        self.inst = self.rm.open_resource(self.resource)
        print 'Keithley 6430 Initialization: ',
        idn = self.inst.query('*IDN?')
        if idn:
            print idn,
        else:
            print 'NOT initialized!'

        # settings
        self.inst.write('*RST')
        self.inst.write('REN')
        self.inst.write(':INIT')
        self.inst.write(':SENS:FUNC "CURR"')
        self.inst.write(':CURR:RANGE:AUTO ON')
        self.inst.write(':OUTP ON')
        
        self.data = []

    def AddDevice(self, ind):
        pass

    def DeleteDevice(self, ind):
        pass

    def StateOne(self, ind):
        return State.On, "OK"

    def ReadOne(self, ind):        
        if ind == 0:
            res = self.inst.query(':READ?')
            print(res)
            self.data = res.encode('utf8').split(',')
        
        return -1.0*float(self.data[ind])