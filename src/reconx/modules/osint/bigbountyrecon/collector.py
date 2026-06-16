import urllib.parse
from typing import List
from reconx.core.models import Finding

class BigBountyReconCollector:
    def __init__(self):
        self.source = "bigbountyrecon"
    
    def collect(self, target: str) -> List[Finding]:
        target_encoded = urllib.parse.quote(target)
        findings = []
        
        dorks = [
            ("Directory Listing", f"site:{target_encoded} intitle:index.of"),
            ("Configuration Files", f"site:{target_encoded} ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini"),
            ("Database Files", f"site:{target_encoded} ext:sql | ext:dbf | ext:mdb"),
            ("WordPress", f"site:{target_encoded} inurl:wp- | inurl:wp-content | inurl:plugins | inurl:uploads | inurl:themes | inurl:download"),
            ("Log Files", f"site:{target_encoded} ext:log"),
            ("Backup Files", f"site:{target_encoded} ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup"),
            ("Login Pages", f"site:{target_encoded} inurl:login | inurl:signin | intitle:Login | intitle: signin | inurl:auth"),
            ("Exposed Documents", f"site:{target_encoded} ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv"),
            ("PHP Info", f"site:{target_encoded} ext:php intitle:phpinfo \"published by the PHP Group\""),
            ("Backdoors/Shells", f"site:{target_encoded}  inurl:shell | inurl:backdoor | inurl:wso | inurl:cmd | shadow | passwd | boot.ini | inurl:backdoor"),
            ("Install/Setup files", f"site:{target_encoded}  inurl:readme | inurl:license | inurl:install | inurl:setup | inurl:config"),
            ("SQL Errors", f"site:{target_encoded} intext:\"sql syntax near\" | intext:\"syntax error has occurred\" | intext:\"incorrect syntax near\" | intext:\"unexpected end of SQL command\" | intext:\"Warning: mysql_connect()\" | intext:\"Warning: mysql_query()\" | intext:\"Warning: pg_connect()\""),
            ("Open Redirects", f"site:{target_encoded} inurl:redir | inurl:url | inurl:redirect | inurl:return | inurl:src=http | inurl:r=http"),
            ("Apache Struts/Action", f"site:{target_encoded} ext:action | ext:struts | ext:do"),
            ("Pastebin", f"site:pastebin.com {target_encoded}"),
            ("LinkedIn Employees", f"site:linkedin.com employees {target_encoded}"),
            ("SharePoint Exposed", f".sharepoint.com/_vti_bin/webpartpages/asmx -docs -msdn -mdsec site:{target_encoded}"),
            ("WSDL and SOAP", f"site:{target_encoded} filetype:wsdl | filetype:WSDL | ext:svc | inurl:wsdl | Filetype: ?wsdl | inurl:asmx?wsdl | inurl:jws?wsdl | intitle:_vti_bin/sites.asmx?wsdl | inurl:_vti_bin/sites.asmx?wsdl"),
            ("GitHub Search", f"https://github.com/search?q=\"*.{target_encoded}\""),
            ("GitLab Search", f"inurl:gitlab {target_encoded}"),
            ("StackOverflow", f"site:stackoverflow.com \"{target_encoded}\""),
            ("S3 Buckets", f"site:.s3.amazonaws.com \"{target_encoded}\""),
            ("DigitalOcean Spaces", f"site:digitaloceanspaces.com \"{target_encoded}\""),
            ("Censys IPv4", f"https://censys.io/ipv4?q={target_encoded}"),
            ("Censys Domain", f"https://censys.io/domain?q={target_encoded}"),
            ("Censys Certs", f"https://censys.io/certificates?q={target_encoded}"),
            ("Shodan", f"https://www.shodan.io/search?query={target_encoded}"),
            ("OpenBugBounty", f"https://www.openbugbounty.org/search/?search={target_encoded}")
        ]
        
        for name, query in dorks:
            # We treat Google searches slightly differently than direct links.
            if query.startswith("http"):
                url = query
            else:
                url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
                
            findings.append(Finding(
                category="osint_dork",
                value=url,
                source=self.source,
                metadata={"dork_type": name, "raw_query": query}
            ))
            
        return findings
