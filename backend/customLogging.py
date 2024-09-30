def logErrors(failReason): 
	with open('error_log.txt', 'a') as error_log:  
		error_log.write(failReason + '\n')