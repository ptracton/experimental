#! /usr/bin/env python3

'''
'''

import HSR_Base

class VectorSum(HSR_Base.HSR_Base):
    '''
    '''
    
    def __init__(self):
        '''
        '''
        super().__init__()
        self._r_scale = None
        return

    @property
    def r_scale(self):
        return self._r_scale

    @r_scale.setter
    def r_scale(self, data=None):
        self._r_scale = data
        return
        
    def calculate(self):
        '''
        Result = Vector1 + R_Scale*Vector2
        '''

        index = 0
        print ('Calculate Vector Sum')
        print ('RScale = 0x%08x' % self.r_scale)
        print ('Index\tVector1\tVector2\tMult\tSum\tSat')
        for index in range(len(self.vector1.vector)):
            mult = (self.r_scale * self.vector2.vector[index]) & 0x000000FFFFFFFFFF
            add = mult + (self.vector1.vector[index] << 24)
            sat = self.saturate(add)
            data_string = '{}\t{:>4}\t{:>4}\t{}\t{}\t{}'.format(index, self.vector1.vector[index], self.vector2.vector[index], mult, add, sat)
            print (data_string)
            self.result_vector.vector.append(sat)
            index = index + 1
        return
