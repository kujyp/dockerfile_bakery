import os
import errno
import shutil
import stat

from dockerfile_bakery.utils import console
from jinja2 import FileSystemLoader, Environment, meta


SEED_DOCKERFILE = "seed.Dockerfile"
GENERATED_MESSAGE = """\
###############################################################################
###############################################################################
###                                                                         ###
###                    GENERATED BY PARTIAL DOCKERFILE                      ###
###                    NOTE: DO NOT UPDATE MANUALLY                         ###
###                                                                         ###
###############################################################################
###############################################################################
"""

SCRIPT_PREFIX = """\
#!/bin/bash -e

""" + GENERATED_MESSAGE + """\

yellow="\\033[0;33m"
red="\\033[0;31m"
nocolor="\\033[0m"

get_script_path() {
    local _src="${BASH_SOURCE[0]}"
    while [[ -h "${_src}" ]]; do
        local _dir="$(cd -P "$( dirname "${_src}" )" && pwd)"
        local _src="$(readlink "${_src}")"
        if [[ "${_src}" != /* ]]; then _src="$_dir/$_src"; fi
    done
    echo $(cd -P "$(dirname "$_src")" && pwd)
}

cd_into_script_path() {
    local script_path=$(get_script_path)
    cd ${script_path}
}

command_exists() {
    command -v "$@" > /dev/null 2>&1
}

### Main
echo -e "${yellow}[INFO] [${BASH_SOURCE[0]}] executed.${nocolor}"

if ! command_exists docker; then
    echo -e "${red}[ERROR] Install docker first.\\n\\
[MacOS] $ brew cask install docker\\n\\
[Linux] $ curl -fsSL https://get.docker.com | sh${nocolor}"
    exit 1;
fi

(
cd_into_script_path

"""

SCRIPT_POSTFIX = """\
)
echo -e "${yellow}[INFO] [${BASH_SOURCE[0]}] Done.${nocolor}"
"""


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def rm_rf(path):
    assert path != "/"
    console.info("Delete files. [$ rm -rf {}] ...".format(path))
    if os.path.exists(path):
        shutil.rmtree(path)


def chmod_plus_x(path):
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)


def save(path, content):
    mkdir_p(os.path.dirname(path))
    with open(path, 'w') as f:
        f.write(content)


def load(path):
    with open(path, 'r') as f:
        return f.read()


class Environments:
    partialdockerfile_path = ""
    generated_path = ""
    generated_scripts_path = ""
    generated_dockerfile_path = ""
    generated_dockerfile_temp_path = ""
    jinja_env = None

    @classmethod
    def init(cls, partialdockerfile_path, generated_path):
        cls.partialdockerfile_path = partialdockerfile_path
        cls.generated_path = generated_path
        cls.generated_scripts_path = os.path.join(cls.generated_path, "scripts")
        cls.generated_dockerfile_path = os.path.join(cls.generated_path, "dockerfiles")
        cls.generated_dockerfile_temp_path = os.path.join(cls.generated_dockerfile_path, "temp")
        cls.jinja_env = Environment(
            loader=FileSystemLoader(partialdockerfile_path))

    @classmethod
    def get_generated_temp_dockerfile_path(cls, path):
        return os.path.join(cls.generated_dockerfile_temp_path, path)

    @classmethod
    def get_generated_dockerfile_path(cls, path):
        return os.path.join(cls.generated_dockerfile_path, path)


class GeneratedDockerfile:
    def __init__(self, path):
        self.path = path


