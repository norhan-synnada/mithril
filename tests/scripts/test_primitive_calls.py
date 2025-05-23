# Copyright 2022 Synnada, Inc.
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

import pytest

import mithril as ml
from mithril.models import Model, Power, Tensor


def test_power_call_threshold_iokey():
    model = Model()
    pow = Power(robust=True, threshold=ml.TBD)
    model += pow.connect(threshold=ml.IOKey("t", Tensor(0.1)))
    assert model.t.metadata.value == 0.1  # type: ignore


def test_error_not_robust_power_call_threshold_iokey():
    pow = Power(robust=False, threshold=ml.TBD)

    with pytest.raises(ValueError) as error_info:
        pow.connect(threshold=ml.IOKey("t", 0.1))

    error_msg = str(error_info.value)
    assert error_msg == "Power does not accept threshold argument when robust is False."


def test_error_not_robust_power_call_threshold_str():
    pow = Power(robust=False, threshold=ml.TBD)

    with pytest.raises(ValueError) as error_info:
        pow.connect(threshold="t")

    error_msg = str(error_info.value)
    assert error_msg == "Power does not accept threshold argument when robust is False."


def test_error_not_robust_power_call_threshold_float():
    pow = Power(robust=False, threshold=ml.TBD)

    with pytest.raises(ValueError) as error_info:
        pow.connect(threshold=Tensor(0.1))

    error_msg = str(error_info.value)
    assert error_msg == "Power does not accept threshold argument when robust is False."


@pytest.mark.skip("This test seems incomplete.")
def test_compile_robust_power_call_with_default_threshold():
    backend = ml.TorchBackend()
    pow = Power(robust=True)
    pm = ml.compile(pow, backend)
    pm.evaluate(data={"base": backend.ones(3, 3), "exponent": backend.ones(3, 3)})


@pytest.mark.skip(
    reason="This test is not yet implemented. Naming convention bugs"
    "should be fix when ToTensor like auto-added models created."
)
def test_error_robust_power_call_threshold_re_set_value():
    rob_pow = Model()
    primitive_pow = Power(robust=True)
    rob_pow += primitive_pow.connect(threshold="threshold")
    primitive_pow.set_values(threshold=1.3)
    from mithril.types import Constant

    mean_model = Model()
    with pytest.raises(ValueError):
        mean_model += rob_pow.connect(threshold=Constant.MIN_POSITIVE_SUBNORMAL)


@pytest.mark.skip(
    reason="This test is not yet implemented. Naming convention bugs"
    "should be fix when ToTensor like auto-added models created."
)
def test_error_robust_power_call_threshold_input_keys():
    model1 = Model()
    pow1 = Power(robust=True)
    model1 += pow1.connect(threshold=ml.IOKey("thres", 0.1))

    model2 = Model()
    pow2 = Power(robust=True)
    model2 += pow2.connect(threshold="thres")
    model2.set_values(thres=0.1)

    assert model1.input_keys == model2.input_keys
