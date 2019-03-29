import os

import pytest

from dockerfile_bakery.dockerfile_assembler import invoke_generate
from tests.utils import rm_rf


@pytest.fixture
def script_dir():
    return os.path.dirname(__file__)


@pytest.fixture
def assets_path(script_dir):
    return os.path.join(script_dir, "assets")


def test_generate_case01(assets_path):
    testassets_path = os.path.join(assets_path, "case01")
    partial_path = "partial_dockerfiles"
    generated_path = "generated"

    rm_rf(os.path.join(testassets_path, generated_path))
    invoke_generate(testassets_path, partial_path, generated_path)

    expected_generated_dockerfilepaths = [
        os.path.join(testassets_path, generated_path, "dockerfiles", "python_base", "Dockerfile.python2.7.15"),
        os.path.join(testassets_path, generated_path, "dockerfiles", "python_base", "Dockerfile.python3.6.7"),
    ]
    for each_filepath in expected_generated_dockerfilepaths:
        assert os.path.exists(each_filepath)

    generated_scripts_dir = os.path.join(testassets_path, generated_path, "scripts")
    with open(os.path.join(generated_scripts_dir, "build_python_base.sh"), 'r') as f:
        script_content = f.read()
        assert "docker build --pull -t python_base:python2.7.15 -f ../dockerfiles/python_base/Dockerfile.python2.7.15 ." in script_content
        assert "docker build --pull -t python_base:python3.6.7 -f ../dockerfiles/python_base/Dockerfile.python3.6.7 ." in script_content

    with open(os.path.join(generated_scripts_dir, "push_python_base.sh"), 'r') as f:
        script_content = f.read()
        assert "docker push python_base:python2.7.15" in script_content
        assert "docker push python_base:python3.6.7" in script_content
