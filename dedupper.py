#!/usr/bin/env python3

import sys, os

class AsmDedupper:
    def __init__(self, ifname):
        self.ifname = ifname
        self.blocks = []
        self.markers = {'.cfi_startproc', '.cfi_endproc'}

    def dedup(self):
        with(open(self.ifname)) as ifile:
            current_block = []
            for line in ifile:
                current_block.append(line)
                stripped_line = line.strip()
                if stripped_line in self.markers:
                    self.blocks.append(current_block)
                    current_block = []
            self.blocks.append(current_block)

    def print(self):
        print(self.blocks)
        print('Num of blocks:', len(self.blocks))

if __name__ == '__main__':
    ifile = sys.argv[1]
    ad = AsmDedupper(ifile)
    ad.dedup()
    ad.print()

