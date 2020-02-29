#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/29 13:31
# @Author: Jtyoui@qq.com
"""数据来自于 中央气象台 http://www.nmc.cn/publish/forecast/AGZ/guiyang.html"""
from fake_useragent import UserAgent
from bs4 import BeautifulSoup, Tag
import requests
import json
import os


class Weather:
    def __init__(self):
        self.ua = UserAgent()
        self.city = []
        with open(os.path.dirname(__file__) + os.sep + 'address.txt', encoding='utf-8')as fp:
            for line in fp:
                self.city.append(line.strip().split())

    def get_weather(self, city):
        """获取天气预报的信息

        :param city: 城市
        """
        message = {}
        data = list(filter(lambda x: x[1] == city, self.city))
        if not data:
            return '没有该城市的天气预报，请查看城市表'
        else:
            data = data[0]
        u, code = data[3], data[2]
        url = f'http://www.nmc.cn{u}'
        text = self._get_html(url)
        soup = BeautifulSoup(text, 'html.parser')
        message['标题'] = soup.title.string  # 标题
        message['城市'] = soup.find(name='div', class_='cname fl').text.strip()  # 城市
        real_url = f'http://www.nmc.cn/f/rest/real/{code}'
        aqi_url = f'http://www.nmc.cn/f/rest/aqi/{code}'
        real_text = self._get_html(real_url) or '{}'
        aqi_text = self._get_html(aqi_url) or '{}'
        real_text_json = json.loads(real_text)
        aqi_text_json = json.loads(aqi_text)
        warns = real_text_json.get('warn')
        if warns:
            warning = {'警告': warns.get('alert'), '发行内容': warns.get('issuecontent'), '防御指南': warns.get('fmeans')}
            message['本市警告'] = warning
        message['发布时间'] = real_text_json.get('publish_time')  # 发布时间
        weather = real_text_json.get('weather')
        if weather:
            message['气温'] = weather.get('temperature')  # 气温
            message['降水'] = weather.get('rain')  # 降水
            message['相对湿度'] = weather.get('humidity')  # 相对湿度
            message['舒适度'] = weather.get('rcomfort')  # 舒适度
            message['体感温度'] = weather.get('feelst')  # 体感温度
            message['空气压力'] = weather.get('airpressure')  # 空气压力
            message['温差'] = weather.get('temperatureDiff')  # 温差

        message['风向风速风级'] = real_text_json.get('wind')  # 风向风速风级
        message['空气质量指数'] = aqi_text_json.get('aqi')  # 空气质量指数
        message['七天天气预报'] = self._get_weather_forecast(soup)
        message['精细预报'] = self._get_fine_prediction(soup)
        return message

    def _get_html(self, url):
        """根据URL地址获取数据"""
        response = requests.get(url=url, headers={'User-Agent': self.ua.random})
        response.encoding = response.apparent_encoding
        text = response.text
        return text

    @staticmethod
    def _get_weather_forecast(soup):
        """获取七天天气预报"""
        forecast = []
        for day in soup.find_all(name='div', class_='day'):
            date = day.find(name='div', class_='date').text.strip()
            week = day.find(name='div', class_='week').text.strip()
            desc = day.find(name='div', class_='wdesc').text.strip()
            temp = day.find(name='div', class_='temp').text.strip()
            direct = day.find(name='div', class_='direct').text.strip()
            wind = day.find(name='div', class_='wind').text.strip()
            forecast.append({'日期': date, '星期': week, '气象': desc, '温度': temp, '风向': direct, '风速': wind})
        return forecast

    @staticmethod
    def _get_fine_prediction(soup):
        """获取精细预报"""
        prediction = {}
        for index, hour in enumerate(soup.find_all(name='div', class_='hour3'), 1):
            ls = []
            for content in hour.contents:
                if isinstance(content, Tag):
                    days = []
                    for con in content.contents:
                        if isinstance(con, Tag):
                            text = con.text.strip()
                            if text == '天气现象':
                                break
                            days.append(text)
                    else:
                        ls.append(days)
            days = []
            for i in range(1, 9):
                days.append(
                    {
                        '时间': ls[0][i],
                        '气温': ls[1][i],
                        '降水': ls[2][i],
                        '风速': ls[3][i],
                        '风向': ls[4][i],
                        '气压': ls[5][i],
                        '相对湿度': ls[6][i],
                        '云量': ls[7][i],
                        '能见度': ls[8][i],
                    }
                )
            prediction[f'第{index}天每3个小时预报'] = days
        return prediction
