from cloudshell.recorder.rest.configuration import Configuration
from cloudshell.recorder.rest.rest_recorder import RestRecorder

if __name__ == '__main__':
    record_table = "request_table_visionedge.yaml"
    base_url = "https://192.168.51.68:8000/api"

    conf = Configuration(record_table)

    recorder = RestRecorder(base_url)
    recorder.initialize(conf.get_session())
    recorder.record(conf.get_requests())
    recorder.save('saved_table.yaml')
