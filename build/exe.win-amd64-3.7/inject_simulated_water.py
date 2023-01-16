import struct
import os
import nidaqmx
import time
from nidaqmx.constants import LineGrouping
import click
import logging
NUM_OF_BYTES_PER_TIME_VALUE = 6


def read_next_time_value(_br):
    pulse_time = 0
    try:
        # each time value represented as 48 bit value
        for i in range(NUM_OF_BYTES_PER_TIME_VALUE // 2):
            power = i * 8 * 2
            temp = int.from_bytes(_br.read(2), byteorder='little', signed=False)
            temp = temp << power
            pulse_time += temp

    except IOError as e:
        print(f"\nError message: {e}\n")
        # print(f"Details:\n{traceback.format_exc()}")

    pulse_time = (pulse_time * 1000) / 2048
    return int(pulse_time)


def get_time_values(filename):
    ret_val = []
    _br = open(filename, 'rb')
    file_len = os.path.getsize(filename)
    _fileCurrentPos = 0
    out_val = 0
    while _fileCurrentPos + NUM_OF_BYTES_PER_TIME_VALUE <= file_len:
        if out_val > 0:
            pulse_time = read_next_time_value(_br)
        else:
            pulse_time = 1
        out_val = 0 if out_val > 0 else 3.3  # there is no value to the 3.3. next we will put True whenever value = 3.3
        ret_val.append((pulse_time, out_val))
        _fileCurrentPos += NUM_OF_BYTES_PER_TIME_VALUE
    _br.close()
    return ret_val


@click.command()
@click.option('--filename', '-f', default='major.bin', show_default=True, type=str, help='Data file name.')
@click.option('--verbose', '-v',is_flag=True, show_default=True, default=False,
              help='Verbose mode - log debug messages.')
@click.option('--line', '-l', show_default=True, default=1, type=int, help='Digital output number [0-7]')
def main(filename, verbose, line):
    logging.basicConfig(filename=f'injector-{line}.log', format='%(asctime)s: %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG if verbose is True else logging.INFO)

    logger.info('Start running')

    _digital_g_OutTask = nidaqmx.Task()
    logger.debug('Create task')

    # Create the digital output channel
    _digitalOutput = _digital_g_OutTask.do_channels.add_do_chan(f"Dev1/port0/line{line}")
    # _digitalOutput.start()

    logging.debug('Build list of timeout,value')
    ret_val = get_time_values(filename=filename)

    logging.debug('Start loop')
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(f"Dev1/port0/line{line}", line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
        try:
            for delay, pulse in ret_val[18:]:
                task.write(True)
                # set 0 < pulse < 2001
                delay = delay if delay > 1 else 1000  # if the dt is negative number, i fix it to 1 second
                delay = delay if delay < 2000 else 2000
                time.sleep(delay/1000.0)
                task.write(False)
        except nidaqmx.DaqError as e:
            logger.error('Fail to set pulse', e)

        except KeyboardInterrupt:
            logger.info("ctrl-C pressed")

    logger.info('Exiting../.')


if __name__ == "__main__":
    main()
