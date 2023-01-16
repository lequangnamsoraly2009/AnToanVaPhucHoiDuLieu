@echo off
for /l %%i in (0, 2, %1) do (
	del f%%i.dat
)