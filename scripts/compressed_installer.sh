#!/bin/bash
# Self-extracting installer for open-with-chooser
set -e

echo "=== Open-with-chooser Auto-installer ==="

# Create temporary directory
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

# Extract embedded data (base64 encoded tar.gz)
sed -n '/^__DATA__$/,$p' "$0" | tail -n +2 | base64 -d | tar -xzf -

# Run installation
chmod +x install.sh
./install.sh

# Cleanup
cd /
rm -rf "$TMPDIR"

echo "Installation completed successfully!"
exit 0

__DATA__
H4sIAAAAAAAAA+1dZ3wUx9W/M9JJ6r333hECCwtMNdgYbFy+xzj3ni+x48QFt4Tt3E+OdxFn2zsF
7ASwDbbB2A5xwQ02YAy2wTbFBhtjg40Ng43BxmBjsLExBmODjcHGYGNsgzEGG4ON3d9/Zmd2d2Z3
9ub20vNMeE7S7s6+N2/ezLz3dmdmZ2YW/mfL7JkzZ858c9aMGdNnzJg2ffq0adOmTps6deq3pk6Z
MmXy5MmTJk6cOGHChPHjx48bN27s2LFjxowZPXr0qFGjRo4cOXz48GHDhg0dOnTIkCGDBw8eNGjQ
wIEDBwwY0L9/f5/P16dPn969e/fs2bN79+7dunXr2rVrly5dOnfu3KlTp44dO3bo0KF9+/bt2rVr
27Ztmzat27Rt067dN23btW/fvkOHDh07duzUqVPnzp27dOnStWvXbt26de/evUePHj179uzVq1fv
3r379OnTt2/fvn37+ny+Pn36+Hy+vn379u3bt2/fvn369u3bt2/fvn369u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3b
t2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/f
vn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn37
9u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2/fvn379u3bt2+f==