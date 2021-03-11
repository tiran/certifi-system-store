from setuptools import setup
from setuptools.command.egg_info import egg_info


class alt_egg_info(egg_info):
    @property
    def name(self):
        return "certifi"

    def run(self):
        super().run()
        self.run_command("orig_egg_info")
        orig_ei_cmd = self.get_finalized_command("orig_egg_info")
        self.filelist.graft(orig_ei_cmd.egg_info)


setup(
    cmdclass={
        # "egg_info": alt_egg_info,
        # "orig_egg_info": egg_info,
    },
)
