#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2018/2/28 10:58
# @Author: Jtyoui@qq.com
from pyunit_weather import Weather
import pprint


def test():
    weather = Weather()
    w = weather.get_weather('台')
    pprint.pprint(w)


if __name__ == '__main__':
    test()