class DockerfileTemplate(object):
    def __init__(self, path):
        self.filename = os.path.basename(path)
        self.dirname = os.path.dirname(path)
        self.generated_dockerfiles = []
        self.generated = False

    @property
    def path(self):
        return os.path.join(self.dirname, self.filename)

    def get_generated_dockerfiles(self):
        if self.generated:
            return self.generated_dockerfiles

        self._generate_dockerfiles()
        self.generated = True
        return self.generated_dockerfiles

    def _generate_dockerfiles(self):
        source, _, _ = Environments.jinja_env.loader.get_source(Environments.jinja_env, self.path)
        parsed = Environments.jinja_env.parse(source)
        variables = meta.find_undeclared_variables(parsed)

        if len(variables) == 0:
            targetpath = os.path.join(Environments.generated_dockerfile_temp_path, self.path)
            save(targetpath, Environments.jinja_env.get_template(self.path).render())
            self.generated_dockerfiles.append(GeneratedDockerfile(self.path))
            return

        spawned = {}
        idx_array = {}
        for each in variables:
            idx_array[each] = 0
            if each.startswith("__FROM__"):
                dependency_name = each[len("__FROM__"):]
                dependency_seed = DockerfileSeed.findby_dependency(dependency_name)
                spawned[each] = ["{}:{}".format(dependency_seed.imagename, eachtag) for eachtag in dependency_seed.get_taglist()]
                continue
            spawned[each] = self.get_subdockerfiles(each)

        iteration_end = False
        while not iteration_end:
            params = {}
            tag = ""
            for each in variables:
                params[each] = ""
                eachspawned = spawned[each][idx_array[each]]
                if isinstance(eachspawned, GeneratedDockerfile):
                    filepath = eachspawned.path
                    tag += os.path.basename(filepath).replace(".partial.Dockerfile", "").replace("partial.Dockerfile", "")
                    params[each] = load(Environments.get_generated_temp_dockerfile_path(filepath))
                elif isinstance(eachspawned, str):
                    tag = eachspawned[eachspawned.find(':') + 1:] + tag
                    params[each] = eachspawned

            rendered = Environments.jinja_env.get_template(self.path).render(
                **params
            )
            targetdirectory = os.path.dirname(self.path)
            targetfilename = os.path.basename(self.path).replace(".partial.Dockerfile", "") + tag + ".partial.Dockerfile"
            targetpath = os.path.join(targetdirectory, targetfilename)

            save(Environments.get_generated_temp_dockerfile_path(targetpath), rendered)
            self.generated_dockerfiles.append(GeneratedDockerfile(targetpath))
            for idx, each in enumerate(variables):
                idx_array[each] += 1
                if idx_array[each] >= len(spawned[each]):
                    if len(idx_array) - 1 == idx:
                        iteration_end = True
                        break
                    idx_array[each] = 0
                    continue
                else:
                    break

    def get_subdockerfiles(self, propertyname):
        ret = []
        parentpath = os.path.dirname(os.path.join(Environments.partialdockerfile_path, self.path))
        subpath = os.path.join(parentpath, propertyname)
        for dirpath, dirnames, filenames in os.walk(subpath):
            for filename in filenames:
                ret += DockerfileTemplate(os.path.join(os.path.join(self.dirname, propertyname), filename)) \
                    .get_generated_dockerfiles()
            # Retrieve top level directory only
            break

        return ret


class DockerfileSeed(DockerfileTemplate):
    seeds = set()

    @classmethod
    def findby_dependency(cls, dependency):
        for eachseed in cls.seeds:
            if os.path.basename(eachseed.imagename) == dependency:
                return eachseed
        return None

    def __init__(self, seedfile_path):
        super(DockerfileSeed, self).__init__(seedfile_path)
        self.taglist = []
        self.imagename = os.path.dirname(seedfile_path)
        self.dependency = self.get_dependency_from_template_or_none()
        DockerfileSeed.seeds.add(self)

    def get_dependency_from_template_or_none(self):
        source, _, _ = Environments.jinja_env.loader.get_source(Environments.jinja_env, os.path.join(self.imagename, SEED_DOCKERFILE))
        parsed = Environments.jinja_env.parse(source)
        variables = meta.find_undeclared_variables(parsed)
        for each in variables:
            if each.startswith("__FROM__"):
                return each[len("__FROM__"):]
        return None

    def generate_dockerfiles(self):
        assert self.generated is not None
        if self.generated:
            return

        dependency_seed = DockerfileSeed.findby_dependency(self.dependency)
        if dependency_seed is not None:
            dependency_seed.generate_dockerfiles()

        self._generate_dockerfiles()

        self.generated = True

    def get_taglist(self):
        assert self.generated is True
        assert self.taglist is not None
        return self.taglist

    def _generate_dockerfiles(self):
        super(DockerfileSeed, self)._generate_dockerfiles()
        for each_generated in self.generated_dockerfiles:
            generated_filename = os.path.basename(each_generated.path)
            tag = generated_filename.replace("seed.Dockerfile", "").replace(".partial.Dockerfile", "")
            fulldocker_filename = "Dockerfile.{}".format(tag)
            fulldocker_filepath = os.path.join(os.path.dirname(each_generated.path), fulldocker_filename)
            save(os.path.join(Environments.generated_dockerfile_temp_path, fulldocker_filepath),
                 load(os.path.join(Environments.generated_dockerfile_temp_path, each_generated.path)))
            os.remove(os.path.join(Environments.generated_dockerfile_temp_path, each_generated.path))
            save(os.path.join(Environments.generated_dockerfile_path, fulldocker_filepath),
                 GENERATED_MESSAGE + load(os.path.join(Environments.generated_dockerfile_temp_path, fulldocker_filepath)))
            self.taglist.append(tag)

        return

    def __eq__(self, other):
        if not isinstance(other, DockerfileSeed):
            return False
        return self.imagename == other.imagename

    def __hash__(self):
        return hash(self.imagename)

    def __repr__(self):
        return "DockerfileSeed: [{}]".format(self.__dict__)


