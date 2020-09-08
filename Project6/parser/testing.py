#testing.pyimport file
import os

# Execute testing for all items
for i in range(1, 11):
	os.system('python3 parser.py ' 
		+ os.path.join('sentences', str(i) + '.txt'))
