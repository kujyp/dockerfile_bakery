import os

import pytest

from dockerfile_bakery.dockerfile_assembler import invoke_generate
from tests.utils import rm_rf


@pytest.fixture
def script_dir():
    return os.path.dirname(__file__)


@pytest.fixture
def testassets_path(script_dir):
    return os.path.join(script_dir, "assets", "case02")


@pytest.fixture
def generated_path():
    return "generated"


@pytest.fixture
def partial_path():
    return "partial_dockerfiles"


@pytest.fixture
def expected_generated_base_dockerfile_dir(testassets_path,
                                           generated_path):
    return os.path.join(testassets_path,
                        generated_path, "dockerfiles",
                        "registry.navercorp.com",
                        "mtengine",
                        "tf_bazel_builder_base")


@pytest.fixture
def expected_generated_builder_dockerfile_dir(testassets_path,
                                              generated_path):
    return os.path.join(testassets_path,
                        generated_path,
                        "dockerfiles",
                        "registry.navercorp.com",
                        "mtengine",
                        "tf_bazel_builder")


@pytest.fixture
def expected_generated_scripts_dir(testassets_path,
                                   generated_path):
    return os.path.join(testassets_path, generated_path, "scripts")


@pytest.fixture
def expected_tf_bazel_builder_base_dockerfile_count():
    return 2


@pytest.fixture
def expected_tf_bazel_builder_dockerfile_count(expected_tf_bazel_builder_base_dockerfile_count):
    return expected_tf_bazel_builder_base_dockerfile_count * 5 * 2


@pytest.fixture
def expected_generated_dockerfilepaths(testassets_path,
                                       generated_path):
    generated_base_dockerfile_dir = os.path.join(testassets_path,
                                                 generated_path, "dockerfiles",
                                                 "registry.navercorp.com",
                                                 "mtengine",
                                                 "tf_bazel_builder_base")
    generated_builder_dockerfile_dir = os.path.join(testassets_path,
                                                    generated_path,
                                                    "dockerfiles",
                                                    "registry.navercorp.com",
                                                    "mtengine",
                                                    "tf_bazel_builder")
    return [
        os.path.join(generated_base_dockerfile_dir,
                     "Dockerfile.cuda9.0_cudnn7.0_python2.7.15_tf1.12.0"),
        os.path.join(generated_base_dockerfile_dir,
                     "Dockerfile.cuda10.0_cudnn7.4_python2.7.15_tf1.12.0"),


        os.path.join(generated_builder_dockerfile_dir,
                     "Dockerfile.cuda9.0_cudnn7.0_python2.7.15_tf1.12.0_capability3.5_7.0"),
        os.path.join(generated_builder_dockerfile_dir,
                     "Dockerfile.cuda9.0_cudnn7.0_python2.7.15_tf1.12.0_capability5.2"),
        os.path.join(generated_builder_dockerfile_dir,
                     "Dockerfile.cuda9.0_cudnn7.0_python2.7.15_tf1.12.0_capability5.2_6.1"),
        os.path.join(generated_builder_dockerfile_dir,
                     "Dockerfile.cuda9.0_cudnn7.0_python2.7.15_tf1.12.0_capability6.1"),
        os.path.join(generated_builder_dockerfile_dir,
                     "Dockerfile.cuda9.0_cudnn7.0_python2.7.15_tf1.12.0_capability7.0"),

        os.path.join(generated_builder_dockerfile_dir,
                     "Dockerfile.cuda9.0_cudnn7.0_python2.7.15_tf1.12.0_capability3.5_7.0_xla"),

        os.path.join(generated_builder_dockerfile_dir,
                     "Dockerfile.cuda10.0_cudnn7.4_python2.7.15_tf1.12.0_capability3.5_7.0"),

        os.path.join(generated_builder_dockerfile_dir,
                     "Dockerfile.cuda10.0_cudnn7.4_python2.7.15_tf1.12.0_capability3.5_7.0_xla"),
    ]


# Region Test
def test_generate_should_generate_dockerfiles(testassets_path,
                                              partial_path,
                                              generated_path,
                                              expected_generated_dockerfilepaths,
                                              expected_generated_base_dockerfile_dir,
                                              expected_generated_builder_dockerfile_dir,
                                              expected_tf_bazel_builder_base_dockerfile_count,
                                              expected_tf_bazel_builder_dockerfile_count):
    rm_rf(os.path.join(testassets_path, generated_path))
    invoke_generate(testassets_path, partial_path, generated_path)

    for each_filepath in expected_generated_dockerfilepaths:
        assert os.path.exists(each_filepath), "Check [{}] existance.".format(each_filepath)


def test_should_build_script_contains_right_number_of_image(testassets_path,
                                                            partial_path,
                                                            generated_path,
                                                            expected_generated_scripts_dir,
                                                            expected_tf_bazel_builder_base_dockerfile_count,
                                                            expected_tf_bazel_builder_dockerfile_count):
    rm_rf(os.path.join(testassets_path, generated_path))
    invoke_generate(testassets_path, partial_path, generated_path)

    with open(os.path.join(expected_generated_scripts_dir, "build_tf_bazel_builder_base.sh"), 'r') as f:
        script_content = f.read()
        assert script_content.count("docker build") == expected_tf_bazel_builder_base_dockerfile_count

    with open(os.path.join(expected_generated_scripts_dir, "build_tf_bazel_builder.sh"), 'r') as f:
        script_content = f.read()
        assert script_content.count("docker build") == expected_tf_bazel_builder_dockerfile_count


