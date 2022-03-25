# 17T Birmingham Magnet Support and Emulator

### Technical Manual Locataion

`\\isis\shares\ISIS_Experiment_Controls\Manuals\Birmingham_17T_Magnet\`

### Support Repository:
https://github.com/ISISComputingGroup/EPICS_17T_Birmingham_Magnet

### IOC Repository:
https://github.com/ISISComputingGroup/EPICS-ioc/tree/6850_17T_Birmingham_Magnet/B17TMAG

## Useful Commands

To start EPICS environment locally, simply run the `config_env` script: 
`C:\Instrument\Apps\EPICS\config_env`

When the IOC is running, you can use the following command to checks record values:
`<epics command> %mypvprefix%B17TMAG-IOC-01:<PV record>`

To test the IOC using LEWIS emulator, execute the `run_test.bat` script located:
`master\system_tests\run_tests.bat`

Add `-a` flag to `run_test.bat` to run IOC emulator and not tests straight away if wishing to view in IBEX or check PV values when testing.


### Connecting to Emulator

To connect to the emulator, either use the below example script of putty:

```python
import socket



OUT_TERMINATOR = "\r"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 52088))

while True:
    cmd = input("ouput")
    s.sendall(cmd + OUT_TERMINATOR)
    data = s.recv(4096)  # Needs to be longer than the returned message
    print(data)

s.close()
```

