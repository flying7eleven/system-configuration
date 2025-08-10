#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from dataclasses import dataclass, asdict
from json import loads, dumps
from os.path import expanduser


@dataclass
class WirePlumberProperties(object):
    volume: float
    mute: bool
    channelMap: list[str]
    channelVolumes: list[float]


class WirePlumberConfigurationEntry(object):
    def __init__(self, selection_property: str, selection_pattern: str, configuration: str):
        self._selection_property = selection_property
        self._selection_pattern = selection_pattern
        self._configuration = WirePlumberProperties(**loads(configuration))

    def set_channel_volume(self, volume: float) -> bool:
        if volume < 0.0 or volume > 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")

        changed = any(abs(channel_volume - volume) > 0.001 for channel_volume in self._configuration.channelVolumes)

        for channel_idx in range(len(self._configuration.channelVolumes)):
            self._configuration.channelVolumes[channel_idx] = volume

        return changed


class WirePlumberAudioSink(WirePlumberConfigurationEntry):
    def __init__(self, selection_property: str, selection_pattern: str, configuration: str):
        super(WirePlumberAudioSink, self).__init__(selection_property, selection_pattern, configuration)

    def __repr__(self):
        return f'Audio/Sink:{self._selection_property}:{self._selection_pattern.replace(" ", "\\s")}={dumps(asdict(self._configuration))}'


class WirePlumberInputAudio(WirePlumberConfigurationEntry):
    def __init__(self, selection_property: str, selection_pattern: str, configuration: str):
        super(WirePlumberInputAudio, self).__init__(selection_property, selection_pattern, configuration)

    def __repr__(self):
        return f'Input/Audio:{self._selection_property}:{self._selection_pattern.replace(" ", "\\s")}={dumps(asdict(self._configuration))}'


class WirePlumberOutputAudio(WirePlumberConfigurationEntry):
    @staticmethod
    def create_new(selection_pattern: str):
        return WirePlumberOutputAudio("application.name", selection_pattern,
                                      '{"volume": 1.0, "mute": false, "channelMap": ["FL", "FR"], "channelVolumes": [1.0, 1.0]}')

    def __init__(self, selection_property: str, selection_pattern: str, configuration: str):
        super(WirePlumberOutputAudio, self).__init__(selection_property, selection_pattern, configuration)

    def __repr__(self):
        return f'Output/Audio:{self._selection_property}:{self._selection_pattern.replace(" ", "\\s")}={dumps(asdict(self._configuration))}'


class WirePlumberParser(object):
    def __init__(self):
        self._file_path = expanduser("~/.local/state/wireplumber/stream-properties")
        self._entries = {}
        self._parse_property_file()

    def save(self):
        with open(self._file_path, "w") as file:
            file.write("[stream-properties]\n")
            for key in self._entries.keys():
                file.write(f"{self._entries[key]}\n")

    def set_channel_volume_for_app(self, stream_selector: str, volume: float):
        changed = False
        if stream_selector not in self._entries.keys():
            self._entries[stream_selector] = WirePlumberOutputAudio.create_new(stream_selector)
            changed = True

        if self._entries[stream_selector].set_channel_volume(volume):
            return True
        else:
            return changed

    def _parse_property_file(self):
        with open(self._file_path, "r") as file:
            for line in file:
                if line.startswith("[stream-properties]"):
                    continue

                if not line.startswith("#"):
                    selector, configuration = line.strip().split("=", 1)
                    category, selection_property, selection_pattern = selector.split(":", 2)
                    corrected_selection_pattern = selection_pattern.replace("\\s", " ")

                    match category:
                        case "Audio/Sink":
                            self._entries[corrected_selection_pattern] = WirePlumberAudioSink(selection_property,
                                                                                    selection_pattern, configuration)
                        case "Input/Audio":
                            self._entries[corrected_selection_pattern] = WirePlumberInputAudio(selection_property,
                                                                                     selection_pattern, configuration)
                        case "Output/Audio":
                            self._entries[corrected_selection_pattern] = WirePlumberOutputAudio(selection_property,
                                                                                      selection_pattern, configuration)
                        case _:
                            raise ValueError("Unknown selector {}".format(selector))


def run_module():
    module_args = dict(
        app_name=dict(type='str', required=True),
        volume=dict(type='float', required=True),
        description=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        message='The item was already in the desired state'
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # validate parameters
    if module.params['volume'] is not None and (module.params['volume'] < 0.0 or module.params['volume'] > 1.0):
        module.fail_json(msg='volume must be between 0.0 and 1.0', **result)

    #
    parser = WirePlumberParser()
    changed = parser.set_channel_volume_for_app(module.params['app_name'], module.params['volume'])
    if changed:
        result['changed'] = True
        result['message'] = f'The channel volume for "{module.params['app_name']}" has been set'

    # if we're in check mode, don't make any changes
    if module.check_mode:
        module.exit_json(**result)

    if changed:
        parser.save()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

