from PyQt5 import QtWidgets
import os, sys, time, traceback
from io import StringIO


class ExceptHook():

    log_path = '.'
    support_email = "support@nobodysupportsthis.com"
    version = 'v0.0'

    def excepthook(excType, excValue, tracebackobj):
        """
        Global function to catch unhandled exceptions.
        @param excType exception type
        @param excValue exception value
        @param tracebackobj traceback object
        """
        separator = '-' * 80
        logFile = os.path.join(ExceptHook.log_path, "error.log")
        notice = \
            """An unhandled exception occurred. Please report the problem\n""" \
            """via email to <%s>.\n\n""" \
            """A log has been written to "%s".\n\nError information:\n""" % \
            (ExceptHook.support_email, logFile)
        versionInfo = "version: {}\n\n".format(ExceptHook.version)
        timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

        tbinfofile = StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
        errmsg = '%s: \n%s' % (str(excType), str(excValue))
        sections = [separator, timeString, separator, errmsg, separator, tbinfo]
        msg = '\n'.join(sections)
        print(msg)
        try:
            f = open(logFile, "a")
            f.write(msg)
            f.write(versionInfo)
            f.close()
        except IOError:
            pass

        if True:  # Show Dialog?
            errorbox = QtWidgets.QMessageBox()
            errorbox.setText(str(notice) + str(msg) + str(versionInfo))
            errorbox.exec_()
