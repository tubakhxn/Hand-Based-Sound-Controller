"""audio_controller.py

Windows system audio control wrapper using pycaw. Provides a simple AudioController
class to get/set the master volume as a float in [0.0, 1.0].

If pycaw is not available or the OS is not Windows, it raises informative errors.
"""
import platform

IS_WINDOWS = platform.system() == 'Windows'

if IS_WINDOWS:
    try:
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        import ctypes
        from ctypes import POINTER, cast
        from comtypes import GUID
    except Exception as e:
        raise ImportError('pycaw or comtypes is required on Windows to control system volume. Install with: pip install pycaw comtypes') from e


class AudioController:
    def __init__(self):
        if not IS_WINDOWS:
            raise EnvironmentError('AudioController only supports Windows via pycaw')
        devices = AudioUtilities.GetSpeakers()
        # pycaw.utils.AudioDevice may already expose an EndpointVolume pointer
        # (see diagnostic output). Prefer that if available to avoid calling
        # Activate which some pycaw wrappers don't expose.
        if hasattr(devices, 'EndpointVolume'):
            self.volume = devices.EndpointVolume
        elif hasattr(devices, '_volume'):
            # internal attribute used by some pycaw versions
            self.volume = devices._volume
        else:
            # fallback to COM Activate() as in many examples
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        # get volume range for debug if needed
        # min, max, step = self.volume.GetVolumeRange()

    def get_volume(self) -> float:
        """Return current master volume as float 0.0 - 1.0."""
        # GetMasterVolumeLevelScalar returns 0.0-1.0
        return float(self.volume.GetMasterVolumeLevelScalar())

    def set_volume(self, value: float):
        """Set master volume. value: float in 0.0 - 1.0."""
        v = min(max(value, 0.0), 1.0)
        self.volume.SetMasterVolumeLevelScalar(v, None)
