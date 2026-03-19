#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    BlobFixupCtx,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.tools import (
    llvm_objdump_path,
)
from extract_utils.utils import (
    run_cmd,
)

namespace_imports = [
    'hardware/qcom-caf/sm8750',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.qti.diaghal-V1-ndk',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.wifidisplaysession_aidl-V1-ndk',
        'vendor.qti.ims.uceaidlservice-V1-ndk',
        'vendor.qti.ImsRtpService-V1-ndk',
        'vendor.qti.qccsyshal_aidl-V1-ndk',
        'vendor.qti.qccvndhal_aidl-V1-ndk',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    (
        'odm/etc/camera/enhance_motiontuning.xml',
        'odm/etc/camera/motiontuning.xml',
        'odm/etc/camera/snsc_bokeh_motiontuning.xml',
        'odm/etc/camera/snsc_enhance_motiontuning.xml',
        'odm/etc/camera/snsc_motiontuning.xml',
        'odm/etc/camera/snsc_noface_motiontuning.xml'
    ): blob_fixup()
        .regex_replace(
            'xml=version',
            'xml version'
        ),
    (
        'odm/lib64/libaudioroute_ext.so',
        'vendor/lib64/libagm.so',
        'vendor/lib64/libar-pal.so',
        'vendor/lib64/libmcs.so',
        'vendor/lib64/libmikaraoke.so',
        'vendor/lib64/libtiantongpal.so',
    ): blob_fixup()
        .replace_needed(
            'libaudioroute.so',
            'libaudioroute_annibale.so'
        ),
    (
        'odm/bin/hw/vendor.xiaomi.hw.touchfeature-service',
        'odm/lib64/hw/displayfeature.default.so',
        'odm/lib64/libadaptivehdr.so',
        'odm/lib64/libcolortempmode.so',
        'odm/lib64/libdither.so',
        'odm/lib64/libflatmode.so',
        'odm/lib64/libhistprocess.so',
        'odm/lib64/libmiBrightness.so',
        'odm/lib64/libmiSensorCtrl.so',
        'odm/lib64/libpaperMode.so',
        'odm/lib64/librhytheyecare.so',
        'odm/lib64/libsdr2hdr.so',
        'odm/lib64/libsre.so',
        'odm/lib64/libtruetone.so',
        'odm/lib64/libvideomode.so',
        'vendor/lib64/libgnss.so'
    ): blob_fixup()
        .replace_needed(
            'android.hardware.sensors-V2-ndk.so',
            'android.hardware.sensors-V3-ndk.so',
        ),
    (
        'odm/bin/hw/android.hardware.security.keymint-service.strongbox-nxp',
        'odm/lib64/libjc_keymint-nxp.so',
        'odm/lib64/libjc_keymint_transport_nxp.so',
        'odm/lib64/libkeymint_empty-nxp.so',
        'odm/lib64/libkeymint_empty-thales.so',
        'vendor/bin/hw/android.hardware.security.keymint-service-qti',
        'vendor/lib64/libqtikeymint.so',
    ): blob_fixup()
        .replace_needed(
            'android.hardware.security.keymint-V3-ndk.so',
            'android.hardware.security.keymint-V3-ndk_prebuilt.so'
        )
        .replace_needed(
            'libcppbor_external.so',
            'libcppbor_annibale.so'
        ),
    'odm/bin/hw/vendor.xiaomi.sensor.citsensorservice.aidl': blob_fixup()
        .replace_needed(
            'android.hardware.graphics.common-V5-ndk.so',
            'android.hardware.graphics.common-V6-ndk.so'
        )
        .replace_needed(
            'android.hardware.sensors-V2-ndk.so',
            'android.hardware.sensors-V3-ndk.so'
        ),
    (
        'vendor/etc/media_codecs_sun.xml',
        'vendor/etc/media_codecs_sun_vendor_without_dvenc.xml',
    ): blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|google_video|vendor_audio).*\n', ''),
    (
        'odm/lib64/camera/components/com.qti.node.dewarp.so',
        'odm/lib64/hw/com.qti.chi.override.so',
        'odm/lib64/libcamximageformatutils.so',
        'odm/lib64/libchifeature2.so',
        'odm/lib64/vendor.qti.hardware.camera.offlinecamera-service-impl.so',
        'vendor/lib64/libqvrservice.so'
    ): blob_fixup()
        .replace_needed(
            'android.hardware.graphics.allocator-V1-ndk.so',
            'android.hardware.graphics.allocator-V2-ndk.so'
        ),
    'odm/lib64/hw/camera.qcom.so': blob_fixup()
        .replace_needed(
            'android.hardware.sensors-V2-ndk.so',
            'android.hardware.sensors-V3-ndk.so'
        ),
    (
        'odm/lib64/com.qti.feature2.qcfa.so',
        'odm/lib64/libmicamera_aidl_device.so',
        'odm/lib64/com.qti.feature2.swmf.so',
        'odm/lib64/com.qti.feature2.hdr.so',
        'odm/lib64/com.qti.feature2.derivedoffline.so',
        'odm/lib64/com.qti.feature2.gs.sm8750.so',
        'odm/lib64/com.qualcomm.mcx.policy.mfl.so',
        'odm/lib64/com.qti.feature2.anchorsync.so',
        'odm/lib64/com.qti.feature2.metadataserializer.so',
        'odm/lib64/com.qti.feature2.generic.sm8750.so',
        'odm/lib64/com.qualcomm.qti.mcx.usecase.extension.so',
        'odm/lib64/com.qti.feature2.afbrckt.so',
        'odm/lib64/libchifeature2.so',
        'odm/lib64/com.qti.feature2.rtmcx.so',
        'odm/lib64/com.qti.feature2.frc.so',
        'odm/lib64/com.qti.feature2.mcreprocrt.so',
        'odm/lib64/com.qti.feature2.realtimeserializer.so',
        'odm/lib64/com.qti.feature2.raw2yuvhdr.so',
        'odm/lib64/com.qti.feature2.statsregeneration.so',
        'odm/lib64/com.qti.feature2.demux.so',
        'odm/lib64/com.qti.feature2.mux.so',
        'odm/lib64/com.qti.feature2.rawhdr.so',
        'odm/lib64/com.qti.feature2.generic.so',
        'odm/lib64/com.qti.feature2.ml.so',
        'odm/lib64/com.qualcomm.mcx.policy.sfl.so',
        'odm/lib64/com.qti.feature2.serializer.so',
        'odm/lib64/com.qti.feature2.rtmcx.sm8750.so',
        'odm/lib64/com.qti.feature2.rt.so',
        'odm/lib64/libcamxsettingsmanager.so',
        'odm/lib64/com.qti.feature2.stub.so',
        'odm/lib64/hw/com.qti.chi.override.so',
        'odm/lib64/hw/com.qti.chi.offline.so',
        'odm/lib64/com.qti.feature2.rtpostproc.so',
        'odm/lib64/com.qti.feature2.mfsr.sm8750.so',
        'odm/lib64/libmicamera_adapter.so',
        'odm/lib64/com.qti.feature2.offlinestatsregeneration.so',
        'odm/lib64/libcamxcommonutils.so',
        'odm/lib64/com.qti.feature2.mfsr.so',
        'odm/lib64/com.qti.feature2.rtpostproc.sm8750.so',
        'odm/lib64/com.qti.feature2.memcpy.so',
        'odm/lib64/libmicamera_hal_core.so',
        'odm/lib64/com.qti.feature2.mcreprocrt.sm8750.so',
        'odm/lib64/com.qti.feature2.fusion.so'
    ): blob_fixup()
        .binary_regex_replace(b'ro.build.product', b'ro.vendor.camera'),
    'vendor/lib64/libcamera2ndk_vendor.so': blob_fixup()
        .replace_needed(
            'android.frameworks.cameraservice.device-V2-ndk',
            'android.frameworks.cameraservice.device-V3-ndk'
        )
        .replace_needed(
            'android.frameworks.cameraservice.service-V2-ndk',
            'android.frameworks.cameraservice.service-V3-ndk'
        ),
    'vendor/lib64/camera.device-external-impl.so': blob_fixup()
        .replace_needed(
            'android.hardware.graphics.common-V5-ndk',
            'android.hardware.graphics.common-V6-ndk'
        ),
    'vendor/lib64/libcameraopt.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    (
        'odm/lib64/libAncHumanPreviewBokeh.so',
        'odm/lib64/libMiEmojiEffect.so',
        'odm/lib64/libMiPhotoFilter.so',
        'odm/lib64/libMiVideoFilter.so',
        'odm/lib64/libTrueSight.so',
        'odm/lib64/libarcsoft_beautyshot.so',
        'odm/lib64/libwa_widelens_undistort.so'
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_isSupported'),
    (
        'odm/lib64/hw/fingerprint.qcom_us.default.so',
        'odm/lib64/libqc_hal.so'
    ): blob_fixup()
        .replace_needed(
            'android.hardware.biometrics.fingerprint-V5-ndk.so',
            'android.hardware.biometrics.fingerprint-V4-ndk.so'
        ),
    'odm/etc/init/vendor.xiaomi.hw.touchfeature-service.rc': blob_fixup()
        .regex_replace(r'service touch-kmsg-init-sh\b[\s\S]*?\n(?=\S|$)', ''),
    'vendor/etc/init/audiohalservice_qti.rc': blob_fixup()
        .regex_replace(r'service set_diag_state[\s\S]*?\n(?=\S|$)', ''),
    (
        'vendor/bin/wfdhdcphalservice',
        'vendor/bin/wfdvndservice'
    ): blob_fixup()
        .replace_needed(
            'libwfdhdcpservice_proprietary.so',
            'libwfdhdcpservice_annibale.so'
        ),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .replace_needed(
            'android.hardware.graphics.common-V5-ndk.so',
            'android.hardware.graphics.common-V6-ndk.so'
        ),
    'vendor/lib64/libwfdmmsrc_proprietary.so': blob_fixup()
        .replace_needed(
            'android.media.audio.common.types-V2-ndk.so',
            'android.media.audio.common.types-V3-ndk.so'
        ),
}  # fmt: skip

module = ExtractUtilsModule(
    'annibale',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
