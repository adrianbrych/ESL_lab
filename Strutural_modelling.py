import random

from myhdl import Signal, always_comb, block, delay
from myhdl import intbv, instance, always, StopSimulation, always_seq
from myhdl import ResetSignal, modbv

random.seed(5)
randrange = random.randrange


@block 
def mux(a,b,z,sel):
    @always_comb
    def comb():
        if sel ==  1: 
            z.next = a
        else:
            z.next = b 
    return comb
    
@block
def test_mux():
    z, a, b, sel = [Signal(intbv(0)) for i in range(4)]
    mux_1 = mux(a, b, z, sel)
    
    @instance
    def stimulus():
        print("z a b sel")
        for i in range(12):
            a.next, b.next, sel.next = randrange(8), randrange(8), randrange(2)
            yield delay(10)
            print("%s %s %s %s" % (z, a, b, sel))  
    return stimulus, mux_1


@block
def inc(count, enable, clock, reset):

    @always_seq(clock.posedge, reset=reset)
    def seq():
        if enable:
            count.next = count + 1

    return seq


random.seed(1)
randrange = random.randrange
ACTIVE_LOW, INACTIVE_HIGH = 0, 1


@block
def testbench():
    m = 3
    count = Signal(modbv(0)[m:])
    enable = Signal(bool(0))
    clock  = Signal(bool(0))
    reset = ResetSignal(0, active=0, isasync=True)

    inc_1 = inc(count, enable, clock, reset)

    HALF_PERIOD = delay(10)

    @always(HALF_PERIOD)
    def clockGen():
        clock.next = not clock

    @instance
    def stimulus():
        reset.next = ACTIVE_LOW
        yield clock.negedge
        reset.next = INACTIVE_HIGH
        for i in range(16):
            enable.next = min(1, randrange(3))
            yield clock.negedge
        raise StopSimulation()

    @instance
    def monitor():
        print("enable  count")
        yield reset.posedge
        while 1:
            yield clock.posedge
            yield delay(1)
            print("   %s      %s" % (int(enable), count))

    return clockGen, stimulus, inc_1, monitor

tb = testbench()
tb.run_sim()

