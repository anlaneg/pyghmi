# encoding:utf-8
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2015 Lenovo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyghmi.ipmi.oem.lenovo.inventory import EntryField, \
    parse_inventory_category_entry
#指明raw格式的消息结构，也相当于定义了结构体（类型为dict,每个field是实体的key)
cpu_fields = (
    EntryField("index", "B"),
    EntryField("Cores", "B"),
    EntryField("Threads", "B"),
    EntryField("Manufacturer", "13s"),
    EntryField("Family", "30s"),
    EntryField("Model", "30s"),
    EntryField("Stepping", "3s"),
    EntryField("Maximum Frequency", "<I",
               valuefunc=lambda v: str(v) + " MHz"),
    EntryField("Reserved", "h", include=False))


#定义如何自raw中解析出cpu信息字段
#有两个返回值，1返回解析的raw长度，2返回解析的对象取值
def parse_cpu_info(raw):
    return parse_inventory_category_entry(raw, cpu_fields)


def get_categories():
    return {
        "cpu": {
            "idstr": "CPU {0}",#用于格式化每一个实例，{0}为0，1，2。。。。
            "parser": parse_cpu_info,
            "command": {
                "netfn": 0x06,
                "command": 0x59,
                "data": (0x00, 0xc1, 0x01, 0x00)
            }
        }
    }
