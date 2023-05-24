# Raspberry Pi 2 Linux Image
## Setup enviroment
In order to start generating Linux images with Yocto Projetc we must get a poki version. To achive this you must copy this command in the Linux terminal (debian based in this case):
```
sudo apt install gawk wget git diffstat unzip texinfo gcc build-essential chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev python3-subunit mesa-common-dev zstd liblz4-tool file locales
git clone git://git.yoctoproject.org/poky
cd poky
git checkout -t origin/langdale -b my-langdale
git pull
```
Then we must initialize the enviroment in a builf folder as:
```
source poky/oe-init-build-env build_dir
```
This should take you to the build_dir automatically. [Link to official documentation](https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html)

## Raspberry Pi Layer
This layer has must of the raspberry pi dependencies, even the python3 libs that allow you to control the offitial camera of Raspberry Pi. In order to include this layer into your projetc you must execute the following commands inside your build_dir directory.
```
git clone -b langdale https://github.com/agherzan/meta-raspberrypi.git
bitbake-layers add-layer meta-raspberrypi
```
To make sure that the layer is included you can look for the conf/bblayers.conf.

**NOTE: You must make sure (and this applies to all future layers you might want to add) that the layer is compatible with the poky version you are using, in this case _langdale_, otherwise you won't be able to generate the OS image.**

## meta-openembedded Layer
This layer is essential in most of the Yocto projects bacause it has lots of aplications and features those you might be interested in. To include this layer and the specific features for this project you must write the following commands:
```
git clone -b langdale https://github.com/openembedded/meta-openembedded.git
bitbake-layers add-layer meta-openembedded/meta-oe
bitbake-layers add-layer meta-openembedded/meta-python
bitbake-layers add-layer meta-openembedded/meta-networking
bitbake-layers add-layer meta-openembedded/meta-multimedia
```
## meta-tensorflow Layer
TensorFlow is an open source software library for high performance numerical
computation primarily used in machine learning. Its flexible architecture
allows easy deployment of computation across a variety of types of platforms
(CPUs, GPUs, TPUs), and a range of systems from single desktops to clusters
of servers to mobile and edge devices.
(https://www.tensorflow.org/)
It is highly recomended to checkout the documentation in [Link to official documentation](https://github.com/ribalda/meta-tensorflow) in order to understand the depedecies of this layer. In order to include this layer into your projetc you must execute the following commands inside your build_dir directory.
```
git clone https://github.com/ribalda/meta-tensorflow.git
git clone -b langdale git://git.yoctoproject.org/meta-java
bitbake-layers add-layer meta-tensorflow
```
## Create a custom layer
In this layer we setup the files that we want to be installed by default in the Linux image. First step is creating a example layer ussing the bitbake feature bitbake-layers cerate-layer meta-layername
```
bitbake-layers cerate-layer meta-layername
bitbake-layers add-layer meta-layername
```
Which you can find in this repository alongside the files that will be installed.

## local.conf prameters
This project is based on Raspberry Pi 2 hardware so we must setup the local.conf file with the features that we need. To achive this you must follow this steps, alongside the ondes described in [Link to official documentation](https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html).
- Select the machine by modifing the parameter: MACHINE ??= "raspberrypi2"
- Add this lines: GPU_MEM = "16" and IMAGE_FSTYPES = "tar.xz ext3 rpi-sdimg"
- Finally copy this features to be installed into the local.conf file:
```
IMAGE_INSTALL:append = " \
		 example \
		 python3-picamera \
		 git \
		 python3-pip \
		 python3-pygobject \
		 python3-paramiko \
                 vim \
                 openssh \
                 opencv \ 
                 ntp \
                 ntpdate \
                 picamera-libs \
                 v4l-utils \
                 usbutils \
		"
IMAGE_INSTALL:append = " tensorflow-lite"
DISTRO_FEATURES:append = " v4l2"
RPI_CAMERA = "1"
VIDEO_CAMERA = "1"
```
## Create the image
By using the command:
```
bitbake core-image-base
```
We use core-image-base because this build is a console-only image that fully supports the target device hardware [Link to the mount video](https://docs.yoctoproject.org/ref-manual/images.html), because it has the needed features to support a usb camera. 
The image should start building, this process migth take a few minutes based on your hardware.
After this process is finished look for your image in build_dir/tmp/deploy/images/raspberrypi2/core-image-base-raspberrypi2.rpi-sdimg.
The follow the steps shown in the video [Link to the mount video](https://youtu.be/zVLKPtGCtN4?t=230).

