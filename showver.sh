PYTHON=python
if [ $# -lt 1 ]; then
   echo "run it like $0 <hostlist> [python version number]"
fi

if [ $# -eq 2 ]; then
   echo "has \$2"
   if [ $2 -eq 3 ]; then
   echo "use python$2"
   PYTHON="python$2"
   else
       echo "\$2 is not 3, still use python2"
   fi

else
   echo "use python2"
fi

eval "$PYTHON climain.py -a sendcmd.action -m 'show ver' -l \"$1\" -p"
