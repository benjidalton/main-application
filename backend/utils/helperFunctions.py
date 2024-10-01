from bs4 import BeautifulSoup

def prettyPrintHtml(htmlContent: BeautifulSoup, fileName: str, mode = 'w'):
	"""
		Pretty print content to an HTML file for easier investigation if necessary.

		Args:
			htmlContent (BeautifulSoup): * The HTML content to be written to the file.
			fileName (str): * The name of the file (without extension) where the content will be saved.
			mode (str): * The file mode for opening the file. Default is 'w' (write).
    """
	with open('./htmlFiles/' + fileName + '.html', mode, encoding='utf-8') as file:
		file.write(str(htmlContent))
		
def handleEscapeCharaceters(strings): 
	if isinstance(strings, str): 
		return strings.replace("'", "''")
	return [substring.replace("'", "''") for substring in strings]