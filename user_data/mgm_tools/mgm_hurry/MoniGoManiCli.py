# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-

# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------

"""MoniGoManiCli is the responsible module to communicate with the mgm strategy."""

# ___  ___               _  _____        ___  ___               _  _____  _  _
# |  \/  |              (_)|  __ \       |  \/  |              (_)/  __ \| |(_)
# | .  . |  ___   _ __   _ | |  \/  ___  | .  . |  __ _  _ __   _ | /  \/| | _
# | |\/| | / _ \ | '_ \ | || | __  / _ \ | |\/| | / _` || '_ \ | || |    | || |
# | |  | || (_) || | | || || |_\ \| (_) || |  | || (_| || | | || || \__/\| || |
# \_|  |_/ \___/ |_| |_||_| \____/ \___/ \_|  |_/ \__,_||_| |_||_| \____/|_||_|

import datetime
import json
import os
import shutil
import subprocess  # noqa: S404 (skip security check)
import shlex
import sys

import yaml

# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------


class MoniGoManiCli(object):
    """Use this module to communicate with the mgm hyperstrategy,."""

    log_output: bool = False
    output_path: str = None
    output_file_name: str = None

    def __init__(self, basedir, logger):
        """Instantiate a new object of mgm cli.

        Args:
            basedir (str): The directory
            logger (logger): The logger
        """
        self.basedir = basedir
        self.logger = logger

        self.log_output = True  # :todo move to mgm logger?
        self.output_path = '{0}/Some Test Results/'.format(self.basedir)
        self.output_file_name = 'MGM-Hurry-Command-Results-{0}.log'.format(datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))

    def installation_exists(self) -> bool:
        """Check if the MGM Hyper Strategy installation exists.

        Returns:
            success (bool): Whether or not the config and strategy files are found.
        """
        if os.path.exists('{0}/user_data/mgm-config.json'.format(self.basedir)) is False:
            self.logger.warning('🤷♂️ No "mgm-config.json" file found.')
            return False

        if os.path.exists('{0}/user_data/strategies/MoniGoManiHyperStrategy.py'.format(self.basedir)) is False:
            self.logger.warning('🤷♂️ No "MoniGoManiHyperStrategy.py" file found.')
            return False

        self.logger.debug('👉 MoniGoManiHyperStrategy and configuration found √')
        return True

    def create_config_files(self, target_dir: str) -> bool:
        """Copy example files as def files.

        Args:
            target_dir (str): The target dir where the "mgm-config.example.json" exists.

        Returns:
            success (bool): True if files are created, false if something failed.
        """
        example_files = [
            {
                'src': 'mgm-config.example.json',
                'dest': 'mgm-config.json',
            },
            {
                'src': 'mgm-config-private.example.json',
                'dest': 'mgm-config-private.json',
            },
        ]

        for example_file in example_files:
            src_file = target_dir + '/user_data/' + example_file['src']

            if not os.path.isfile(src_file):
                self.logger.error('❌ Bummer. Cannot find the example file "{0}" to copy from.'.format(example_file['src']))
                return False

            dest_file = target_dir + '/user_data/' + example_file['dest']

            if os.path.isfile(dest_file):
                self.logger.warning('⚠️ The target file "{0}" already exists. Is cool.'.format(example_file['dest']))
                continue

            shutil.copyfile(src_file, dest_file)

        self.logger.info('👉 MoniGoMani config files prepared √')
        return True

    def load_config_files(self) -> dict:
        """Load & Return all the MoniGoMani Configuration files.

        Including:
            - mgm-config
            - mgm-config-private
            - mgm-config-hyperopt
            - mgm-config-hurry

        Returns:
            dict: Dictionary containing all the MoniGoMani Configuration files
        """

        # Load the MGM-Hurry Config file if it exists
        with open('.hurry', 'r') as yml_file:
            config = yaml.full_load(yml_file) or {}

        hurry_config = config['config'] if 'config' in config else None

        if hurry_config is None:
            self.logger.error('🤷 No Hurry config file found. Please run: mgm-hurry setup')
            sys.exit(1)

        # Start loading the MoniGoMani config files
        mgm_config_files = {
            'mgm-config': {},
            'mgm-config-private': {},
            'mgm-config-hyperopt': {},
        }

        for mgm_config_filename in mgm_config_files:
            # Check if the MoniGoMani config filename exist in the ".hurry" config file
            if 'mgm_config_names' not in hurry_config or mgm_config_filename not in hurry_config['mgm_config_names']:
                self.logger.error('🤷 No "{0}" filename found in the ".hurry" config file. Please run: mgm-hurry setup'.format(mgm_config_filename))
                sys.exit(1)

            mgm_config_filepath = '{0}/user_data/{1}'.format(
                self.basedir,
                hurry_config['mgm_config_names'][mgm_config_filename],
            )

            # Check if the mandatory MoniGoMani config files exist
            if os.path.isfile(mgm_config_filepath) is False:
                if mgm_config_filename in ['mgm-config', 'mgm-config-private']:
                    self.logger.error('🤷 No "{0}" file found in the "user_data" directory. Please run: mgm-hurry setup'.format(mgm_config_filename))
                    sys.exit(1)

            elif (os.path.isfile(mgm_config_filepath) is False) and (mgm_config_filename == 'mgm-config-hyperopt'):
                self.logger.info('No "{0}" file found in the "user_data" directory.'.format(mgm_config_filename))

            # Load the MoniGoMani config file as an object and parse it as a dictionary
            else:
                file_object = open(mgm_config_filepath, )
                json_data = json.load(file_object)
                mgm_config_files[mgm_config_filename] = json_data

        # Append the previously loaded MGM-Hurry config file
        mgm_config_files['mgm-config-hurry'] = hurry_config

        return mgm_config_files

    def run_command(self,
                    command: str,
                    log_output: bool = None,
                    output_path: str = None,
                    output_file_name: str = None) -> int:
        """Execute shell command and log output to mgm logfile.

        :param command (str): Shell command to execute.
        :param log_output (bool, optional): Whether or not to log the output to mgm-logfile. Defaults to False.
        :param output_path (str, optional): Path to the output of the '.log' file. Defaults to 'Some Test Results/MoniGoMani_version_number/'
        :param output_file_name (str, optional): Name of the '.log' file. Defaults to 'Results-<Current-DateTime>.log'.
        :return int: return code zero (0) if all went ok. > 0 if there's an issue.
        """
        if command is None or command == '':
            self.logger.error(
                '🤷 Please pass a command through. Without command no objective, sir!'
            )
            sys.exit(1)

        if output_path is None:
            output_path = self.output_path

        if output_file_name is None:
            output_file_name = self.output_file_name

        if log_output is not None:
            self.log_output = log_output

        if self.log_output is True:
            output_file = open(self._get_logfile(output_path=output_path, output_file_name=output_file_name), 'w')

        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                if log_output is True:
                    self._write_log_line(output_file, output.strip())
        rc = process.poll()
        return rc

    def _get_logfile(self,
                     output_path: str,
                     output_file_name: str) -> str:
        """Get the full path to log file.

        Creates the output path directory if it not exists.
        Also creates the output file name if it not exists.

        :param output_path (str): The full path to the output log file. Defaults to None.
        :param output_file_name (str): The filename of the output log file. Defaults to None.
        :return str: full path to log file (including logfile name)

        :todo integrate in self.logger to avoid duplicate functionality
        """

        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        mgm_config_files = self.load_config_files()

        # create path like foo/bar/
        # and be sure only 1 repeating / is used
        output_path = os.path.normpath(
            os.path.join(
                output_path,
                mgm_config_files['mgm-config-private']['bot_name'],
                '/',
            ), )

        return os.path.join(output_path, output_file_name)

    def _write_log_line(self, log_file, line):
        """Writes clean log line to file.

        :param log_file (file.open()): The log file to write to.
        :param line (str): The data to log.

        :todo integrate in self.logger to avoid duplicate functionality
        """

        second_splitter = line.find(' - ', line.find(' - ') + 1) + 3
        trimmed_line = line[second_splitter:len(line)]
        if self.filter_line(trimmed_line) is False:
            log_file.write(trimmed_line)

    def exec_cmd(self, cmd: str, save_output: bool = False) -> int:
        self.logger.deprecated('Calling exec_cmd is deprecated. Please switch to public method run_command()')
        return self.run_command(cmd, log_output=save_output)

    def _exec_cmd(self, cmd: str, save_output: bool = False, output_path: str = None, output_file_name: str = None) -> int:
        self.logger.deprecated('Calling _exec_cmd is deprecated. Please switch to public method run_command()')
        return self.run_command(cmd, save_output, output_path, output_file_name)
