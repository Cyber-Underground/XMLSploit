# XMLSploit

XMLSploit is a powerful tool designed to aid in the exploration and analysis of XML vulnerabilities. This repository contains a collection of XML payloads, along with a Python script for testing and exploiting XML-related security weaknesses.

## Features

- **Comprehensive XML Payloads:** Explore a wide range of XML vulnerabilities with meticulously crafted payloads, covering the following exploit scenarios:
  - Exfiltration Fork Bomb
  - Simple XML Entity
  - Parameter Entity Expanding to External Entity
  - External Entity Inclusion
  - XXE: Entity 
  - XXE: File Disclosure
  - XXE: Denial-of-Service 
  - XXE: Local File Inclusion 
  - XXE: Blind Local File Inclusion 
  - XXE: Access Control Bypass (Loading Restricted Resources - PHP example)
  - XXE: SSRF (Server Side Request Forgery) Example
  - XXE: Remote Attack (Through External XML Inclusion) Example
  - XXE: UTF-7 Example
  - XXE: Base64 Encoded 
  - XXE: XXE inside SOAP 
  - XXE: XXE inside SVG

## Usage

1. **Clone the Repository:**

    ```bash
    git clone [https://github.com/your-username/XMLSploit.git](https://github.com/Cyber-Underground/XMLSploit/)
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Script:**

    ```bash
    python xmlsploit.py
    ```

4. **Follow the On-Screen Instructions:**
    
    - Choose an option to send XML payloads to a target URL or scan a website for XML files.
    - Select a payload from the provided list.
    - Enter the target URL or website URL as prompted.
    - Customize the number of threads for concurrent execution if desired.

## Contributions

Contributions to XMLSploit are welcome! If you have ideas for new payloads, feature enhancements, or bug fixes, feel free to open an issue or submit a pull request.

## License

XMLSploit is licensed under the [MIT License](LICENSE).
