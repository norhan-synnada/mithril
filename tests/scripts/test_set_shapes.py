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


from mithril.models import Add, IOKey, Model, Sigmoid

from .test_utils import check_shapes_semantically


def test_set_shapes_1():
    model = Model()

    model |= Sigmoid().connect("input1", IOKey("output1"))
    model |= Sigmoid().connect("input2", IOKey("output2"))

    model.set_shapes(input1=["a", "b"], input2=["b", "a"])

    ref_shapes = {
        "input1": ["a", "b"],
        "output1": ["a", "b"],
        "input2": ["b", "a"],
        "output2": ["b", "a"],
    }

    check_shapes_semantically(ref_shapes, model.shapes)


def test_set_shapes_1_kwargs_arg():
    model = Model()

    model |= Sigmoid().connect("input1", IOKey("output1"))
    model |= Sigmoid().connect("input2", IOKey("output2"))

    model.set_shapes(input1=["a", "b"], input2=["b", "a"])

    ref_shapes = {
        "input1": ["a", "b"],
        "output1": ["a", "b"],
        "input2": ["b", "a"],
        "output2": ["b", "a"],
    }

    check_shapes_semantically(ref_shapes, model.shapes)


def test_set_shapes_1_hybrid_arg():
    model = Model()

    model |= Sigmoid().connect("input1", IOKey("output1"))
    model |= Sigmoid().connect("input2", IOKey("output2"))

    model.set_shapes({model.input1: ["a", "b"]}, input2=["b", "a"])  # type: ignore

    ref_shapes = {
        "input1": ["a", "b"],
        "output1": ["a", "b"],
        "input2": ["b", "a"],
        "output2": ["b", "a"],
    }

    check_shapes_semantically(ref_shapes, model.shapes)


def test_set_shapes_1_hybrid_arg_same_metadata_1():
    model = Model()

    model |= Sigmoid().connect("input1", IOKey("output1"))
    model |= Sigmoid().connect("input2", IOKey("output2"))

    model.set_shapes({model.input2: ["a", "b"]}, input2=[2, 3])  # type: ignore
    assert model.shapes[model.input2.key] == [2, 3]  # type: ignore


def test_set_shapes_1_hybrid_arg_same_metadata_2():
    model = Model()

    model |= Sigmoid().connect("input1", IOKey("output1"))
    model |= Sigmoid().connect("input2", IOKey("output2"))

    model.set_shapes({model.input2: [2, 3]}, input2=["a", "b"])  # type: ignore
    assert model.shapes[model.input2.key] == [2, 3]  # type: ignore


def test_set_shapes_2():
    model = Model()

    model |= Sigmoid().connect("input1", IOKey("output1"))
    model |= Sigmoid().connect("input2", IOKey("output2"))

    model.set_shapes({model.input1: ["a", "b"], "input2": ["b", "a"]})  # type: ignore

    ref_shapes = {
        "input1": ["a", "b"],
        "output1": ["a", "b"],
        "input2": ["b", "a"],
        "output2": ["b", "a"],
    }

    check_shapes_semantically(ref_shapes, model.shapes)


def test_set_shapes_3():
    model = Model()

    model |= Sigmoid().connect("input1", IOKey("output1"))
    model |= Sigmoid().connect("input2", IOKey("output2"))

    model.set_shapes({model.input1: ["a", "b"], model.output2: ["b", "a"]})  # type: ignore

    ref_shapes = {
        "input1": ["a", "b"],
        "output1": ["a", "b"],
        "input2": ["b", "a"],
        "output2": ["b", "a"],
    }

    check_shapes_semantically(ref_shapes, model.shapes)


def test_set_shapes_4():
    model = Model()

    model |= (sig1 := Sigmoid()).connect("input1", IOKey("output1"))
    model |= (sig2 := Sigmoid()).connect("input2", IOKey("output2"))

    model.set_shapes({sig1.input: ["a", "b"], sig2.input: ["b", "a"]})

    ref_shapes = {
        "input1": ["a", "b"],
        "output1": ["a", "b"],
        "input2": ["b", "a"],
        "output2": ["b", "a"],
    }

    check_shapes_semantically(ref_shapes, model.shapes)


