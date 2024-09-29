import time
import threading
import scripts.webscraping.webscraper as webscraper
import scripts.llm.openAIAgent as openAIAgent
import sql.sqlUtility as sqlUtility

timeoutEvent = threading.Event()

def timeFunction(timedFunction):
	startTime = time.time()
	try: 
		timedFunction()
	except Exception as e:
		print(f'Script terminated prematurely due to: {e}')
	finally:
		endTime = time.time()
		elapsedTimeSeconds = endTime - startTime
		elapsedTimeMinutes = elapsedTimeSeconds / 60
		print(f'Ran for: {elapsedTimeMinutes:.1f} minutes.')



def watchdog(func, maxTime):
    """Watchdog to monitor the function's runtime."""
    global timeoutEvent
    timeoutEvent.clear()
    
    def wrapper():
        try:
            func()  # Run the function
        except Exception as e:
            print(f"Function terminated due to: {e}")
        finally:
            timeoutEvent.set()

    # Run the function in a separate thread
    functionThread = threading.Thread(target=wrapper)
    functionThread.start()

    # Watchdog timer to check if the function runs too long
    startTime = time.time()
    while time.time() - startTime < maxTime:
        if timeoutEvent.is_set():
            return  # Stop the watchdog if the function completes early
        time.sleep(0.1)  # Check every 100ms

    # If we exceed the time limit, restart the function
    print(f"Function has exceeded {maxTime} seconds, restarting...")
    timeoutEvent.set()
    functionThread.join()
    watchdog(func, maxTime)

# if __name__== "__main__":

	# watchdog(webscraper.getStandardBattingAndPitchingTables, 15)

	#  sqlUtility.getDatabaseSchema()