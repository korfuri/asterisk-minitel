#!/usr/bin/env bash

printf "Version: 1\r\nTXspeed: 133.333\r\nRXspeed: 8.33\r\n\r\n\x13" | nc -v 127.0.0.1 3615
