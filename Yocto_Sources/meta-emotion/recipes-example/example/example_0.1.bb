SUMMARY = "bitbake-layers recipe"
DESCRIPTION = "Recipe created by bitbake-layers"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"
SRC_URI += "file://EmotionDetectionLite.py \ 
	    file://dataset_prepare.py \ 
	    file://haarcascade_frontalface_default.xml \ 
	    file://model.tflite \
	    file://EmotionDetectionLiteRasp.py \
	    file://webcamtest.py \
	   "
DEPENDS = "python3-paramiko"

S = "${WORKDIR}"

do_install() {
	install -d ${D}${bindir}
	install -m 0755 EmotionDetectionLite.py ${D}${bindir}
	install -m 0755 dataset_prepare.py ${D}${bindir}
	install -m 0755 haarcascade_frontalface_default.xml ${D}${bindir}
	install -m 0755 model.tflite ${D}${bindir}
	install -m 0755 EmotionDetectionLiteRasp.py ${D}${bindir}
	install -m 0755 webcamtest.py ${D}${bindir}
}


