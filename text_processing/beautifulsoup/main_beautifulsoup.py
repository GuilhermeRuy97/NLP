from bs4 import BeautifulSoup
import requests

def scrape_bs4_commands():
    """
    Scrapes BeautifulSoup commands and methods from the official documentation.
    
    Returns:
        dict: Dictionary containing categorized BS4 commands
    """
    url = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch documentation. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize dictionary to store commands by category
    commands = {
        'navigation': [],
        'searching': [],
        'modification': [],
        'output': []
    }
    
    # Find all code blocks and method names
    for section in soup.find_all(['div', 'section']):
        # Look for method names in code blocks
        code_blocks = section.find_all('code')
        for code in code_blocks:
            method = code.get_text().strip()
            
            # Categorize methods based on common patterns
            if any(x in method for x in ['.parent', '.sibling', '.next', '.previous', '.contents']):
                commands['navigation'].append(method)
            elif any(x in method for x in ['find', 'select', 'search']):
                commands['searching'].append(method)
            elif any(x in method for x in ['append', 'insert', 'replace', 'decompose', 'extract']):
                commands['modification'].append(method)
            elif any(x in method for x in ['prettify', 'get_text', 'string']):
                commands['output'].append(method)
    
    # Remove duplicates while preserving order
    for category in commands:
        commands[category] = list(dict.fromkeys(commands[category]))
    
    return commands

def print_commands(commands):
    """
    Prints the scraped commands in a formatted way.
    
    Args:
        commands (dict): Dictionary of categorized commands
    """
    for category, methods in commands.items():
        print(f"\n{category.upper()} METHODS:")
        print("-" * 50)
        for method in methods:
            print(f"- {method}")

if __name__ == "__main__":
    try:
        bs4_commands = scrape_bs4_commands()
        print_commands(bs4_commands)
    except Exception as e:
        print(f"Error: {str(e)}")