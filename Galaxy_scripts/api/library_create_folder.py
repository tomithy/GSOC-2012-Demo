#!/usr/bin/env python

import os, sys
sys.path.insert( 0, os.path.dirname( __file__ ) )
from common import submit

try:
    data = {}
    data[ 'folder_id' ] = sys.argv[3]
    data[ 'name' ] = sys.argv[4]
    data[ 'create_type' ] = 'folder'
except IndexError:
    print 'usage: %s key url folder_id name [description]' % os.path.basename( sys.argv[0] )
    sys.exit( 1 )
try:
    data[ 'description' ] = sys.argv[5]
except IndexError:
    data[ 'description' ] = ''

submit( sys.argv[1], sys.argv[2], data )
