from setuptools import find_packages, setup

package_name = 'ai_server'

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
    maintainer='mk',
    maintainer_email='mk@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ai_server = ai_server.ai_main:main',
            'ai_server2 = ai_server.ai_main_2:main',
            'display_result = ai_server.display_result:main',
            'result_publisher = ai_server.result_publisher:main',
            'test = ai_server.test1:main',
        ],
    },
)
