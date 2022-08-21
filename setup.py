from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'qwota',
    version = '0.0.1',
    author = 'Henning Seljenes',
    author_email = 'henning.seljenes@gmail.com',
    license = 'MIT',
    description = 'Tool for checking OpenShift AppliedClusterQuotaResource',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = '<github url where the tool code will remain>',
    py_modules = ['qwota'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        qwota=qwota_cli:cli
    '''
)