#! /bin/bash

if [ -z $1 ]; then
  echo "You need to provide the timeout"
  echo "run-ikaros.sh <timeout> <outdir>"
  exit 1
fi

if [ -z $2 ]; then
  echo "You need to provide the output dir"
  echo "run-ikaros.sh <timeout> <outdir>"
  exit 1
fi

outdir=$2
mkdir -p $outdir
rm -f $outdir/*

timeout $1 ikaros --language scala --pattern-gen construction
touch $2/scalac_construction

timeout $1 ikaros --language scala --pattern-gen z3
touch $2/scalac_z3

timeout $1 ikaros --language java --pattern-gen z3
touch $2/javac_z3

timeout $1 ikaros --language java --pattern-gen construction
touch $2/javac_construction
