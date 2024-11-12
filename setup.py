from setuptools import setup, find_packages

setup(
    name="cuda_render",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cffi>=1.17.1",
    ],
    author="Beltran offerrall",
    author_email="offerrallzombies@gmail.com",
    description="A minimal OpenGL renderer for CUDA buffers",
    python_requires=">=3.7",
)
