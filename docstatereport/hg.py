import struct
import subprocess


class Mercurial:
    def __init__(self):
        self.server = subprocess.Popen(
            ['hg', '--config', 'ui.interactive=True', 'serve', '--cmdserver',
             'pipe'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        hello = self.readchannel()

    def __del__(self):
        self.server.stdin.close()
        self.server.wait()

    def readchannel(self):
        channel, length = struct.unpack('>cI', self.server.stdout.read(5))
        if channel in 'IL':
            return channel, length
        return channel, self.server.stdout.read(length)

    def writeblock(self, data):
        self.server.stdin.write(struct.pack('>I', len(data)))
        self.server.stdin.write(data)
        self.server.stdin.flush()

    def runcommand(self, data):
        self.server.stdin.write('runcommand\n')
        self.writeblock('\0'.join(data))
        return self.receive_response()

    def receive_response(self):
        errors = []
        while True:
            channel, val = self.readchannel()
            if channel == 'o':
                yield val
            elif channel == 'r':
                exit_code = struct.unpack(">l", val)[0]
                if exit_code != 0 or errors:
                    raise Exception("command failed", exit_code, errors)
                else:
                    break
            elif channel == 'e':
                errors.append(val)
            else:
                raise Exception("unexpected channel:", channel, val)

    def manifest(self, revision):
        return self.runcommand(['manifest', '-r', revision])

    def parent(self, revision, file_name):
        results = self.runcommand(['parent', '-r', revision, file_name, '-T',
                                   '{author}\n{date|shortdate}'])
        results = list(results)
        splitted = results[0].split('\n')
        return {'file_name': file_name, 'author': splitted[0],
                'date': splitted[1]}
