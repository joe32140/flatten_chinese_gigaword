#!/usr/bin/env bash
set -e

# Path to Gigaword corpus with all data files decompressed.
export GIGAWORDDIR=$1
# The directory to write output to
export OUTPUTDIR=$2
# The number of jobs to run at once
export NUMJOBS=$3

#echo "Unziping files..."
#find ${GIGAWORDDIR}/data/*/*.gz | parallel --gnu --progress -j ${NUMJOBS} gzip -d  \{\}

echo "Flattening Gigaword with ${NUMJOBS} processes..."
mkdir -p $OUTPUTDIR
find ${GIGAWORDDIR}/data/*/* | parallel --gnu --progress -j ${NUMJOBS} python flatten_one_gigaword.py \
                                        --gigaword-path \{\} --output-dir ${OUTPUTDIR}

#from simplified chinese to tranditional chinese
#find ${GIGAWORDDIR}/data/*/*.gz | parallel --gnu --progress -j ${NUMJOBS} python -m opencc -i \{\} -o \{\} -c s2twp

echo "Combining the flattened files into one..."
cat ${OUTPUTDIR}/*.flat > ${OUTPUTDIR}/flattened_paragraph_gigaword.txt
cat ${OUTPUTDIR}/*.headline > ${OUTPUTDIR}/flattened_heaadline_gigaword.txt
echo "Removing tmp files..."
rm ${OUTPUTDIR}/*.flat ${OUTPUTDIR}/*.headline
