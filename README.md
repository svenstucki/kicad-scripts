# KiCad Scripts

A place where I collect scripts for automating KiCad.


## ```fix_vias.py```

This script is meant to fix vias that have no net association due to the way
KiCad handles stitching vias ([this post](http://www.svenstucki.ch/wp/2017/07/via-stitching-in-kicad-problem-and-workaround/)
explains the problem in more detail).

It does this by replacing all vias not associated to a net by a footprint
consisting of a single through hole pad with the same dimensions connected to
the GND net. This is not always the right behaviour, especially if there are
multiple different copper pours of different nets (it won't work at all in that
case).

The script is called like this:

    ./fix_vias.py <input .kicad_pcb file>

It will modify the input file, creating a backup first is highly recommended.
