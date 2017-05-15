## nrdpy

### Overview

`nrdpy` is a library for submitting passive checks to [Nagios NRDP](https://github.com/NagiosEnterprises/nrdp) endpoints.

### Example

```python
from nrdpy import NRDP, HostResult, ServiceResult

# create a "host check" result

host_result = HostResult(host='server.local')

rtt = do_ping('server.local')

if rtt is not None:
    host_result.state = HostResult.Up
    host_result.output = '{}ms RTT'.format(rtt)
    host_result.add_perf_data('rtt', rtt, units='ms')
else:
    host_result.state = HostResult.Down

# create a "service check" result

service_result = ServiceResult(host='server.local', service='ssh')

connected = do_tcp_connect('server.local', port=22)

if connected == True:
    service_result.state = ServiceResult.Ok
else:
    service_result.state = ServiceResult.Critical

# submit check results

nagios = NRDP(endpoint='http://nagios.local/nrdp', token='psD0u8RUbeq')

nagios.submit(results=[host_result, service_result])
```
