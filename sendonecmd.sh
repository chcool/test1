PYTHON=python
if [ $# -lt 1 ]; then
   echo "run it like $0 <hostlist> <cmd(s)> [python version number]"
fi

if [ $# -eq 3 ]; then
   echo "has \$3"
   if [ $3 -eq 3 ]; then
        echo "use python$3"
        PYTHON="python$3"
   else
       echo "\$2 is not 3, still use python2"
   fi

else
   echo "use python2"
fi

#eval "$PYTHON climain.py -a sendcmd.action -m 'show ver' -l $1"
eval "$PYTHON climain.py -a sendcmd.action -m \"$2\" -l \"$1\""