def test_set_shapes_5():
    model = Model()
    sub_model = Model()
    sub_model |= Sigmoid().connect("input1", IOKey("output1"))
    sub_model |= Sigmoid().connect("input1", "sub_out")

    model |= sub_model.connect(input1="input1", output1=IOKey("output"))
    model.set_shapes({sub_model.input1: [3, 4]})  # type: ignore


def test_set_shapes_6():
    model1 = Model()
    model2 = Model()
    model3 = Model()
    model4 = Model()

    model1 |= (add1 := Add()).connect(
        left="left", right="right", output=IOKey("output")
    )
    model2 += model1.connect(left="left", right="right", output=IOKey("output"))
    model3 += model2.connect(left="left", right="right", output=IOKey("output"))
    model4 += model3.connect(left="left", right="right", output=IOKey("output"))

    model3.set_shapes({add1.right: [3, 4], model4.output: [3, 4]}, left=[3, 4])  # type: ignore

    ref_shapes = {"left": [3, 4], "right": [3, 4], "output": [3, 4]}

    check_shapes_semantically(ref_shapes, model4.shapes)


def test_set_shapes_7():
    model1 = Model()
    model2 = Model()
    model3 = Model()
    model4 = Model()

    model1 += (add1 := Add()).connect(
        left="left", right="right", output=IOKey("output")
    )
    model2 += model1.connect(left="left", right="right", output=IOKey("output"))
    model3 += model2.connect(left="left", right="right", output=IOKey("output"))
    model4 += model3.connect(left="left", right="right", output=IOKey("output"))

    model3.set_shapes({"left": [3, 4], add1.right: [3, 4], model4.output: [3, 4]})  # type: ignore

    ref_shapes = {"left": [3, 4], "right": [3, 4], "output": [3, 4]}

    check_shapes_semantically(ref_shapes, model4.shapes)


def test_set_shapes_8():
    model = Model()
    model += Add().connect(left="left", right="right", output=IOKey("output"))
    model.set_shapes(left=[("V1", ...)], right=[("V1", ...)], output=[("V1", ...)])

    ref_shapes = {
        "left": ["(V1, ...)"],
        "right": ["(V1, ...)"],
        "output": ["(V1, ...)"],
    }
    check_shapes_semantically(ref_shapes, model.shapes)


def test_comparison_connection_set_shape():
    model1 = Model()
    model2 = Model()
    model3 = Model()
    model4 = Model()

    model1 += (add1 := Add()).connect(
        left="left", right="right", output=IOKey("output")
    )
    model2 += model1.connect(left="left", right="right", output=IOKey("output"))
    model3 += model2.connect(left="left", right="right", output=IOKey("output"))
    model4 += model3.connect(left="left", right="right", output=IOKey("output"))
    model4 += (add2 := Add()).connect(right="final_right", output=IOKey("final_output"))

    add1.left.set_shapes([3, 4])
    add1.right.set_shapes([3, 4])
    add2.right.set_shapes([3, 4])

    ref_shapes = {
        "left": [3, 4],
        "right": [3, 4],
        "final_right": [3, 4],
        "output": [3, 4],
        "final_output": [3, 4],
    }

    check_shapes_semantically(ref_shapes, model4.shapes)


def test_comparison_connection__without_model_set_shape():
    model1 = Model()
    model2 = Model()
    model3 = Model()
    model4 = Model()

    model1 += Add().connect(left="left", right="right", output=IOKey("output"))
    model2 += model1.connect(left="left", right="right", output=IOKey("output"))
    model3 += model2.connect(left="left", right="right", output=IOKey("output"))

    left = IOKey("left")
    left.set_shapes([3, 4])
    right = IOKey("right")
    right.set_shapes([3, 4])
    final_right = IOKey("final_right")
    final_right.set_shapes([3, 4])

    model4 += model3.connect(left=left, right=right, output=IOKey("output"))
    model4 += Add().connect(right=final_right, output=IOKey("final_output"))

    ref_shapes = {
        "left": [3, 4],
        "right": [3, 4],
        "final_right": [3, 4],
        "output": [3, 4],
        "final_output": [3, 4],
    }

    check_shapes_semantically(ref_shapes, model4.shapes)
