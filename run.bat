set codedirectory=D:\SISE\puzzles
for /r  %codedirectory% %%i in (*.txt) do (
python main.py dfs LUDR %%i 4x4_07_00212_sol.txt 4x4_07_00212_stats.txt)