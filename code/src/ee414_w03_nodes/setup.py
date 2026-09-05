from setuptools import find_packages, setup

package_name = 'ee414_w03_nodes'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Anis Koubaa',
    maintainer_email='akoubaa@alfaisal.edu',
    description='EE 414 Week 3 — nodes that use the Week 3 interfaces.',
    license='TODO',
    entry_points={
        'console_scripts': [
            'wheel_publisher = ee414_w03_nodes.wheel_publisher:main',
            'odom_node       = ee414_w03_nodes.odom_node:main',
            'reset_client    = ee414_w03_nodes.reset_client:main',
            'driver          = ee414_w03_nodes.driver:main',
        ],
    },
)
