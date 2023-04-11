import re 
import json
import subprocess
import urllib.request

def nvidia_smi(query = None):
    command = 'nvidia-smi'
    if query:
        command += f' {query}'
        command = command.split()
    return subprocess.check_output(command)

def cuda_version():
    data = nvidia_smi()
    data = data.decode('utf-8').strip()
    version = re.findall("CUDA Version: \d{1,2}\.\d{1,2}", data)[0]
    version = re.findall("\d{1,2}.\d{1,2}", version)[0]
    if len(version.split('.')) < 3:
        version += '.0'
    return version

def get_graphic_card():
    # nvidia-smi --query-gpu=gpu_name --format=csv,noheader
    gpu = ""
    not_allowed = ['NVIDIA', 'Laptop', 'GPU']
    data = nvidia_smi('--query-gpu=gpu_name --format=csv,noheader').decode('utf-8').strip()
    values = data.split(' ')
    for i in values:
        if i not in not_allowed:
            gpu += f'{i} '
    return gpu.strip()

def get_compute_capability(gpu):
    url = 'https://developer.nvidia.com/cuda-gpus'
    with urllib.request.urlopen(url) as r:
        data = r.read().decode('utf-8')
    start = data.find(gpu+'<')
    if start < 0:
        return start
    start += len('gpu')
    v = ''
    b = False
    for i in range(start, len(data)):
        if data[i] == '<':
            b = True
        if b:
            ch = ord(data[i])
            if ch >= ord('0') and ch <= ord('9') or data[i] == '.':
                v += data[i]
            if len(v) == 3:
                break
    return v


def get_docker_image(cudaVersion,distribution='ubuntu', type='devel'):
    # type runtime or devel
    url = f'https://hub.docker.com/v2/repositories/nvidia/cuda/tags/?page_size=25&page=1&name={cudaVersion}-cudnn'
    request = urllib.request.urlopen(url)
    image = ''

    data = json.load(request)
    images = []
    for i in data['results']:
        name = i['name']
        if distribution in name and type in name:
            images.append(name)
    maxv = -1
    for i in images:
        distversion = i.split('-')[-1]
        version = ''
        for j in distversion:
            if j >= '0' and j <= '9' or j == '.':
                version += j
        version = float(version)
        if version > maxv:
            maxv = version
            image = i
    return f'nvidia/cuda:{image}'

def main():
    gpu = get_graphic_card()
    print('GPU:', gpu)
    compute_cap = get_compute_capability(gpu)
    print('Compute capability:', compute_cap)
    cuda_v = cuda_version()
    image = get_docker_image(cuda_v, type='devel')
    print('Docker image:', image)
    with open('.env', 'w') as f:
        f.write(f'COMPUTE_CAPABILTY={compute_cap}\n')
        f.write(f'IMAGE={image}\n')

if __name__ == '__main__':
    main()