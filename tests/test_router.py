# coding: utf-8

import os
import unittest
import libmc
from libmc import Client


RES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')


class HashRouterCase(unittest.TestCase):

    def test_md5_router(self):
        server_list = ['localhost', 'myhost:11211', '127.0.0.1:11212',
                       'myhost:11213']
        mc = Client(server_list)

        md5_mc = Client(server_list, hash_fn=libmc.MC_HASH_MD5)
        rs = {
            'test:10000': 'localhost:11211',
            'test:20000': '127.0.0.1:11212',
            'test:30000': '127.0.0.1:11212',
            'test:40000': '127.0.0.1:11212',
            'test:50000': '127.0.0.1:11212',
            'test:60000': 'myhost:11213',
            'test:70000': '127.0.0.1:11212',
            'test:80000': '127.0.0.1:11212',
            'test:90000': '127.0.0.1:11212',
        }
        for k in rs:
            self.assertEqual(mc.get_host_by_key(k), rs[k])
            self.assertEqual(md5_mc.get_host_by_key(k), rs[k])

        for addr in server_list:
            ps = addr.split(':')

            if len(ps) == 1:
                hostname = ps[0]
                port = 11211
            else:
                hostname = ps[0]
                port = int(ps[1])

            if port == 11211:
                key = '%s-10' % hostname
            else:
                key = '%s:%s-10' % (hostname, port)

            self.assertEqual(mc.get_host_by_key(key),
                             '%s:%s' % (hostname, port))
            self.assertEqual(md5_mc.get_host_by_key(key),
                             '%s:%s' % (hostname, port))

    def test_md5_router_mass(self):
        with open(os.path.join(RES_DIR, 'server_port.csv')) as fhandler:
            server_list = [':'.join(addr.strip().split(','))
                           for addr in fhandler.readlines()]
        mc = Client(server_list, hash_fn=libmc.MC_HASH_MD5)
        with open(os.path.join(RES_DIR, 'key_pool_idx.csv')) as fhandler:
            for line in fhandler:
                key, idx_ = line.strip().split(',')
                idx = int(idx_)
                assert mc.get_host_by_key(key) == server_list[idx]

    def test_fnv1a_32_router(self):
        fnv1a_32_mc = Client([
            'localhost', 'myhost:11211', '127.0.0.1:11212', 'myhost:11213'
        ], hash_fn=libmc.MC_HASH_FNV1A_32)
        rs = {
            'test:10000': '127.0.0.1:11212',
            'test:20000': '127.0.0.1:11212',
            'test:30000': 'myhost:11213',
            'test:40000': 'myhost:11211',
            'test:50000': 'myhost:11211',
            'test:60000': '127.0.0.1:11212',
            'test:70000': '127.0.0.1:11212',
            'test:80000': 'myhost:11213',
            'test:90000': 'localhost:11211'
        }

        for k in rs:
            self.assertEqual(fnv1a_32_mc.get_host_by_key(k), rs[k])

    def test_crc_32_router(self):
        crc_32_mc = Client([
            'localhost', 'myhost:11211', '127.0.0.1:11212', 'myhost:11213'
        ], hash_fn=libmc.MC_HASH_CRC_32)
        rs = {
            'test:10000': '127.0.0.1:11212',
            'test:20000': '127.0.0.1:11212',
            'test:30000': '127.0.0.1:11212',
            'test:40000': 'myhost:11213',
            'test:50000': 'myhost:11211',
            'test:60000': 'localhost:11211',
            'test:70000': 'myhost:11213',
            'test:80000': 'myhost:11211',
            'test:90000': 'localhost:11211'
        }
        for k in rs:
            self.assertEqual(crc_32_mc.get_host_by_key(k), rs[k])
