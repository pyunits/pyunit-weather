#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2018/2/28 10:58
# @Author: Jtyoui@qq.com
from pyunit_weather import Weather
import pprint


def test_city():
    weather = Weather()
    w = weather.get_city_weather('九龙')
    pprint.pprint(w)


def test_county():
    weather = Weather()
    w = weather.get_county_weather('九龙')
    pprint.pprint(w)


if __name__ == '__main__':
    test_city()
    test_county()
