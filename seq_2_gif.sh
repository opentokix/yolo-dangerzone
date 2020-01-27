#!/bin/bash

if [[ -z "$1" ]];
then
  me=`basename $0`
  echo "Usage: $me filename.mov"
  exit 1
fi

#This is just to get some uniq filenames
DATE=`date +%s`

mkdir ./frames_$DATE
ffmpeg -i $1 -vf scale=480:-1 -r 24 frames_${DATE}/ffout%03d.png
convert -delay .04167 -rotate 90 -loop 1 frames_${DATE}/ffout*.png output.gif
convert output.gif -fuzz 5% -layers Optimize output_final.gif
rm output.gif
rm -rf frames_${DATE}
