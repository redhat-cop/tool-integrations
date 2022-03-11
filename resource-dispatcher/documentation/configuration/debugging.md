# Debugging / Profiling

There are a few profiling tools built in to help identify any leaks when developing this application or any task configurations for it. The interval at which each type of profile should be run is configurable. Multiple or all debugging options can be enabled at the same time.

## Memory Profiling

Memory profiling can be used to observe if anything is consuming increasing amounts of memory over time. It configured using

```yaml
debugging:
  memory_profile:
    interval: 5 minutes
```

which periodically outputs a profile of the objects held in memory (in the main process), like so:

```
### DEBUG: BEGIN MEMORY PROFILE ###

refs:
1080	<class 'dict'> {4386728040: <weakref at 0x104c36db0; to 'type' at 0x105782868 (type)>, 4386743384: <weakref at 0x10
790	<class 'dict'> {'application/javascript': ['.js', '.mjs'], 'application/json': ['.json'], 'application/manifest+jso
393	<class 'dict'> {'sys': <module 'sys' (built-in)>, 'builtins': <module 'builtins' (built-in)>, '_frozen_importlib':
299	<class 'dict'> {'__name__': 'os', '__doc__': "OS routines for NT or Posix depending on what system we're on.\n\nThi
280	<class 'list'> ['A. HISTORY OF THE SOFTWARE', '==========================', '', 'Python was created in the early 19
269	<class 'list'> ['altsep', 'curdir', 'pardir', 'sep', 'pathsep', 'linesep', 'defpath', 'name', 'path', 'devnull', 'S
260	<class 'functools._lru_cache_wrapper'> <functools._lru_cache_wrapper object at 0x105348280>
260	<class 'functools._lru_cache_wrapper'> <functools._lru_cache_wrapper object at 0x1053489d0>
260	<class 'functools._lru_cache_wrapper'> <functools._lru_cache_wrapper object at 0x10534b280>
256	<class 'dict'> {(typing.Iterable, <class 'str'>): <functools._lru_list_elem object at 0x1054b26b0>, (typing.Mapping

bytes:
65704	 <_io.BufferedWriter name='<stdout>'>
65704	 <_io.BufferedWriter name='<stderr>'>
65704	 <_io.BufferedReader name=7>
36960	 {'application/javascript': ['.js', '.mjs'], 'application/json': ['.json'], 'application/manifest+jso
18520	 {4386728040: <weakref at 0x104c36db0; to 'type' at 0x105782868 (type)>, 4386743384: <weakref at 0x10
18520	 {'sys': <module 'sys' (built-in)>, 'builtins': <module 'builtins' (built-in)>, '_frozen_importlib':
9312	 {'__name__': 'posix', '__doc__': 'This module provides access to operating system functionality that
9312	 {'__name__': 'posix', '__doc__': 'This module provides access to operating system functionality that
9312	 {'__name__': 'os', '__doc__': "OS routines for NT or Posix depending on what system we're on.\n\nThi
9312	 {'__name__': 'socket', '__doc__': "This module provides socket operations and some related functions

types:
8804	 <class 'function'>
6586	 <class 'dict'>
5407	 <class 'tuple'>
1873	 <class 'weakref'>
1320	 <class 'list'>
1248	 <class 'wrapper_descriptor'>
1234	 <class 'cell'>
1173	 <class 'type'>
1064	 <class 'method_descriptor'>
1041	 <class 'getset_descriptor'>

### DEBUG: END MEMORY PROFILE ###
```

## PID Profiling

This tool makes extensive use of child processes - but they should always be fairly short-lived. A summary of the current status of child processes is available by setting

```yaml
debugging:
  pid_profile:
    interval: 5 minutes
```

which prints

```
### DEBUG: BEGIN PID PROFILE ###

There are 4 child processes. PIDs are: 21902, 21906, 21910, 21914 - spawned 11, 8, 5, 2 seconds ago, respectively
1 are zombie processes. PIDs are: 21902

### DEBUG: END PID PROFILE ###
```

## Disk Profiling

If repositories are configured, a repository cache and a number of temporary directories may be in use depending on how many tasks are executing. a profile of this information can be configured using

```yaml
debugging:
  disk_profile:
    interval: 5 minutes
```

which prints

```
### DEBUG: BEGIN DISK PROFILE ###

Repository cache: 300907 bytes
Temporary directory in use by PID 21914: /private/var/folders/zp/jytdbdmx5xs3vfp4g_kqfr3w0000gn/T/tmpwc0g93bo (300907 bytes)
Temporary directory in use by PID 21906: /private/var/folders/zp/jytdbdmx5xs3vfp4g_kqfr3w0000gn/T/tmpambauxnq (300907 bytes)
Temporary directory in use by PID 21910: /private/var/folders/zp/jytdbdmx5xs3vfp4g_kqfr3w0000gn/T/tmp1s8ih57t (300907 bytes)
No other open files.

### DEBUG: END DISK PROFILE ###
```