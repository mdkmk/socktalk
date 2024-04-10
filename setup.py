from setuptools import setup, find_packages

setup(
    name='socktalk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'PyQt5==5.15.10',
        'openai==1.14.2'
    ],
    entry_points={
        'console_scripts': [
            'ai_server=server_client.start_server_with_ai_client:main',
            'chat_server=server_client.server:main',
            'chat_client=server_client.client:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
