import re
import logging
import subprocess
import multiprocessing
import threading

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def start_tunnel(queue):
    command = ['python3', '-m', 'pymobiledevice3', 'lockdown', 'start-tunnel']

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    logging.info("Tunnel started")

    rsd_pattern = re.compile(r"--rsd (\S+) (\d+)")
    address, port = None, None

    while True:
        output = process.stdout.readline().strip()
        if output:
            logging.info(output)

        match = rsd_pattern.search(output)
        if match:
            address, port = match.group(1), int(match.group(2))
            queue.put((address, port))
            logging.info(f"RSD Address: {address}, RSD Port: {port}")
            break

    process.wait()

def simulate_location(address, port):
    command = ['python3', '-m', 'pymobiledevice3', 'developer', 'dvt', 'simulate-location', 'play', 'track.gpx', '--rsd', address, str(port)]

    process = subprocess.Popen(
        command,
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        text=True
    )

    logging.info(f"Simulating location with RSD {address}:{port}")

    process.wait()

def tunnel():
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=start_tunnel, args=(queue,))
    process.start()
    
    try:
        result = queue.get(timeout=20)
        if result is None:
            raise RuntimeError("❌ 无法建立隧道连接")
        address, port = result
        
        location_thread = threading.Thread(target=simulate_location, args=(address, port))
        location_thread.start()
        
        return process, address, port, location_thread
    except Exception as e:
        logging.error(f"❌ 隧道建立失败: {e}")
        process.terminate()
        process.join(timeout=2)
        if process.is_alive():
            process.kill()

    return None, None, None, None

if __name__ == "__main__":
    process, address, port, location_thread = tunnel()
    if address and port:
        print(f"RSD Address: {address}, RSD Port: {port}....")
        location_thread.join()