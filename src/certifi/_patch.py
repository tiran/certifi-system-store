import os
import shutil
import sys
import pkg_resources


def _relsymlink(target, linkname):
    """ln -rs target linkname"""
    linkname_dir, linkname_file = os.path.split(linkname)
    rel_target = os.path.relpath(target, linkname_dir)
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    dir_fd = os.open(linkname_dir, flags)
    try:
        os.symlink(rel_target, linkname_file, dir_fd=dir_fd)
    except OSError as e:
        # modify error text to include common base directory
        e.strerror = f"{e.strerror} at {linkname_dir}"
        raise
    finally:
        os.close(dir_fd)


def _patch_dist_info():
    # distribution object for the canonical project name
    css_dist = pkg_resources.get_distribution("certifi_system_store")
    try:
        certifi_dist = pkg_resources.get_distribution("certifi")
    except pkg_resources.DistributionNotFound:
        pass
    else:
        if os.path.samefile(css_dist.egg_info, certifi_dist.egg_info):
            return False, css_dist.egg_info, certifi_dist.egg_info
        else:
            # blow away certifi's dist-info
            shutil.rmtree(certifi_dist.egg_info)
            # reset current working set, so pkg_resources can pick up our hack
            pkg_resources.working_set.__init__()

    # certifi-system-store's dist-info
    abs_css_distinfodir = os.path.abspath(css_dist.egg_info)
    css_basedir, css_distinfodir = os.path.split(abs_css_distinfodir)

    # certifi's dist-info in same base directory
    certifi_distinfodir = css_distinfodir.replace("certifi_system_store", "certifi")
    abs_certifi_distinfodir = os.path.join(css_basedir, certifi_distinfodir)

    # create symlink certifi.dist-info -> certifi_system_store.dist-info
    _relsymlink(target=abs_css_distinfodir, linkname=abs_certifi_distinfodir)

    # get dist info from refreshed working set
    css_dist = pkg_resources.get_distribution("certifi_system_store")
    certifi_dist = pkg_resources.get_distribution("certifi")

    # check that certifi dist-info is in same site-packages as certifi package
    certifi_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.abspath(certifi_dist.egg_info)

    if os.path.dirname(certifi_dir) != os.path.dirname(dist_dir):
        raise RuntimeError(
            f"'{certifi_dir} and {dist_dir} have different parent directories."
        )

    # double check versions
    _verify_dist_info()

    return True, css_dist.egg_info, certifi_dist.egg_info


def _verify_dist_info():
    css_dist = pkg_resources.get_distribution("certifi_system_store")
    try:
        certifi_dist = pkg_resources.get_distribution("certifi")
    except pkg_resources.DistributionNotFound as e:
        raise RuntimeError(e)
    else:
        if certifi_dist.version != css_dist.version:
            raise RuntimeError(
                f"'certifi.dist-info' is not an alias to "
                f"'certifi_system_store.dist-info'. "
                f"Please execute '{sys.executable} -m certifi -v'."
            )

    return True
