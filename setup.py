import json 
import os 

from setuptools import setup 
from setuptools import find_packages
from setuptools.command.build_py import build_py

from zipfile import ZipFile
class my_build_py(build_py): 
    """
    Example of including custom build step which creates a new .py file 
    """
    # Implemented with a run() method 
    def run(self) -> None: 

        with open(os.path.join('src','mypkg', 'foo.json'), 'r') as file: 
            contents = json.load(file)
        with open(os.path.join('src', 'mypkg', 'foo.py'), 'w') as file: 
            file.write(f"JSON = {contents!r}\n")
        zip_path = os.path.join('src','mypkg','bar.zip')
        try:
            extract_to = os.path.abspath(os.path.join('src', 'mypkg','unzipped'))
            os.makedirs(extract_to, exist_ok=True) 
            print(f"Current working directory: {os.getcwd()}".upper())  
            print(f'Attempting to unzip {zip_path} to {extract_to}'.upper())
            print(f"Contents of 'mypkg': {os.listdir(os.path.join('src','mypkg'))}".upper())
            with ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(extract_to)
            print(f"Unzipped contents to {extract_to}: {os.listdir(extract_to)}")
        except Exception as e: 
            print(os.listdir('.'))
            print(os.listdir('src','mypkg'))
            raise e
        super().run()
setup(
  name='mypkg',
  version='0.0.0',
  package_dir={"":"src"},
  packages=find_packages(where='src', exclude=('tests*', 'testing*')),
  cmdclass={'build_py':my_build_py}, 
  # include_package_data=True # includes anything in MANIFEST.in in final install state
  # This can be excessive if you need files in your build only and not your runtime.
  package_data={
      'mypkg':('*.json', 'subdir/*.json', '*.zip', 'unzipped/*'),
      # 'mypkg.subdir':('*.json',),
  }
 )