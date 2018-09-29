from birthday import getDOB
from cg import main
import json


if __name__ == '__main__':
	roll = input('Roll Number: ')
	dob = getDOB(roll)
	data = main(roll, dob)
	if data:
		json_data = json.loads(data)
		for sem in json_data:
			print('Semester ' + sem['semno'] + ': ' + sem['nccgsg'])
	else:
		print('Data mismatch!')