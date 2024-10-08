def log_errors(fail_reason): 
	with open('error_log.txt', 'a') as error_log:  
		error_log.write(fail_reason + '\n')