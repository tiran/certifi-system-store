import os
import shutil
import sys

if sys.version_info >= (3, 8):
    from importlib import metadata

    PackageNotFoundError = metadata.PackageNotFoundError

    def _get_distinfo(name):
        dist = metadata.distribution(name)
        egg_info = dist._path
        return dist.version, egg_info

    def _invalidate_caches():
        pass

else:
    import pkg_resources

    PackageNotFoundError = pkg_resources.DistributionNotFound

    def _get_distinfo(name):
        dist = pkg_resources.get_distribution(name)
        return dist.version, dist.egg_info

    def _invalidate_caches():
        pkg_resources.working_set.__init__()


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
    css_version, css_egg_info = _get_distinfo("certifi_system_store")
    try:
        certifi_version, certifi_egg_info = _get_distinfo("certifi")
    except PackageNotFoundError:
        pass
    else:
        if certifi_version == css_version:
            return False, css_egg_info, certifi_egg_info
        else:
            # blow away certifi's dist-info
            shutil.rmtree(certifi_egg_info)
            # reset current working set, so pkg_resources can pick up our hack
            _invalidate_caches()

    # certifi-system-store's dist-info
    abs_css_distinfodir = os.path.abspath(css_egg_info)
    css_basedir, css_distinfodir = os.path.split(abs_css_distinfodir)

    # certifi's dist-info in same base directory
    certifi_distinfodir = css_distinfodir.replace("certifi_system_store", "certifi")
    abs_certifi_distinfodir = os.path.join(css_basedir, certifi_distinfodir)

    # create symlink certifi.dist-info -> certifi_system_store.dist-info
    _relsymlink(target=abs_css_distinfodir, linkname=abs_certifi_distinfodir)

    # get dist info from refreshed working set
    css_version, css_egg_info = _get_distinfo("certifi_system_store")
    certifi_version, certifi_egg_info = _get_distinfo("certifi")

    # check that certifi dist-info is in same site-packages as certifi package
    certifi_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.abspath(certifi_egg_info)

    # compare with samefile instead of string comparison to avoid false
    # negatives caused by venv lib64 / lib symlinks
    if not os.path.samefile(os.path.dirname(certifi_dir), os.path.dirname(dist_dir)):
        raise RuntimeError(
            f"'{certifi_dir} and {dist_dir} have different parent directories."
        )

    # double check versions
    _verify_dist_info()

    return True, css_egg_info, certifi_egg_info


def _verify_dist_info():
    css_version, css_egg_info = _get_distinfo("certifi_system_store")
    try:
        certifi_version, certifi_egg_info = _get_distinfo("certifi")
    except PackageNotFoundError as e:
        raise RuntimeError(e)
    else:
        if certifi_version != css_version:
            raise RuntimeError(
                f"'certifi.dist-info' is not an alias to "
                f"'certifi_system_store.dist-info'. "
                f"Please execute '{sys.executable} -m certifi -v'."
            )

    return True
