#!/bin/bash

BASEDIR=$(dirname $0)
psql -h localhost -d postgres -c "drop database test" 
psql -h localhost -d postgres -c "create database test"
psql -h localhost -d test -f $BASEDIR/001_create.sql
psql -h localhost -d test -f $BASEDIR/002_treasury_and_vendingaddress.sql
psql -h localhost -d test -f $BASEDIR/100_fakeBaseData.sql
