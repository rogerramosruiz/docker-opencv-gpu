import subprocess
import re 

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
    return nvidia_smi('--query-gpu=gpu_name --format=csv,noheader').decode('utf-8').strip()


if __name__ == '__main__':
    print(get_graphic_card())