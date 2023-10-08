from setuptools import find_packages, setup

package_name = 'merge_arrays'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Kyle',
    maintainer_email='kylesha585@gmail.com',
    description='Merge and Sort Arrays',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'listener = merge_arrays.array_merger:main',
        ],
    },
)
