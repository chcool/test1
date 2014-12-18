PYTHON=python
if [ $# -lt 1 ]; then
   echo "run it like $0 <hostlist> <cmd(s)> [python version number]"
fi


last=$#
echo "python$last"
#exit

if [ $last -eq 3 ]; then
   echo "last param = 3,use python3"
   PYTHON="python$3"
else
   echo "use python2"
fi

eval "$PYTHON climain.py -a sendcmd.action -m \"$2\" -l \"$1\""
