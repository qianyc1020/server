import sys

sys.path.append('/root/server/server')

from core import config
import core.globalvar as gl

config.init("/root/server/server/conf/pyg.conf")
# config.init("/home/pengyi/server/conf/pyg.conf")
gl.init()
