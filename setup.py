from setuptools import setup, find_packages

setup(
    name='cdbt',
    version='0.3.7',
    description='A CLI tool to manage dbt builds with state handling and manifest management',
    author='Craig Lathrop',
    author_email='development@coldborecapital.com',
    packages=find_packages(),
    install_requires=[
        'click',
        'pyperclip',
        'snowflake-connector-python[pandas]',
        'python-dotenv',
        'openai',
        'sqlfluff',
        'sqlfluff-templater-dbt',
        'wordninja'
    ],
    entry_points={
        'console_scripts': [
            'cdbt=cdbt.cmdline:cdbt',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8'
)
