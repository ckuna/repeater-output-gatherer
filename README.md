# Repeater Ouput Gatherer
A very eager single threaded telnet client that logs telnet output and pongs the remote host every 10 seconds

# Usage
The following command would read telnet output from `127.0.0.1:7878` and log the output to a file `logfile.log`
```
repeater-output-gatherer.exe 127.0.0.1 7878 logfile.log
```
