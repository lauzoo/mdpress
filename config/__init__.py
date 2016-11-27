# coding: UTF-8
import os


def load_config(mode=os.environ.get('MODE')):
    """Load config."""
    mode = mode.upper() if mode else mode
    try:
        if mode == 'DEVELOPMENT':
            from .development import DevelopmentConfig
            return DevelopmentConfig
        elif mode == 'TESTING':
            from .testing import TestingConfig
            return TestingConfig
        elif mode == 'DOCKER':
            from .docker import DockerConfig
            return DockerConfig
        else:
            from .production import ProductionConfig
            return ProductionConfig
    except ImportError:
        from .default import Config
        return Config
