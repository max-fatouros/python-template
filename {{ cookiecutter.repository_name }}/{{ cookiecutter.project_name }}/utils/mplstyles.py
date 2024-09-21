"""
https://matplotlib.org/stable/tutorials/introductory/customizing.html#defining-your-own-style
"""
from {{ cookiecutter.project_name }}.utils import paths

PAPER = [
    'seaborn-v0_8',
    paths.UTIL_DIR / 'paper.mplstyle',
]

POSTER = [
    PAPER,
    paths.UTIL_DIR / 'poster.mplstyle',
]
