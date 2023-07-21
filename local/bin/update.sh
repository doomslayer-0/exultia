#!/bin/bash 

upd="$(checkupdates | wc -l)"
printf " %s  " $upd
