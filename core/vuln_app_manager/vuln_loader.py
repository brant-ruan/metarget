"""
Application Vulnerabilities Loader
"""

import yaml
import glob

import config
import utils.color_print as color_print


def load_vuln(filename):
    """Load information about one vulnerability from one file.

    Args:
        filename: File storing information of specific vulnerability.

    Returns:
        If loading succeeds, return information dict about the vulnerability,
        else, return None.
    """
    try:
        with open(filename, 'r') as f:
            # for SafeLoader, see
            # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
            vuln = yaml.load(f, Loader=yaml.SafeLoader)
            # e.g. path: vulns_app/thinkphp/5.0.23-rce/
            vuln['path'] = filename[:len(
                filename) - len(config.vuln_app_desc_file)]
            return vuln
    except FileNotFoundError:
        color_print.warning(
            '{filename} does not exist, skipped.'.format(
                filename=filename))
        return None


def load_vulns(files):
    content = list()
    for f in files:
        vuln = load_vuln(f)
        if vuln:
            content.append(vuln)
    return content


def load_vulns_by_dir(dirname, recursive=False):
    vuln_files = glob.glob(
        '{dirname}/{appv_desc}'.format(
            dirname=dirname,
            appv_desc=config.vuln_app_desc_file),
        recursive=recursive)
    return load_vulns(vuln_files)


if __name__ == '__main__':
    print(
        load_vulns_by_dir(
            '/Users/rambo/pjts/metarget-gitlab/metarget/vulns_app/*/*',
            recursive=True))
