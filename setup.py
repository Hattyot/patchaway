import setuptools

setuptools.setup(
    name="patchaway",
    version="0.0.1",
    author="Hattyot",
    description="Patch python builtin methods",
    url="https://github.com/Hattyot/patchaway",
    project_urls={
        "Bug Tracker": "https://github.com/Hattyot/patchaway/issues"
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
)