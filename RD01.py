import requests
from bs4 import BeautifulSoup
import socket
import platform

def get_website_location(url):
    """Attempts to determine the location of a website."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        meta_location = soup.find("meta", attrs={"name": "location"})
        if meta_location:
            return f"Location (meta tag): {meta_location['content']}"

        try:
            hostname = url.split("//")[-1].split("/")[0]
            ip_address = socket.gethostbyname(hostname)

            addr_info_list = socket.getaddrinfo(hostname, 28)

            location_info = None
            for addr_info in addr_info_list:
                family, socktype, proto, canonname, sockaddr = addr_info
                if family == socket.AF_INET:
                    ip, port = sockaddr
                    try:
                        if platform.system() != "Windows":
                            host, aliaslist, addresslist = socket.getnameinfo((ip, port), socket.NI_NAMEREQUIRED)
                            location_info = f"{host} (IP: {ip})"
                        else:
                            location_info = f"IP: {ip} (Reverse lookup not fully available on Windows)"
                        break  # Stop after finding the first IPv4 address
                    except socket.gaierror as e:
                        location_info = f"Could not determine location from IP {ip}: {e}"
                        break

            if location_info:
                return f"Location (IP/getnameinfo): {location_info}"
            else:
                return f"Location (IP): Could not determine location from IP {ip_address}"

        except socket.gaierror as e:
            return f"Location: Could not resolve hostname to IP address: {e}"

    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    website_url = input("Enter the website URL (including http:// or https://): ")
    location = get_website_location(website_url)
    print(location)
