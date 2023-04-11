# OpenCV with gpu in docker 

Compile OpenCV for a Nvidia GPU in a docker container

# Table of Contents

- [Clone repo](#clone-repo)
- [Compile](#compile)
  - [Set up](#set-up)
  - [Build image](#build-image)
- [Compiling errors in WSL](#compiling-errors-in-wsl)
  - [Increase WSL RAM limit](#increase-wsl-ram-limit)
  - [Compile single threaded](#compile-single-threaded)

## Clone repo
```
git clone https://github.com/rogerramosruiz/docker-opencv-gpu.git
cd docker-opencv-gpu
```

## Compile
### Set up
Run setup.py
Windows
```
python setup.py
```

Linux
```
python3 setup.py
```

A .env file will be created created with GPUs  compute capability and the recomended image, if the values are not filled correctly edit them.

for the compute capability visit https://developer.nvidia.com/cuda-gpus

for nvida image https://hub.docker.com/r/nvidia/cuda


### Build image
run docker compose

```bash
docker-compose up
```


## Compiling errors in WSL

If an error occurs whilest compiling and the machine O.S is windows using WSL, it might be that WSL is RAM limited.

Either increase WSL RAM limit or compile single threaded

### Increase WSL RAM limit

https://stackoverflow.com/questions/62405765/memory-allocation-to-docker-containers-after-moving-to-wsl-2-in-windows 

https://www.youtube.com/watch?v=h-jNlXN6qhI

More info on .wslconfig 

https://learn.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig

### Compile single threaded

Edit Dockerfile

Change this line   
```Dockerfile
RUN make -j$(nproc)
```
For
```Dockerfile
RUN make
```

⚠️ Note that compilation time will be slower.