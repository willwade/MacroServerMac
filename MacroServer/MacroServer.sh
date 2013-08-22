#! /bin/bash

LOGFILE='/var/run/MacroServerMac.pid'

case "$1" in
  start)
    echo "Starting MacroServer"
    ((/usr/bin/python MacroServerMac.py --notifier=Notifier --loglevel=debug) & echo $! > $LOGFILE &)
    ;;
  toggle)
    echo "Toggling MacroServer"
    if [ -f "$LOGFILE" ];
    then
       echo "Stopping MacroServer"
       kill -9 $(<"$LOGFILE")
       rm -f $LOGFILE
    else
       echo "Starting MacroServer"
       ((/usr/bin/python MacroServerMac.py --notifier=Notifier --loglevel=debug) & echo $! > $LOGFILE &)
    fi
    ;;
  stop)
    echo "Stopping MacroServer"
    kill -9 $(<"$LOGFILE")
    rm -f $LOGFILE
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: MacroServer.sh {start|stop|toggle}"
    exit 1
    ;;
esac

exit 0