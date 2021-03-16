import os
import shutil
from setuptools import setup

cmdclass = {}

try:
    from wheel.bdist_wheel import bdist_wheel, wheel_version
except ImportError:
    pass
else:

    class custom_bdist_wheel(bdist_wheel):
        def add_hack(self, css_distinfo):
            if not css_distinfo.endswith(".dist-info"):
                raise ValueError(css_distinfo)
            directory, distinfo = os.path.split(css_distinfo)
            certifi_distinfo = os.path.join(
                directory, distinfo.replace("certifi_system_store", "certifi")
            )
            if os.path.isdir(certifi_distinfo):
                shutil.rmtree(certifi_distinfo)
            shutil.copytree(css_distinfo, certifi_distinfo)

            # _relsymlink(distinfo_path, certifi_distinfo)
            # print(distinfo_path, certifi_distinfo)
            # raise ValueError(egginfo_path, distinfo_path)

        def write_wheelfile(
            self, wheelfile_base, generator="bdist_wheel (" + wheel_version + ")"
        ):
            super().write_wheelfile(wheelfile_base, generator)
            self.add_hack(wheelfile_base)

    cmdclass["bdist_wheel"] = custom_bdist_wheel


setup(cmdclass=cmdclass)
