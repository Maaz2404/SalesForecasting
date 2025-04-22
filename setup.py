from setuptools import find_packages, setup

HYPHEN_E_DOT = '-e .'  # Fix missing space

def get_requirements(file):
    with open(file, 'r') as f:
        requirements = f.readlines()
        requirements = [req.strip() for req in requirements]  # Remove \n safely
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
        
    return requirements

setup(
    name='salesforecasting',  # Fixed typo
    version='0.0.1',
    author='Maaz Ahmad',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')  # Correct parsing
)
