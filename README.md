# Introspection

## Description
Introspection is a Python program designed to test all possible pages from a given URL to discover all available paths.

The program utilizes a pre-established list of keywords, along with HTTP requests to check the availability of pages on the target server. It then provides information about the HTTP responses received for each tested path.

## Features
- Automatic exploration of all possible paths from a URL
- Use of threads to optimize performance
- Display of HTTP responses received for each tested path
- Easy-to-use with a command-line interface

## Installation
1. Ensure you have Python installed on your system.
2. Clone this GitHub repository to your machine:
   ```bash
   git clone https://github.com/Ol1vi3R/introspection.git
3. Navigate to the project directory:
   ```bash
   cd introspection
4. Install the required dependencies by running the following command:
   ```bash
   pip install -r requirements.txt

## Usage
   To run the program, use the following command:
   ```bash
   python3 introspection.py <target_URL>
   ```
   Make sure to replace <target_URL> with the URL you want to explore.

## Example
   Suppose you want to explore possible pages on the site https://example.com. You can run the program as follows:
   ```bash
   python3 introspection.py https://example.com
   ```
## Disclaimer
   This program is intended for educational or security auditing purposes on systems for which you have authorization to perform testing. Using this program on systems without authorization may be unlawful. The author is not responsible for any misuse or illegal use of this program.

## Author
   This program was developed by Ol1vi3R.

## License
   This project is licensed under the BSD 3-Clause "New" or "Revised" License. See the LICENSE file for more details.