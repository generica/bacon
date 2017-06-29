# bacon

> Brett's Automatic Configurator and Operating system Negotiator

A simple experiment for fun

## Installation

```sudo python3 setup.py install```

## Usage

```
usage: bacon [-h] [-v] [-t] [-f FILE]

 optional arguments:
   -h, --help            show this help message and exit
   -v, --verbose         Increase verbosity
   -t, --test            Test only, don't apply changes
   -f FILE, --file FILE  File to use for definitions
```

## File format

Changes are described in yaml format, and can be spread over multiple files if you prefer.

The schemas for resources are:

```yaml
uniqueResourceName: string
  type: file
  ensure: ['present', 'absent']   # Wanted state
  path: string                    # '/path/to/file'
  mode: string                    # '0644'
  user: string                    # 'nobody'
  group: string                   # 'nogroup'
  content: string                 # 'My content for the file'
  requires: string                # Any resource that should be installed first
  requires:
    - string
    - string                      # If multiple services are required
  notify: string                  # Any service resource that should be reloaded on change of this file
```

```yaml
uniqueResourceName: string
  type: package
  ensure: ['present', 'absent']   # Wanted state
  name: string                    # Package name
  requires: string                # Any resource that should be installed first
  requires:
    - string
    - string                      # If multiple services are required
```

```yaml
uniqueResourceName: string
  type: service
  manager: ['systemd']            # Which init program is used
  name: string                    # Initscript name
  ensure: ['running', 'stopped']  # Wanted state
  requires: string                # Any resource that should be installed first
  requires:
    - string
    - string                      # If multiple services are required
```

## Contributing

> My operating system isn't represented, what should I do to be able to install packages?

Easy!
* Edit ```bacon/modules/package.py```
* Add your OS/Linux release to **detect_release()**
* Add files to ```bacon/modules/YourOS/package.py```

They should have two functions:

```python3
def package_is_installed(package):
    ''' See if a package is installed or not '''
...
def perform_change(change):
    ''' Perform the change on the resource '''
```

See existing OSes for examples, and the format of the change request

> I don't use systemd, I use sysvinit!

Sorry! Easy fix though.
* Add a new module, ```bacon/modules/sysvinit/service.py```

It should have two functions (at least):

```python3
def service_is_running(service):
    ''' See if a service is running or not '''
...
def perform_change(service, ensure):
    ''' Perform the change on the resource '''
```

See systemd directory for examples, and the format of the change request

> I want to do more than just files, packages and services! What about managing users as well?

Easy!
* Add your new module, ```bacon/modules/user.py```

It should have two functions (at least):

```python3
def needs_change(change):
    ''' Detect if a change needs to occur or not '''
...
def perform_change(change):
    ''' Perform the change on the resource '''
```

See existing modules for the format of the change request
