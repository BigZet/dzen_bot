import setuptools

setuptools.setup(
    name="dzen_auto_author",
    version="1.0.0",
    description="Powerfull bot for authors in dzen.ru",
    url="https://github.com/BigZet/dzen_bot",
    packages=setuptools.find_packages(),
    python_requires='>=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    include_package_data=True,
    install_requires=[
       'selenium',
       'selenium-stealth'
    ]
)