import os

from dockerfile_bakery import consts, dockerfile_generator
from dockerfile_bakery.dockerfile_generator import rm_rf
from dockerfile_bakery.utils import console


def get_seed_yaml_list(path):
    ret = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename == consts.SEED_YAML_FILENAME:
                seedfile_path = os.path.join(dirpath, filename)
                ret.append(seedfile_path)
    return ret


def generate_dockerfiles(partialdockerfile_path):
    seed_list = get_seed_yaml_list(partialdockerfile_path)
    for eachseed in seed_list:
        dockerfile_generator.generate_dockerfile(eachseed)


def invoke_generate(context_path,
                    partial_path,
                    generated_path):
    partial_normpath = os.path.normpath(
        os.path.join(context_path, partial_path))
    generated_normpath = os.path.normpath(
        os.path.join(context_path, generated_path))

    console.info("partial_path=[{}], generated_path=[{}]".format(
        os.path.relpath(partial_path, "."),
        os.path.relpath(generated_path, "."),
    ))

    rm_rf(generated_normpath)

    generate_dockerfiles(partial_normpath)
