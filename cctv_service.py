import time
import traceback


def main():
    # read the value of carrier of eth0, 1 == connected, 0 == not connected
    with open("/sys/class/net/eth0/carrier") as f:
        _eth_connected = bool(int(f.read().rstrip()))

    neat_print("ethernet status: ", _eth_connected)

    # call the respective function
    if _eth_connected:
        eth_connected()
    else:
        eth_not_connected()


def eth_connected():
    # ethenet is connected, simply stop this service
    neat_print("ethernet is connected, not starting TCU")
    exit(0)


def eth_not_connected():
    # ethernet is not connected, start the tcu script
    neat_print("ethernet is not connected, starting TCU...")
    import tcu_main

    try:
        tcu_main.main()
    except BaseException:
        traceback.print_exc()
        neat_print("cctv_main.main() raised error")
        exit(1)

    neat_print("cctv_service.py is stopped")
    exit(0)


def neat_print(*args):
    _time = round(time.time() * 1000) / 1000
    string = "[ {time} ] CCTV Service: ".format(time=_time)
    for arg in args:
        string += str(arg)

    print(string)


if __name__ == "__main__":
    main()
