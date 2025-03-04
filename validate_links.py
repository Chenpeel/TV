import requests
import git
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 获取环境变量
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
TIMEOUT = int(os.getenv('TIMEOUT', 5))  # 设置合理的超时时间
PREFIX_RANGE = os.getenv('PREFIX_RANGE', '20-3f')
MAX_WORKERS = int(os.getenv('MAX_WORKERS', 10))  # 设置线程池的最大工作线程数

def validate_link(url):
    for _ in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            continue
    return False

def update_links(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(validate_link, line.strip()): line for line in lines if line.startswith('http')}
        for future in as_completed(future_to_url):
            line = future_to_url[future]
            if future.result():
                updated_lines.append(line)
            else:
                print(f"Link {line.strip()} is invalid.")

    # Append non-HTTP lines
    updated_lines.extend([line for line in lines if not line.startswith('http')])

    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

if __name__ == "__main__":
    repo = git.Repo('.')
    repo.git.pull()

    m3u_files = ['CCTV.m3u', 'IPTV-f-v6.m3u', 'TV-IPV4.m3u', 'CNTV1.m3u', 'CNTV2.m3u', 'CNTV3.m3u', '4k.m3u', '4k.txt']
    for m3u_file in m3u_files:
        update_links(m3u_file)

    repo.git.add(update=True)
    repo.index.commit("Update M3U links")
    origin = repo.remote(name='origin')
    origin.push()
