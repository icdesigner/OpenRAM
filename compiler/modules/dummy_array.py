# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California 
# All rights reserved.
#
from bitcell_base_array import bitcell_base_array
from sram_factory import factory
from globals import OPTS


class dummy_array(bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, column_offset=0, mirror=0, name=""):
        super().__init__(rows=rows, cols=cols, column_offset=column_offset, name=name)
        self.mirror = mirror

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
        
    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place_array("dummy_r{0}_c{1}", self.mirror)

        self.add_layout_pins()

        self.add_boundary()
        
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        self.dummy_cell = factory.create(module_type="dummy_{}".format(OPTS.bitcell))
        self.add_mod(self.dummy_cell)

        self.cell = factory.create(module_type="bitcell")
        
    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        for col in range(self.column_size):
            for row in range(self.row_size):
                name = "bit_r{0}_c{1}".format(row, col)
                self.cell_inst[row, col]=self.add_inst(name=name,
                                                       mod=self.dummy_cell)
                self.connect_inst(self.get_bitcell_pins(row, col))

    def input_load(self):
        # FIXME: This appears to be old code from previous characterization. Needs to be updated.
        wl_wire = self.gen_wl_wire()
        return wl_wire.return_input_cap()
        