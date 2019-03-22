from functools import update_wrapper

import click

from dockerfile_bakery.dockerfile_assembler import invoke_generate
from dockerfile_bakery.utils import console


def main():
    cli(obj={})


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    """Dockerfile bakery"""
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug


def enable_debug_mode(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        if ctx.obj and ctx.obj['DEBUG']:
            return ctx.invoke(f, *args, **kwargs)
        else:
            try:
                return ctx.invoke(f, *args, **kwargs)
            except BaseException as e:
                console.error(e)

    return update_wrapper(new_func, f)


@cli.command(short_help="Generate dockerfiles from partial dockerfiles")
@click.argument('context_path',
                required=False,
                default=".",
                type=str)
@click.option('--partial-path', '-P',
              required=False,
              type=str,
              help="User account(oss.navercorp.com)")
@click.option('--generated-path', '-G',
              required=False,
              help="User account(oss.navercorp.com)")
@enable_debug_mode
def generate(context_path, partial_path, generated_path):
    """Generate dockerfiles from partial dockerfiles"""
    console.notice("Command generate")
    kargs = {
        "context_path": context_path
    }
    if partial_path is not None:
        kargs["partial_path"] = partial_path
    if generated_path is not None:
        kargs["generated_path"] = generated_path
    invoke_generate(**kargs)


if __name__ == '__main__':
    main()
