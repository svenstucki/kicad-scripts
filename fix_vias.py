#!/usr/bin/env python

import sys

import pcbnew


def fmt(value, suffix=''):
    # format KiCad value (integer, 10e-6mm)
    v = float(value) * (10**-6)
    return '{:.2f}{}'.format(v, suffix)

def fmtu(value):
    return fmt(value, 'mm')


# convert mm value to KiCad internal size value
def mm2kicad(value):
    return int(value / 10**-6)


def get_via_module(board, drill, diameter, net):
    n = 'VIA-{}-{}'.format(fmt(drill), fmt(diameter))

    # instantiate new module
    m = pcbnew.MODULE(board)
    #m.SetReference('REF**')
    #m.SetValue(n)
    m.SetLastEditTime(pcbnew.GetNewTimeStamp())

    # adjust reference and value display settings
    # TODO: m.GraphicalItems() does not yield any items, find a way to hide ref/value

    lib_id = pcbnew.LIB_ID(n)
    m.SetFPID(lib_id)

    # create through-hole pad
    pad = pcbnew.D_PAD(m)
    pad.SetPadName('1')
    pad.SetNet(net)
    pad.SetPosition(pcbnew.wxPoint(0, 0))

    pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
    pad.SetSize(pcbnew.wxSize(diameter, diameter))

    pad.SetDrillShape(pcbnew.PAD_DRILL_SHAPE_CIRCLE)
    pad.SetDrillSize(pcbnew.wxSize(drill, drill))

    pad.SetLayerSet(pcbnew.LSET.AllCuMask())
    pad.SetZoneConnection(pcbnew.PAD_ZONE_CONN_FULL)

    # add pad to module
    m.Add(pad)

    return m


if __name__ == '__main__':
    fn = sys.argv[1]

    # load board
    board = pcbnew.LoadBoard(fn)
    if not board:
        sys.exit(1)

    nets = board.GetNetsByNetcode()
    #print('Nets:')
    #for c, net in nets.items():
    #    print(" * {:3d} {}".format(c, net.GetNetname()))
    #print

    search_net = nets[0]
    replace_net = board.FindNet('GND')

    print('Finding vias in net 0:')
    tracks = board.TracksInNet(search_net.GetNet())
    for t in tracks:
        # check if track is via
        is_via = pcbnew.VIA.ClassOf(t)
        if not is_via:
            continue

        # cast track to via
        via = pcbnew.Cast_to_VIA(t)
        print('* ({}, {}) drill {} diameter {}'.format(
            fmt(via.GetStart().x), fmt(via.GetStart().y),
            fmtu(via.GetDrill()),
            fmtu(via.GetWidth())
        ))

        # create replacement module
        via_m = get_via_module(board, via.GetDrill(), via.GetWidth(), replace_net)
        via_m.SetPosition(via.GetStart())
        via_m.SetTimeStamp(via.GetTimeStamp())

        # replace via with module
        board.Remove(via)
        board.Add(via_m)

    board.Save(fn)