def get_seed_list(path):
    ret = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename == SEED_DOCKERFILE:
                seedfile_path = os.path.join(
                    os.path.relpath(dirpath, path), filename)
                ret.append(DockerfileSeed(seedfile_path))
    return ret


def generate_dockerfiles():
    seed_list = get_seed_list(Environments.partialdockerfile_path)
    for eachseed in seed_list:
        eachseed.generate_dockerfiles()


def generate_build_script(imagename, dependency):
    script_content = ""

    script_content += SCRIPT_PREFIX
    if dependency is not None:
        script_content += "./build_{}.sh\n".format(dependency)

    cmds = {}
    for dirpath, dirnames, filenames in os.walk(Environments.get_generated_dockerfile_path(imagename)):
        relpath = os.path.relpath(dirpath, Environments.generated_scripts_path)
        for filename in filenames:
            if filename.startswith("Dockerfile."):
                tag = filename[len("Dockerfile."):]
            else:
                tag = "latest"

            pulloption = ""
            if dependency is None:
                pulloption = " --pull"
            cmds[tag] = "docker build{} -t {}:{} -f {}/{} .".format(pulloption,
                                                                    imagename,
                                                                    tag,
                                                                    relpath,
                                                                    filename)
        break

    for tag in sorted(cmds):
        script_content = script_content + cmds[tag] + '\n'

    script_content += SCRIPT_POSTFIX
    scriptpath = os.path.join(Environments.generated_scripts_path,
                              "build_{}.sh".format(os.path.basename(imagename)))
    save(scriptpath, script_content)
    chmod_plus_x(scriptpath)


def generate_build_scripts():
    seed_list = get_seed_list(Environments.partialdockerfile_path)
    for eachseed in seed_list:
        generate_build_script(eachseed.imagename, eachseed.dependency)


def generate_push_script(imagename):
    script_content = ""

    script_content += SCRIPT_PREFIX
    script_content += "./build_{}.sh\n".format(os.path.basename(imagename))

    cmds = {}
    for dirpath, dirnames, filenames in os.walk(
            Environments.get_generated_dockerfile_path(imagename)):
        for filename in filenames:
            if filename.startswith("Dockerfile."):
                tag = filename[len("Dockerfile."):]
            else:
                tag = "latest"

            cmds[tag] = "docker push {}:{}".format(imagename, tag)
        break

    for tag in sorted(cmds):
        script_content = script_content + cmds[tag] + '\n'

    script_content += SCRIPT_POSTFIX
    scriptpath = os.path.join(Environments.generated_scripts_path,
                              "push_{}.sh".format(os.path.basename(imagename)))
    save(scriptpath, script_content)
    chmod_plus_x(scriptpath)


def generate_push_scripts():
    seed_list = get_seed_list(Environments.partialdockerfile_path)
    for eachseed in seed_list:
        generate_push_script(eachseed.imagename)


def invoke_generate(context_path,
                    partial_path="partial_dockerfiles",
                    generated_path="generated"):
    partial_normpath = os.path.normpath(
        os.path.join(context_path, partial_path))
    generated_normpath = os.path.normpath(
        os.path.join(context_path, generated_path))

    console.info("partial_path=[{}], generated_path=[{}]".format(
        os.path.relpath(partial_path, "."),
        os.path.relpath(generated_path, "."),
    ))
    Environments.init(partial_normpath, generated_normpath)
    rm_rf(Environments.generated_path)

    generate_dockerfiles()
    generate_build_scripts()
    generate_push_scripts()
