#!/bin/bash
rangelimitupper=$4
rangelimitlower=$3
cdir='/home/fieseler/Documents/htwsaar/thesis/Implementation/keavem/tests/data'
inpf="${cdir}/$1"
outf="${cdir}/$2"

[[ $# -ne 4 ]] &&  echo "usage: $0 [Inputfile] [Outputfile] [Lower bound:int] [Upper bound:int]" &&  exit 1
rm $outf 2>/dev/null && touch $outf

for i in $(seq ${rangelimitlower} ${rangelimitupper})
do
	curraddr=$(od -Ax -t x1 $inpf | sed "${i}!d" | cut -d' ' -f1)
	currline=$(od -An -t x1 $inpf | sed "${i}!d" | sed s/' '/'\\x'/g)
	echo "line $i:$curraddr:$currline"
	printf $currline >> $outf
done
