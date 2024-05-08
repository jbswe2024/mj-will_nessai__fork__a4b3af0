from nessai.flowmodel import FlowModel
from nessai.experimental.flows.glasflow import (
    GlasflowWrapper,
    get_glasflow_class,
    known_flows,
)
import numpy as np
import pytest


@pytest.mark.parametrize("name", known_flows.keys())
def test_get_glasflow_class(name):
    FlowClass = get_glasflow_class(f"glasflow-{name}")
    FlowClass(n_inputs=2, n_neurons=4, n_blocks=2, n_layers=1)


@pytest.mark.integration_test
def test_glasflow_integration(tmp_path):

    from glasflow.flows import RealNVP

    config = dict(
        model_config=dict(
            ftype="glasflow-realnvp",
            n_inputs=2,
            kwargs=None,
        )
    )

    flowmodel = FlowModel(config=config, output=tmp_path / "test")

    flowmodel.initialise()

    assert isinstance(flowmodel.model, GlasflowWrapper)
    assert isinstance(flowmodel.model._flow, RealNVP)

    flowmodel.train(np.random.randn(100, 2))
