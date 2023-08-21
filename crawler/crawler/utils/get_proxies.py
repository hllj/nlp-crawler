import json

def get_proxies(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    proxy_list = []
    for item in data:
        scheme = 'http' if item['https'] == 'no' else 'https'
        ip = item['ip_address']
        port = item['port']
        proxy = f'{scheme}://{ip}:{port}'
        proxy_list.append(proxy)
    return proxy_list