from fabric.contrib.files import exists
from fabric.operations import run, sudo


def self_signed0(*args, **kwargs):
    run_cmd = sudo  # if kwargs.get('use_sudo') else run

    if exists(kwargs["SSL_KEYOUT"]) or exists(kwargs["SSL_CERTOUT"]):
        return "certs already exist; delete/rename to regenerate"

    # ${VAR%/*}
    run_cmd(
        "mkdir -p `basename {keyout}` `basename {certout}`".format(
            keyout=kwargs["SSL_KEYOUT"], certout=kwargs["SSL_CERTOUT"]
        )
    )

    run_cmd(
        "openssl req {}".format(
            " ".join(
                (
                    "-new",
                    "-newkey ec",
                    "-pkeyopt ec_paramgen_curve:prime256v1",
                    "-days 365",
                    "-nodes",
                    "-x509",
                    '-subj "{subj}"'.format(subj=kwargs["SSL_SUBJ"]),
                    "-keyout {keyout}".format(keyout=kwargs["SSL_KEYOUT"]),
                    "-out {certout}".format(certout=kwargs["SSL_CERTOUT"]),
                )
            )
        )
    )

    return "generated: {keyout} {certout}".format(
        keyout=kwargs["SSL_KEYOUT"], certout=kwargs["SSL_CERTOUT"]
    )
