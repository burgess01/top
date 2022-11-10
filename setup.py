from setuptools import setup, find_packages


setup(
    name="pytop",
    version="1.0",
    license="MIT",
    author="Katherine Burgess",
    author_email="20burgessk@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/burgess01/top",
    keywords="top",
    install_requires=[
        "schedule",
        "psutil",
        "datetime",
        "hurry.filesize",
        "time",
        "sys",
        "platform",
    ],
)
