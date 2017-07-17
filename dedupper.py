#!/usr/bin/env python3

import sys, os

class AsmDedupper:
    def __init__(self, ifname):
        self.ifname = ifname
        self.blocks = []
        self.markers = {'.cfi_startproc', '.cfi_endproc'}

    def dedup(self):
        substitution_count = 0
        self.load_blocks()
        for i in range(1, len(self.blocks)):
            cur_block = self.blocks[i]
            for j in range(i):
                trial_block = self.blocks[j]
                common_length = self.common_tail_length(cur_block, trial_block)
                if common_length > 4:
                    # FIXME go through all choices and pick the longest
                    # rather than the first one.
                    self.substitute_common(trial_block, cur_block, common_length, substitution_count)
                    substitution_count += 1
                    break

    def substitute_common(self, into_block, modified_block, common_length, label_id):
        assert(self.common_tail_length(into_block, modified_block) == common_length)
        label = 'Ltail_packer_%s' % label_id
        into_block.insert(-common_length, '%s:\n' % label)
        modified_block[-common_length+1:-1] = ['\tjmp %s\n' % label]

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

    def print_raw(self):
        for b in self.blocks:
            for line in b:
                print(line.rstrip())

if __name__ == '__main__':
    ifile = sys.argv[1]
    ad = AsmDedupper(ifile)
    ad.dedup()
    ad.print_raw()
    
