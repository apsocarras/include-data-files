## Including resources in packages 

https://www.youtube.com/watch?v=bfyIrX4_yL8&t=830s

Created __init__.py, main.py, venv, 

```bash 
python setup.py sdist bdist_wheel
```
Creates wheel 
Creates source distribution

NOTE: Using setup.py like this directly is [deprecated](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html). Use another tool to build your packages (e.g. [`uv build`](https://docs.astral.sh/uv/concepts/projects/#building-projects))

### Building a package 

#### Wheels 

.whls are zip files of installed state. 

```bash 
unzip -l *.whl

Archive:  include_data_files-0.1.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  10-14-2024 11:44   main.py
      197  10-14-2024 11:48   include_data_files-0.1.0.dist-info/METADATA
       91  10-14-2024 11:48   include_data_files-0.1.0.dist-info/WHEEL
        5  10-14-2024 11:48   include_data_files-0.1.0.dist-info/top_level.txt
      401  10-14-2024 11:48   include_data_files-0.1.0.dist-info/RECORD
---------                     -------
      694                     5 files
```

#### Tarballs (Source Distribution)

.tar files are binary file commonly used for backups and software distribution. 
Source distributions include the files you need to re-create the final installed state of the package. 

```bash
tar --list -f include_data_files-0.1.0.tar.gz 

include_data_files-0.1.0/
include_data_files-0.1.0/PKG-INFO
include_data_files-0.1.0/README.md
include_data_files-0.1.0/include_data_files.egg-info/
include_data_files-0.1.0/include_data_files.egg-info/PKG-INFO
include_data_files-0.1.0/include_data_files.egg-info/SOURCES.txt
include_data_files-0.1.0/include_data_files.egg-info/dependency_links.txt
include_data_files-0.1.0/include_data_files.egg-info/requires.txt
include_data_files-0.1.0/include_data_files.egg-info/top_level.txt
include_data_files-0.1.0/main.py
include_data_files-0.1.0/pyproject.toml
include_data_files-0.1.0/setup.cfg
include_data_files-0.1.0/setup.py
```

Remove the distribution. 

rm -rf dist


```bash 
rm -rf dist build *.egg-info mypkg/foo.py
python setup.py sdist bdist_wheel 
unzip -l dist/*.whl && tar --list -f dist/*.tar.gz
```

### 1. `MANIFEST.in` and `include_package_data=true` 

Main option here is `recursive-include` with the directory and then a glob

```MANIFEST.in
recursive-include mypkg *.json 
```
On its own this includes the .json file in your source distribution. This can be useful if as part of your package distribution you want to create some additional python files on setup. 
* NOTE: Don't include any *outputs* in your source distribution (it's supposed to be the *source*). 
* When you run `setup.py sdist` it will create the output file and thus include the output in your package directory. Repeated invocations of `setup.py bdist_wheel` will then pick up any built files in your source dist. 

You'll notice that the output `foo.py` is included in the wheel, but not `foo.json`. 

```bash 
Archive:  dist/mypkg-0.0.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  10-14-2024 11:44   mypkg/__init__.py
       10  10-14-2024 12:42   mypkg/foo.py
        0  10-14-2024 11:44   mypkg/main.py
       50  10-14-2024 12:42   mypkg-0.0.0.dist-info/METADATA
       91  10-14-2024 12:42   mypkg-0.0.0.dist-info/WHEEL
        6  10-14-2024 12:42   mypkg-0.0.0.dist-info/top_level.txt
      492  10-14-2024 12:42   mypkg-0.0.0.dist-info/RECORD
---------                     -------
      649                     7 files
```

To also include `foo.json` in your installed state, add `include_package_data=True` in your setup.py file's setup method. 


### 2. `MANIFEST.in` and `package_data=<dict>` 

Use `MANIFEST.in` just for your source dist and then package_data for your wheel distribution, e.g. if you wanted to include a license in the source but not the wheel:

```MANIFEST.in
include LICENSE 
```

```python 
## setup.py 
setup(
  name='mypkg',
  version='0.0.0',
  packages=find_packages(exclude=('tests*', 'testing*')),
  cmdclass={'build_py':my_build_py}, 
  package_data={
      'mypkg':('*.json', 'subdir/*.json'),
      # 'mypkg.subdir':('*.json',),
  }
 )
```
