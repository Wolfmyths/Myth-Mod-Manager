@echo off

echo Game Path: %1
echo Drive: %2
echo Exe Name: %3
echo Args: %4

cd /%2 %1

start %3 %4