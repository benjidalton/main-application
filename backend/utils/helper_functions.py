from bs4 import BeautifulSoup

def pretty_print_html(html_content: BeautifulSoup, file_name: str, mode = 'w'):
	"""
		Pretty print content to an HTML file for easier investigation if necessary.

		Args:
			htmlContent (BeautifulSoup): * The HTML content to be written to the file.
			fileName (str): * The name of the file (without extension) where the content will be saved.
			mode (str): * The file mode for opening the file. Default is 'w' (write).
    """
	with open('./htmlFiles/' + file_name + '.html', mode, encoding='utf-8') as file:
		file.write(str(html_content))
		
def handle_escape_characeters(strings): 
	if isinstance(strings, str): 
		return strings.replace("'", "''")
	return [substring.replace("'", "''") for substring in strings]