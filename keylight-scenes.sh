#!/bin/bash

DAYLIGHT=6900
COOL=5500
MIDDLE=4000
WARM=3200

HIGH=100
MID=50
LOW=25

if [ $# -eq 0 ]
then
    echo "no argument supplies"
    exit 0
fi

case $1 in
    midday)
        echo "midday setting"
        keylight --host kl-left.l.opentokix.com --color $DAYLIGHT --brightness $MID
        keylight --host kl-right.l.opentokix.com --color $DAYLIGHT --brightness $MID
    ;;
    cool)
        echo "midday setting"
        keylight --host kl-left.l.opentokix.com --color $COOL --brightness $MID
        keylight --host kl-right.l.opentokix.com --color $COOL --brightness $MID
    ;;

    warm)
        echo "warm setting"
        keylight --host kl-left.l.opentokix.com --color $WARM --brightness $MID
        keylight --host kl-right.l.opentokix.com --color $WARM --brightness $MID
    ;;
    low)
        echo "low setting"
        keylight --host kl-left.l.opentokix.com --brightness $LOW
        keylight --host kl-right.l.opentokix.com --brightness $LOW
    ;;
    mid)
        echo "mid setting"
        keylight --host kl-left.l.opentokix.com --brightness $MID
        keylight --host kl-right.l.opentokix.com --brightness $MID
    ;;
    high)
        echo "high setting"
        keylight --host kl-left.l.opentokix.com --brightness $HIGH
        keylight --host kl-right.l.opentokix.com --brightness $HIGH
    ;;
    art)
        echo "high setting"
        keylight --host kl-left.l.opentokix.com --color $WARM --brightness $MID
        keylight --host kl-right.l.opentokix.com --color $COOL --brightness $HIGH

    ;;
    off)
        keylight --host kl-left.l.opentokix.com --off
        keylight --host kl-right.l.opentokix.com --off
    ;;
    on)
        keylight --host kl-left.l.opentokix.com --on
        keylight --host kl-right.l.opentokix.com --on
    ;;
esac