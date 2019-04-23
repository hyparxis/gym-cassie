from setuptools import setup

REQUIRED_PACKAGES = ["gym", "numpy"]

setup(name='cassierl',
      version='0.2',
      description='Cassie reinforcement learning environment',
      author='Pedro Morais',
      author_email='autranemorais@gmail.com',
      license='MIT',
      packages=['gym_cassie'],
      install_requires=REQUIRED_PACKAGES
)
