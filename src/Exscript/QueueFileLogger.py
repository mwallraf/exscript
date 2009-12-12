# Copyright (C) 2007-2009 Samuel Abels.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import os, traceback
from Logfile     import Logfile
from QueueLogger import QueueLogger

class QueueFileLogger(QueueLogger):
    """
    A QueueLogger that stores logs into files.
    """

    def __init__(self, logdir, mode = 'a', delete = False):
        QueueLogger.__init__(self)
        self.logdir = logdir
        self.mode   = mode
        self.delete = delete
        if not os.path.exists(self.logdir):
            os.mkdir(self.logdir)

    def _get_logfile_name(self, action):
        logfile = action.get_name()
        retries = action.n_failures()
        if retries > 0:
            logfile += '_retry%d' % retries
        return os.path.join(self.logdir, logfile + '.log')

    def _on_action_started(self, action, conn):
        filename = self._get_logfile_name(action)
        log      = Logfile(filename, self.mode, self.delete)
        log.started(conn)
        self._add_log(action, log)