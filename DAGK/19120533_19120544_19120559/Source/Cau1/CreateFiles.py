import sys
from pathlib import Path

num_files = int(sys.argv[1])
path = Path('.')
try:
        path = Path(sys.argv[2])
except:
        pass

cluster_1 = '0\n0\n'
cluster_2 = '0\n'*(1025//3 + 5)

for i in range(0, num_files + 1, 2):
	file_name = path / f"f{i}.dat"
	with open(file_name, 'w') as f:
		f.write(cluster_2)

for i in range(1, num_files + 1, 2):
	file_name = path / f"f{i}.dat"
	with open(file_name, 'w') as f:
		f.write(cluster_1)
