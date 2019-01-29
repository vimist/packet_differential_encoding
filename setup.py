from setuptools import setup


setup(
    name='packet-differential-encoding',
    version='0.0.1',
    author='Vimist',
    description=(
        'A stegonographic method of transmitting data between two hosts using '
        'the time delta between packets.'),
    install_requires=['scapy'],
    packages=['packet_differential_encoding'],
    entry_points={
        'console_scripts': [
            'diff-packets = packet_differential_encoding.__main__:main_cli_args'
        ]
    }
)
