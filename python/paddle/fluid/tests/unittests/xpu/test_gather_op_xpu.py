#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
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

from __future__ import print_function
import unittest
import sys
sys.path.append("..")

import numpy as np

import paddle
import paddle.fluid as fluid
from op_test import OpTest
from op_test_xpu import XPUOpTest

paddle.enable_static()


def gather_numpy(x, index, axis):
    x_transpose = np.swapaxes(x, 0, axis)
    tmp_gather = x_transpose[index, ...]
    gather = np.swapaxes(tmp_gather, 0, axis)
    return gather


class TestXPUGatherOp(XPUOpTest):
    def setUp(self):
        self.op_type = "gather"
        self.use_xpu = True
        self.use_mkldnn = False
        self.attrs = {'use_xpu': True}

        self.config()
        xnp = np.random.random(self.x_shape).astype(self.x_type)
        self.inputs = {
            'X': xnp,
            'Index': np.array(self.index).astype(self.index_type)
        }
        self.outputs = {'Out': self.inputs["X"][self.inputs["Index"]]}

    def config(self):
        """
        For multi-dimension input
        """
        self.dtype = np.float32
        self.x_shape = (10, 20)
        self.x_type = np.float32
        self.index = [1, 3, 5]
        self.index_type = np.int32

    def test_check_output(self):
        if paddle.is_compiled_with_xpu():
            place = paddle.XPUPlace(0)
            self.check_output_with_place(place)

    def test_check_grad(self):
        if paddle.is_compiled_with_xpu():
            place = paddle.XPUPlace(0)
            self.check_grad_with_place(place, ['X'], 'Out')


class TestCase1(TestXPUGatherOp):
    def config(self):
        """
        For one dimension input
        """
        self.dtype = np.float32
        self.x_shape = (100)
        self.x_type = np.float32
        self.index = [1, 3, 5]
        self.index_type = np.int32


class TestCase2(TestXPUGatherOp):
    def config(self):
        """
        For int64_t index type
        """
        self.dtype = np.float32
        self.x_shape = (100)
        self.x_type = np.float32
        self.index = [1, 3, 5]
        self.index_type = np.int64


class TestCase3(TestXPUGatherOp):
    def config(self):
        """
        For other input type
        """
        self.dtype = np.float32
        self.x_shape = (10, 20)
        self.x_type = np.float32
        self.index = [1, 3, 5]
        self.index_type = np.int32


class TestCase4(TestXPUGatherOp):
    def config(self):
        self.dtype = np.float32
        self.x_shape = (10, 20)
        self.attrs = {'use_xpu': True, 'overwrite': False}
        self.x_type = np.float32
        self.index = [1, 1]
        self.index_type = np.int32


class TestCase5(TestXPUGatherOp):
    def config(self):
        self.dtype = np.float32
        self.x_shape = (10, 20)
        self.attrs = {'use_xpu': True, 'overwrite': False}
        self.x_type = np.float32
        self.index = [1, 1, 3]
        self.index_type = np.int32


class TestCase6(TestXPUGatherOp):
    def config(self):
        self.dtype = np.float32
        self.x_shape = (10, 20)
        self.attrs = {'use_xpu': True, 'overwrite': True}
        self.x_type = np.float32
        self.index = [1, 3]
        self.index_type = np.int32


class TestCase7(TestXPUGatherOp):
    def config(self):
        self.dtype = np.float32
        self.x_shape = (10, 20)
        self.attrs = {'use_xpu': True, 'overwrite': True}
        self.x_type = np.float32
        self.index = [1, 3]
        self.index_type = np.int64


## test fp16
class TestCaseFP161(TestXPUGatherOp):
    def config(self):
        """
        For one dimension input
        """
        self.dtype = np.float16
        self.x_shape = (100)
        self.x_type = np.float16
        self.index = [1, 3, 5]
        self.index_type = np.int32


class TestCaseFP162(TestXPUGatherOp):
    def config(self):
        """
        For int64_t index type
        """
        self.dtype = np.float16
        self.x_shape = (100)
        self.x_type = np.float16
        self.index = [1, 3, 5]
        self.index_type = np.int64


class TestCaseFP163(TestXPUGatherOp):
    def config(self):
        """
        For other input type
        """
        self.dtype = np.float16
        self.x_shape = (10, 20)
        self.x_type = np.float16
        self.index = [1, 3, 5]
        self.index_type = np.int32


class TestCaseFP164(TestXPUGatherOp):
    def config(self):
        self.dtype = np.float16
        self.x_shape = (10, 20)
        self.attrs = {'use_xpu': True, 'overwrite': False}
        self.x_type = np.float16
        self.index = [1, 1]
        self.index_type = np.int32


class TestCaseFP165(TestXPUGatherOp):
    def config(self):
        self.dtype = np.float16
        self.x_shape = (10, 20)
        self.attrs = {'use_xpu': True, 'overwrite': False}
        self.x_type = np.float16
        self.index = [1, 1, 3]
        self.index_type = np.int32


class TestCaseFP166(TestXPUGatherOp):
    def config(self):
        self.dtype = np.float16
        self.x_shape = (10, 20)
        self.attrs = {'use_xpu': True, 'overwrite': True}
        self.x_type = np.float16
        self.index = [1, 3]
        self.index_type = np.int32


class TestCaseFP167(TestXPUGatherOp):
    def config(self):
        self.dtype = np.float16
        self.x_shape = (10, 20)
        self.attrs = {'use_xpu': True, 'overwrite': True}
        self.x_type = np.float16
        self.index = [1, 3]
        self.index_type = np.int64


if __name__ == "__main__":
    unittest.main()
