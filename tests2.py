import unittest

from myhdl import Simulation, Signal, delay, intbv, bin, always_comb

MAX_WIDTH = 11

L1 = ['0', '1']
L2 = ['00', '01', '11', '10']
L3 = ['000', '001', '011', '010', '110', '111', '101', '100']

def nextLn(Ln):
    """ Return Gray code Ln+1, given Ln. """
    Ln0 = ['0' + codeword for codeword in Ln]
    Ln1 = ['1' + codeword for codeword in Ln]
    Ln1.reverse()
    return Ln0 + Ln1

def bin2gray(B, G):
    # DUMMY PLACEHOLDER
    """ Gray encoder.

    B -- binary input
    G -- Gray encoded output
    """
    
    @always_comb
    def logic():
        G.next = (B>>1) ^ B

    return logic

class TestOriginalGrayCode(unittest.TestCase):

    def testOriginalGrayCode(self):
        """Check that the code is an original Gray code."""

        Rn = []

        def stimulus(B, G, n):
            for i in range(2**n):
                B.next = intbv(i)
                yield delay(10)
                Rn.append(bin(G, width=n))

        Ln = ['0', '1'] # n == 1
        for w in range(2, MAX_WIDTH):
            Ln = nextLn(Ln)
            del Rn[:]
            B = Signal(intbv(0)[w:])
            G = Signal(intbv(0)[w:])
            dut = bin2gray(B, G)
            stim = stimulus(B, G, w)
            sim = Simulation(dut, stim)
            sim.run(quiet=1)
            self.assertEqual(Ln, Rn)


if __name__ == '__main__':
    unittest.main(verbosity=2)
