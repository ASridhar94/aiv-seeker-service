#!/bin/env bash
psql -U postgres -c "CREATE USER admin PASSWORD 'aivseekerservice123'"
psql -U postgres -c "CREATE DATABASE aiv_seeker OWNER admin"
