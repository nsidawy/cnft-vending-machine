#!/bin/bash

psql -c "drop database test" 
psql -c "create database test"
psql -d test -f 001_create.sql
psql -d test -f 002_fakeBaseData.sql
