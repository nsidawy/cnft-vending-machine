#!/bin/bash

BASEDIR=$(dirname $0)
psql -U postgres -h localhost -c "drop database test" 
psql -U postgres -h localhost -c "create database test"
psql -U postgres -h localhost -d test -f $BASEDIR/001_create.sql
psql -U postgres -h localhost -d test -f $BASEDIR/002_treasury.sql
psql -U postgres -h localhost -d test -f $BASEDIR/100_fakeBaseData.sql
