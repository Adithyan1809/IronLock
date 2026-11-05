from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """This function will return the list of requirements"""
    
    requirement_lst:List[str]=[]
    try:
        with open("requirements.txt") as file:
            #Read Lines fro the file
            lines = file.readlines()
            #Process each line
            for line in lines:
                requirement=line.strip()
                #ignore empty lines and comments and -e .
                if requirement and not requirement.startswith("#") and not requirement.startswith("-e"):
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists in the project directory.")
        
    return requirement_lst

setup(
    name="IronLoack",
    version="0.1",
    author="Adithyan",
    author_email="adithyan18092005@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
