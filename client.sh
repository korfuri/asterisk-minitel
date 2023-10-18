#!/usr/bin/env bash

(
    printf "Version: 1\r\nTXspeed: 133.333\r\nRXspeed: 8.33\r\n\r\n\x13S"  # ULM header
    sleep 0.2  # wait for the capabilities query
    printf "\x01aaa\x04"  # pretend to be the dumbest minitel
    sleep 0.5
    printf "TESTPIL\x13\x41"  # TEST, ENVOI
    sleep 0.2
) | nc -v 127.0.0.1 3615 | cat -e
