#!/usr/bin/env python3

import sys, os

class AsmDedupper:
    def __init__(self, ifname):
        self.ifname = ifname
        self.blocks = []
        self.markers = {'.cfi_startproc', '.cfi_endproc'}

    def dedup(self):
        self.load_blocks()
        for i in range(1, len(self.blocks)):
            cur_block = self.blocks[i]
            for j in range(i):
                trial_block = self.blocks[j]
                common_length = self.common_tail_length(cur_block, trial_block)
                if common_length > 4:
                    print('Found common block of size', common_length)
                    print(cur_block)
                    print(trial_block)
                    print(i, j)

    def common_tail_length(self, b1, b2):
        i1 = len(b1)-1
        i2 = len(b2)-1
        while i1 >= 0 and i2 >= 0 and b1[i1] == b2[i2]: # FIXME, skip plain loop targets
            i1 -= 1
            i2 -= 1
        return len(b1) - i1

    def load_blocks(self):
        with(open(self.ifname)) as ifile:
            current_block = []
            for line in ifile:
                current_block.append(line)
                stripped_line = line.strip()
                if stripped_line in self.markers:
                    self.blocks.append(current_block)
                    current_block = []
            self.blocks.append(current_block)

    def print_stats(self):
        print(self.blocks)
        print('Num of blocks:', len(self.blocks))

if __name__ == '__main__':
    ifile = sys.argv[1]
    ad = AsmDedupper(ifile)
    ad.dedup()
    #ad.print_stats()

