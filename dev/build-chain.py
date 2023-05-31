import subprocess
import sys
from distutils.dir_util import copy_tree


chains = {
    "nodejs-minimal": ["base", "nodejs-minimal"],
    "python-minimal": ["base", "python-minimal"],
    "python-pyspark-jigsaw": ["base", "python-minimal", "spark"],
    "vscode": ["base", "python-minimal", "vscode"],
    "vscode-pyspark-jigsaw": ["base", "python-minimal", "python-pyspark-jigsaw", "vscode"],
    "vscode-minimal": ["base", "python-minimal", "vscode"],
    "vscode-nodejs": ["base", "nodejs-minimal", "vscode"]
}

chain = chains[sys.argv[1]]

GPU = False
if len(sys.argv) == 3:
    if sys.argv[2] == "gpu":
        GPU = True

for i, image in enumerate(chain):

    if image == "base":
        copy_tree("scripts", "base/scripts")
        if GPU:
            previous_image = "nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04"
        else:
            previous_image = "ubuntu:22.04"
    else:
        previous_image = chain[i-1]

    if GPU:
        device_suffix = "-gpu"
    else:
        device_suffix = ""

    cmd = ["docker", "build", image, "-t", image,
           "--build-arg", f"BASE_IMAGE={previous_image}",
           "--build-arg", f"DEVICE_SUFFIX={device_suffix}"]
    print(" ".join(cmd))
    subprocess.run(cmd)
