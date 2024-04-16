from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='socktalk',
    version='0.2.1',
    packages=find_packages(),
    project_urls={
        'Source': 'https://github.com/mdkmk/socktalk'
    },
    install_requires=[
        'annotated-types==0.6.0',
        'anyio==4.3.0',
        'certifi==2024.2.2',
        'distro==1.9.0',
        'exceptiongroup==1.2.0',
        'h11==0.14.0',
        'httpcore==1.0.5',
        'httpx==0.27.0',
        'idna==3.7',
        'openai==1.14.2',
        'pydantic==2.6.4',
        'pydantic_core==2.16.3',
        'PyQt5==5.15.10',
        'PyQt5-Qt5==5.15.2',
        'PyQt5-sip==12.13.0',
        'sniffio==1.3.1',
        'tqdm==4.66.2',
        'typing_extensions==4.11.0'
    ],
    entry_points={
        'console_scripts': [
            'socktalk=server_client.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    description='Socket-based AI chat server and multi-user chat client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='chat server, chat client, AI chatbot, chatGPT, OPENAI API, socket programming, select.select(),'
             ' multi-user chat, real-time communication, Python chat application'
)
