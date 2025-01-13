import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import urljoin
from googlesearch import search
import validators
import re



from bs4 import BeautifulSoup
import requests

import whois



# Index(['Index', 'UsingIP', 'LongURL', 'ShortURL', 'Symbol@', 'Redirecting//',
#       'PrefixSuffix-', 'SubDomains', 'HTTPS', 'DomainRegLen', 'Favicon',
#       'NonStdPort', 'HTTPSDomainURL', 'RequestURL', 'AnchorURL',
#       'LinksInScriptTags', 'ServerFormHandler', 'InfoEmail', 'AbnormalURL',
#       'WebsiteForwarding', 'StatusBarCust', 'DisableRightClick',
#       'UsingPopupWindow', 'IframeRedirection', 'AgeofDomain', 'DNSRecording',
#       'WebsiteTraffic', 'PageRank', 'GoogleIndex', 'LinksPointingToPage',
#       'StatsReport', 'class'],
#      dtype='object')

# Sources from https://eprints.hud.ac.uk/id/eprint/24330/6/MohammadPhishing14July2015.pdf

# 1 is phishing, -1 is not, 0 is suspicious

def is_ip(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.split(':')[0]  # Remove port if present
        
        # Check if domain is IPv4 address
        parts = domain.split('.')
        if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
            return 1
            
        return -1
    except:
        return 1  # Error parsing URL, suspicious

def is_long_url(url):
    if len(url) < 54:
        return -1
    if len(url) >= 75:
        return 0
    return 1

def is_short_url(domain):
    if "TinyURL" in domain or "bit.ly" in domain:
        return 1

    return -1

def has_at_symbol(domain):
    return 1 if "@" in domain else -1

def has_redirecting_slash(url):
    return 1 if "//" in url[8:] else -1

def has_prefix_suffix(domain):
    return 1 if "-" in domain else -1

def has_subdomains(domain):
    if domain.count(".") > 2:
        return 1
    if domain.count(".") == 1:
        return -1
    return 0

def has_https(url):
        
    try:
        parsed = urlparse(url)
        hostname = parsed.netloc
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                if cert:
                    return -1  # Has valid HTTPS cert
                return 1  # Has HTTPS but invalid cert
    except:
        return 1  # No valid HTTPS
    

def classify_domain(domain):
    try:
        domain_info = whois.whois(domain)
        
        expiration_date = domain_info.expiration_date
        
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
                
        if expiration_date:
            current_date = datetime.now()
            time_remaining = (expiration_date - current_date).days / 365.25  # Convert days to years
            
            if time_remaining <= 1:
                return 1
            else:
                return -1
        else:
            return 1  
    except Exception as e:
        print(f"Error checking domain registration: {e}")
        return 1

# No easy way to do this in python
def has_favicon(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        favicon = soup.find("link", rel="shortcut icon") 
               
        if favicon is None:
            favicon = soup.find("link", rel="icon")    
                
        if favicon:
            favicon_url = urljoin(url, favicon.get("href"))

            
            page_domain = urlparse(url).netloc
            favicon_domain = urlparse(favicon_url).netloc
            
            if page_domain != favicon_domain:
                return 1
            
            return -1
    
        default_favicon = urljoin(url, "/favicon.ico")
        default_response = requests.get(default_favicon)
        if default_response.status_code == 200:
            return -1

        return 1
    except:
        return 1  # Error parsing URL, suspicious


def has_nonstd_port(url):
    try:
        parsed = urlparse(url)
        port = parsed.port
        if port is None:
            return -1  # Using standard port
        if port in [80, 443]:
            return -1  # Using standard HTTP/HTTPS ports
        return 1  # Using non-standard port
    except:
        return 1  # Error parsing URL, suspicious
    
def has_https_domain_url(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        if "https" in domain:
            return 1
        return -1
    except:
        return 1 



def has_external_resources(url):   
    try:
        count = 0
        totalCount = 0 
        
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        domain = urlparse(url).netloc
        
        for tag in soup.find_all(["script", "link", "img", "video", "audio"]):
            resource_url = tag.get("src") or tag.get("href")
            if resource_url:
                full_url = urljoin(url, resource_url)
                resource_domain = urlparse(full_url).netloc
                
                if domain not in resource_domain:
                    count += 1
                
                totalCount += 1
        
        percent = count / totalCount * 100
        
        if totalCount == 0:
            return -1
        
        if percent < 22:
            return -1
    
        if percent >= 61:
            return 1

        return 0

    except:
        return 1

def check_anchors(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        domain = urlparse(url).netloc
        
        external_count = 0
        total = 0
        
        for anc in soup.find_all("a"):
            href = anc.get("href")
            if href:
                full_url = urljoin(url, href)
                domain_url = urlparse(full_url).netloc
                
                
                if domain not in domain_url or href in ['#', '#content', '#skip', 'javascript:void(0)']:
                    external_count += 1
                
                total += 1
        
        if total == 0:
            return -1
        
        percent = external_count / total * 100
        
        if percent < 31:
            return -1

        if percent >= 67:
            return 1
        
        return 0
    
    except Exception as e:
        return 1
    

def check_links_in_tags(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        domain = urlparse(url).netloc
        
        external_count = 0
        total = 0
        
        for tag in soup.find_all(["script", "link", "img", "video", "audio"]):
            resource_url = tag.get("src") or tag.get("href")
            if resource_url:
                full_url = urljoin(url, resource_url)
                resource_domain = urlparse(full_url).netloc
                                
                if domain not in resource_domain:
                    external_count += 1
                
            total += 1
        
        if total == 0:
            return -1
        
        percent = external_count / total * 100
        
        if percent < 17:
            return -1
        
        if percent >= 81:
            return 1
        
        return 0
    
    except:
        return 1
    
def classify_sfh(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        forms = soup.find_all("form")
        
        if len(forms) == 0:
            return -1
        
        for form in forms:
            action = form.get("action")
            if action is None or action == "" or action == "about:blank":
                return 1
        
        return -1 

    except:
        return 1
    
    
        
        
def classify_mail(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        for form in soup.find_all("form"):
            action = form.get("action").lower()
            if "mailto:" in action or "mail()" in action or "mail(" in action:
                return 1
        
        return -1
    
    except Exception as e:
        return 1
    
    

def classify_abnormal_url(url):
    try:
        parsed = urlparse(url)
        
        if not parsed.hostname:
            return 1

        return -1
    except:
        return 1

def classify_website_forwarding(url):
    try:
        response = requests.get(url)
        num_redirects = len(response.history)
        
        if num_redirects <= 1:
            return -1
        
        if num_redirects >= 4:
            return 1
        return 0
    except:
        return 1
    
def classify_status_bar(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        onmouseover_events = soup.find_all(attrs={"onmouseover": True})
        
        for event in onmouseover_events:            
            if 'window.status' in event['onmouseover'] or 'status' in event['onmouseover']:
                return 1  
            
        return -1  
    
    except:
        return 1
    

def check_right_click(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        right_click_events = soup.find_all(string=lambda text: text and 'event.button == 2' in text)
        
        if right_click_events:
            return 1
        
        return -1
    except:
        return 1

def classify_popup_window(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        popups = soup.find_all("script", string=lambda text: text and "window.open" in text)
        
        if popups:
            for popup in popups:
                popup_soup = BeautifulSoup(popup.string, "html.parser")
                input_fields = popup_soup.find_all(['input', 'textarea'])
                for field in input_fields:
                    if field.get('type') == 'text' or field.name == 'textarea':
                        return 1
        
        return -1
    except:
        return 1
    
def classify_iframe(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        
        iframes = soup.find_all("iframe")
        
        
        if iframes:
            for iframe in iframes:
                src = iframe.get("src")
                if src:
                    full_url = urljoin(url, src)
                    domain = urlparse(full_url).netloc
                    if domain != urlparse(url).netloc:
                        return 1
        
        return -1
    except:
        return 1

def classify_age_of_domain(domain):
    try:
        domain_info = whois.whois(domain)
        
        creation_date = domain_info.creation_date
        
        
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
                
        if creation_date:
            current_date = datetime.now()
            age = (current_date - creation_date).days / 365.25  # Convert days to years
            
            if age <= 1:
                return 1
            else:
                return -1
        else:
            return 1  
    except Exception as e:
        print(f"Error checking domain registration: {e}")
        return 1   
    
def classify_dns_record(url):
    try:
        domain = urlparse(url).netloc
        domain_info = whois.whois(domain)
        
        if domain_info:
            return -1
        
        return 1
    except:
        return 1

def classify_website_traffic(url):
    return 0 # Could not find a way to do this for free

def classify_page_rank(url):
    return 0 # Could not find a way to do this for free

def is_website_indexed(url):
    query = f"site:{url}"
    
    results = list(search(query, num_results=1))
    
    if results:
        return -1
    
    return 1


def classify_links_pointing_to_page(url):
    return 0 # Could not find a way to do this for free

def classify_stats_report(url):
    return 0 # Could not find a way to do this for free

def return_features(url):
    
    if validators.url(url):
        pass
    elif re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', url):
        url = "https://" + url
    
    try:
        response = requests.get(url)
        if response.status_code >= 200:
            return False
    except:
        return False
    
    
    
    features = []
    
    features.append(is_ip(url))
    features.append(is_long_url(url))
    features.append(is_short_url(url))
    features.append(has_at_symbol(url))
    features.append(has_redirecting_slash(url))
    features.append(has_prefix_suffix(url))
    features.append(has_subdomains(url))
    features.append(has_https(url))
    features.append(classify_domain(url))
    features.append(has_favicon(url))
    features.append(has_nonstd_port(url))
    features.append(has_https_domain_url(url))
    features.append(has_external_resources(url))
    features.append(check_anchors(url))
    features.append(check_links_in_tags(url))
    features.append(classify_sfh(url))
    features.append(classify_mail(url))
    features.append(classify_abnormal_url(url))
    features.append(classify_website_forwarding(url))
    features.append(classify_status_bar(url))
    features.append(check_right_click(url))
    features.append(classify_popup_window(url))
    features.append(classify_iframe(url))
    features.append(classify_age_of_domain(url))
    features.append(classify_dns_record(url))
    features.append(classify_website_traffic(url))
    features.append(classify_page_rank(url))
    features.append(is_website_indexed(url))
    features.append(classify_links_pointing_to_page(url))
    features.append(classify_stats_report(url))
    
    return [features]