def test_should_build_script_contains_appropriate_pull_option(testassets_path,
                                                              partial_path,
                                                              generated_path,
                                                              expected_generated_scripts_dir,
                                                              expected_tf_bazel_builder_base_dockerfile_count):
    rm_rf(os.path.join(testassets_path, generated_path))
    invoke_generate(testassets_path, partial_path, generated_path)

    with open(os.path.join(expected_generated_scripts_dir, "build_tf_bazel_builder_base.sh"), 'r') as f:
        script_content = f.read()
        assert script_content.count("docker build --pull") == expected_tf_bazel_builder_base_dockerfile_count

    with open(os.path.join(expected_generated_scripts_dir, "build_tf_bazel_builder.sh"), 'r') as f:
        script_content = f.read()
        assert script_content.count("docker build --pull") == 0


def test_should_build_script_contains_right_statement(testassets_path,
                                                      partial_path,
                                                      generated_path,
                                                      expected_generated_scripts_dir):
    rm_rf(os.path.join(testassets_path, generated_path))
    invoke_generate(testassets_path, partial_path, generated_path)

    with open(os.path.join(expected_generated_scripts_dir,
                           "build_tf_bazel_builder_base.sh"), 'r') as f:
        script_content = f.read()
        expected_build_statement = \
            "docker build"\
            " --pull"\
            " -t registry.navercorp.com/mtengine/tf_bazel_builder_base:cuda10.0_cudnn7.4_python2.7.15_tf1.12.0"\
            " -f ../dockerfiles/registry.navercorp.com/mtengine/tf_bazel_builder_base/Dockerfile.cuda10.0_cudnn7.4_python2.7.15_tf1.12.0"\
            " ."

        assert expected_build_statement in script_content

    with open(os.path.join(expected_generated_scripts_dir,
                           "build_tf_bazel_builder.sh"), 'r') as f:
        script_content = f.read()
        expected_build_statement = \
            "docker build" \
            " --pull" \
            " -t registry.navercorp.com/mtengine/tf_bazel_builder:cuda10.0_cudnn7.4_python2.7.15_tf1.12.0_capability3.5_7.0_xla" \
            " -f ../dockerfiles/registry.navercorp.com/mtengine/tf_bazel_builder/Dockerfile.cuda10.0_cudnn7.4_python2.7.15_tf1.12.0_capability3.5_7.0_xla" \
            " ."

        assert expected_build_statement in script_content


def test_should_pull_script_contains_right_number_of_image(testassets_path,
                                                           partial_path,
                                                           generated_path,
                                                           expected_generated_scripts_dir,
                                                           expected_tf_bazel_builder_base_dockerfile_count,
                                                           expected_tf_bazel_builder_dockerfile_count):
    rm_rf(os.path.join(testassets_path, generated_path))
    invoke_generate(testassets_path, partial_path, generated_path)

    with open(os.path.join(expected_generated_scripts_dir, "push_tf_bazel_builder_base.sh"), 'r') as f:
        script_content = f.read()
        assert script_content.count("docker push") == expected_tf_bazel_builder_base_dockerfile_count

    with open(os.path.join(expected_generated_scripts_dir, "push_tf_bazel_builder.sh"), 'r') as f:
        script_content = f.read()
        assert script_content.count("docker push") == expected_tf_bazel_builder_dockerfile_count


def test_should_pull_script_contains_right_statement(testassets_path,
                                                     partial_path,
                                                     generated_path,
                                                     expected_generated_scripts_dir):
    rm_rf(os.path.join(testassets_path, generated_path))
    invoke_generate(testassets_path, partial_path, generated_path)

    with open(os.path.join(expected_generated_scripts_dir, "push_tf_bazel_builder_base.sh"), 'r') as f:
        script_content = f.read()
        assert "docker push registry.navercorp.com/mtengine/tf_bazel_builder_base:cuda10.0_cudnn7.4_python2.7.15_tf1.12.0" in script_content
        assert "docker push registry.navercorp.com/mtengine/tf_bazel_builder_base:cuda9.0_cudnn7.0_python2.7.15_tf1.12.0" in script_content

    with open(os.path.join(expected_generated_scripts_dir, "push_tf_bazel_builder.sh"), 'r') as f:
        script_content = f.read()
        assert "docker push registry.navercorp.com/mtengine/tf_bazel_builder:cuda10.0_cudnn7.4_python2.7.15_tf1.12.0_capability3.5_7.0" in script_content
        assert "docker push registry.navercorp.com/mtengine/tf_bazel_builder:cuda10.0_cudnn7.4_python2.7.15_tf1.12.0_capability3.5_7.0_xla" in script_content
