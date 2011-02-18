killproc() {
  PID=$1
  kill $PID
  KILL=15
  TIMEOUT=5
  if [ ! -z $2 ]; then
      TIMEOUT=$2
  fi
  if [ ! -z $3 ]; then
      if [ $3 == 1 ]; then
          KILL=9
      fi
  fi
  TIMEOUTS=0
  PROC="/proc/$PID"
  STIME=$(date +%s)
  while [ -d $PROC ]
  do
      CTIME=$(date +%s)
      if [ $(($CTIME-$STIME)) -gt $TIMEOUT ]; then
          if [ $KILL == 9 ]; then
              kill -9 $PID
              TIMEOUTS=$(($TIMEOUTS+1))
              if [ $TIMEOUTS -gt 4 ]; then
                  return 1
              fi
          else
              return 1
          fi
      fi
      sleep 0.05
  done
  return 0
}
