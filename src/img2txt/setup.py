from setuptools import setup

package_name = 'img2txt'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Samuel Cooper',
    maintainer_email='samuel.j.cooper@outlook.com',
    description='Processes camera images, extracts Japanese text and publishes related information.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cam = img2txt.camera_data:main',
        ],
    },
)