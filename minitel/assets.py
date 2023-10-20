from absl import flags
import os.path


flags.DEFINE_string("assets_path", "minitel/assets", "Path to the assets directory")


def asset(filename):
    return os.path.join(flags.FLAGS.assets_path, filename)
