import re
import chardet
import math
import osa


def open_file(address_file):
    with open(address_file, 'rb') as f:
        data = f.read()
        result = chardet.detect(data)
        s = data.decode(result['encoding'])
        s = ' '.join(s.split(chr(10))).split(chr(32))
        return s


def convert_to_cel(address_file):
    result = open_file(address_file)
    sum_temp = 0
    for el in result:
        result.remove('F')
        if el != 'F':
            sum_temp += int(el)
    res = sum_temp / len(result)
    client = osa.Client('http://www.webservicex.net/ConvertTemperature.asmx?WSDL')
    print(client.service.ConvertTemp(res, 'degreeFahrenheit', 'degreeCelsius'))


def count(address_file):
    result = open_file(address_file)
    client = osa.Client('http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL')
    i = 1
    j = 2
    sum_count = 0
    while j < len(result):
        sum_count += math.ceil(client.service.ConvertToNum('', result[j], 'rub', result[i], 'true', '', ''))
        i += 3
        j += 3
    print(sum_count)


def convert_to_km(address_file):
    result = open_file(address_file)
    client = osa.Client('http://www.webservicex.net/length.asmx?WSDL')
    i = 1
    sum_distance = 0
    while i < len(result):
        value = re.sub(',', '', result[i])
        sum_distance += round(client.service.ChangeLengthUnit(value, 'Miles', 'Kilometers'), 2)
        i += 3
    print(sum_distance)


convert_to_cel('temps.txt')
print()
count('currencies.txt')
print()
convert_to_km('travel.txt')
