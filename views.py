from controller import Controller, Calculator

controller = Controller()
calculator = Calculator(controller)
info = '''
        -sf <path to file>, --seqfile <path to file>  - read sequence from file and set active
        -s <sequence>, --sequence <sequence>  - enter sequence when file not provided and set active
        -n <number>, --number <number>  - print element number of active sequence
        -r |<number>, --random |<number>  - generate full random sequence | generate sequence with <number> len
        -p |<sequence id>, --print |<sequence id>  - without parameter print <id>. <len> | print sequence items with id
        -a <sequence id>, --active <sequence id>  - select sequence with id as active
        -e |<filename>, --export |<filename>  - export sequences to csv file
        -calc, --calculate  - simple calculator for sequences
        -h, --help  - print help menu (this)
        -h <command>, --help <command>  - print help menu with example for command (-n;-s;-sf)
        -q, --quit  - exit from program 
        -v, --version  - print tool version
    '''
help_seqfile = '''
    Import sequence from XML file.
    --seqfile usage:
        -sf /path/to/xml/file.xml
        or
        --seqfile C:\\path\\to\\xml\\file.xml
    '''
help_sequence = '''
    IDK for what, but you can enter additional parameters for sequence item, parameter "value" is required!
    If you sequence in [] - no need in "value" parameter.
    --sequence usage:
        -s [1,2,3,4,5,6]
        or
        --sequence {"name":"test","salary":9000,"value": 0}
    '''
help_number = '''
    Print sequence element by your number.
    --number usage:
        -n 1
        or
        --number 5
    '''


class View:

    def __init__(self):
        self.command = ''
        self.version_number = '0.0.1'

    def menu(self):
        self.help_info()
        while True:
            raw_command = input('Enter command:')
            command = raw_command.split(' ')
            match len(command):
                case 1:
                    match command[0]:
                        case '-sf' | '--seqfile':
                            print('You forget path to file!')
                        case '-s' | '--sequence':
                            print('You forget sequence!')
                        case '-n' | '--number':
                            print('You forget number!')
                        case '-a' | '--active':
                            controller.print_active()
                        case '-p' | '--print':
                            controller.print_sequences()
                        case '-e' | '--export':
                            controller.export()
                        case '-r' | '--random':
                            controller.random_all()
                        case '-h' | '--help':
                            self.help_info()
                        case '-v' | '--version':
                            self.version()
                        case '-q' | '--quit':
                            break
                        case _:
                            print('Unknown command')
                case 2:
                    match command:
                        case '-sf' | '--seqfile', filename:
                            controller.load_file(filename)
                        case '-s' | '--sequence', sequence:
                            controller.load_sequence(sequence)
                        case '-a' | '--active', index:
                            controller.set_active(index)
                        case '-n' | '--number', number:
                            controller.get_element(number)
                        case '-e' | '--export', filename:
                            controller.export(filename)
                        case '-r' | '--random', number:
                            controller.random_sequence(number)
                        case '-calc' | '--calculate', expression:
                            calculator.parse(expression)
                        case '-p' | '--print', index:
                            controller.print_sequence(index)
                        case '-h' | '--help', command:
                            self.command = command
                            self.help_info()
                        case _:
                            print('Unknown command')
                case _:
                    match command:
                        case '-s' | '--sequence', *kwt:
                            controller.load_sequence(' '.join(kwt))
                        case _:
                            print(command)

    def help_info(self):
        if self.command:
            match self.command:
                case '-sf' | '--seqfile':
                    print(help_seqfile)
                case '-s' | '--sequence':
                    print(help_sequence)
                case '-n' | '--number':
                    print(help_number)
        else:
            print(info)

    def version(self):
        print(f'version {self.version_number}')


