import os
import sys
from pathlib import Path
from typing import Union, IO, Optional


try:
    import curses
except ImportError:
    curses = None  # Compiled w/o curses

from httpie.compat import is_windows
from httpie.config import DEFAULT_CONFIG_DIR, Config, ConfigFileError

from httpie.utils import repr_dict


# use this to manage all things environment related 
class Environment:
    """
    Information about the execution context
    (standard streams, config directory, etc).

    By default, it represents the actual environment.
    All of the attributes can be overwritten though, which
    is used by the test suite to simulate various scenarios.

    """
    is_windows: bool = is_windows
    config_dir: Path = DEFAULT_CONFIG_DIR
    stdin: Optional[IO] = sys.stdin  
    stdin_isatty: bool = stdin.isatty() if stdin else False
    stdin_encoding: str = None
    stdout: IO = sys.stdout
    stdout_isatty: bool = stdout.isatty()
    stdout_encoding: str = None
    stderr: IO = sys.stderr
    stderr_isatty: bool = stderr.isatty()
    colors = 256
    program_name: str = 'http'

    def __init__(self, **kwargs):
        """
        Use keyword arguments to overwrite
        any of the class attributes for this instance.
        """
        # making sure all the keyword args are actually attributes of this class 
        assert all(hasattr(type(self), attr) for attr in kwargs.keys())
        self.__dict__.update(**kwargs) # easy way to update all attributes

        # Keyword arguments > stream.encoding > default utf8
        if self.stdin and self.stdin_encoding is None:
            self.stdin_encoding = getattr(
                self.stdin, 'encoding', None) or 'utf8'
        if self.stdout_encoding is None: 
            actual_stdout = self.stdout
            self.stdout_encoding = getattr(
                actual_stdout, 'encoding', None) or 'utf8'
    
    def __str__(self):
        defaults = dict(type(self).__dict__)
        actual = dict(defaults)
        actual.update(self.__dict__)
        actual['config'] = self.config
        return repr_dict({
            key: value 
            for key, value in actual.items()
            if not key.startswith('_')
        })

    def __repr__(self): 
        return f'<{type(self).__name__} {self}>'

    _config = None # this is a cache for config 

    # core part of Environment 
    # Support loading config from the config file directory https://httpie.org/doc#config-file-directory
    @property 
    def config(self) -> Config:
        config = self._config 
        if not config:
            self._config = config = Config(directory=self.config_dir)
            if not config.is_new():
                try:
                    config.load()
                except ConfigFileError as e: 
                    self.log_error(e, level='warning')
    
    def log_error(self, msg, level='error'):
        assert level in ['error', 'warning']
        self.stderr.write(f'\n{self.program_name}: {level}: {msg}\n\n')
